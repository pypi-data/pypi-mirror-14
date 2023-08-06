"""
Utils that support fringe DataSet features.
"""
import os
import tempfile
import logging
import json
import shutil
import pysam
from pbcore.util.Process import backticks

log = logging.getLogger(__name__)

def consolidateBams(inFiles, outFile, filterDset=None, useTmp=True):
    """Take a list of infiles, an outFile to produce, and optionally a dataset
    (filters) to provide the definition and content of filtrations."""
    # check space available
    final_free_space = disk_free(os.path.split(outFile)[0])
    projected_size = sum(file_size(infn) for infn in inFiles)
    log.debug("Projected size:            {p}".format(p=projected_size))
    log.debug("In place free space:       {f}".format(f=final_free_space))
    # give it a 5% buffer
    if final_free_space < (projected_size * 1.05):
        raise RuntimeError("No space available to consolidate")
    if useTmp:
        tmpout = tempfile.mkdtemp(suffix="consolidation-filtration")
        tmp_free_space = disk_free(tmpout)
        log.debug("Tmp free space (need ~2x): {f}".format(f=tmp_free_space))
        # need 2x for tmp in and out, plus 10% buffer
        if tmp_free_space > (projected_size * 2.1):
            log.debug("Using tmp storage: " + tmpout)
            tmpInFiles = _tmpFiles(inFiles, tmpout)
            origOutFile = outFile
            origInFiles = inFiles[:]
            inFiles = tmpInFiles
            outFile = os.path.join(tmpout, "outfile.bam")
        else:
            log.debug("Using in place storage")
            useTmp = False

    if filterDset and filterDset.filters:
        finalOutfile = outFile
        outFile = _infixFname(outFile, "_unfiltered")
    _mergeBams(inFiles, outFile)
    if filterDset and filterDset.filters:
        _filterBam(outFile, finalOutfile, filterDset)
        outFile = finalOutfile
    _indexBam(outFile)
    _pbindexBam(outFile)
    if useTmp:
        shutil.copy(outFile, origOutFile)
        shutil.copy(outFile + ".bai", origOutFile + ".bai")
        shutil.copy(outFile + ".pbi", origOutFile + ".pbi")
        # cleanup:
        shutil.rmtree(os.path.split(outFile)[0])

def _tmpFiles(inFiles, tmpout=None):
    tmpInFiles = []
    if tmpout is None:
        tmpout = tempfile.mkdtemp(suffix="consolidation-filtration")
    for i, fname in enumerate(inFiles):
        newfn = _infixFname(os.path.join(tmpout, os.path.basename(fname)), i)
        shutil.copy(fname, newfn)
        tmpInFiles.append(newfn)
    return tmpInFiles

def disk_free(path):
    if path == '':
        path = os.getcwd()
    space = os.statvfs(path)
    return space.f_bavail * space.f_frsize

def file_size(path):
    return os.stat(path).st_size

def _pbindexBam(fname):
    cmd = "pbindex {i}".format(i=fname)
    log.info(cmd)
    o, r, m = backticks(cmd)
    if r != 0:
        raise RuntimeError(m)
    return fname + ".pbi"

# Singleton so we don't need to check and parse repeatedly
class BamtoolsVersion:
    class __BamtoolsVersion:
        def __init__(self):
            cmd = "bamtools -v"
            o, r, m = backticks(cmd)

            if r == 127:
                self.good = False
                return

            version = ''
            for line in o:
                if line.startswith("bamtools"):
                    version = line.split(' ')[-1]
                    break
            self.number = version
            if map(int, version.split('.')) >= [2, 4, 0]:
                self.good = True
            else:
                self.good = False

    instance = None
    def __init__(self):
        if not BamtoolsVersion.instance:
            BamtoolsVersion.instance = BamtoolsVersion.__BamtoolsVersion()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def check(self):
        if not self.good:
            raise RuntimeError("Bamtools version >= 2.4.0 required for "
                               "consolidation")

def _sortBam(fname):
    BamtoolsVersion().check()
    tmpname = _infixFname(fname, "_sorted")
    cmd = "bamtools sort -in {i} -out {o}".format(i=fname, o=tmpname)
    log.info(cmd)
    o, r, m = backticks(cmd)
    if r != 0:
        raise RuntimeError(m)
    shutil.move(tmpname, fname)

def _indexBam(fname):
    pysam.index(fname)
    return fname + ".bai"

def _indexFasta(fname):
    pysam.faidx(fname)
    return fname + ".fai"

def _mergeBams(inFiles, outFile):
    BamtoolsVersion().check()
    if len(inFiles) > 1:
        cmd = "bamtools merge -in {i} -out {o}".format(i=' -in '.join(inFiles),
                                                       o=outFile)
        log.info(cmd)
        o, r, m = backticks(cmd)
        if r != 0:
            raise RuntimeError(m)
    else:
        shutil.copy(inFiles[0], outFile)

def _filterBam(inFile, outFile, filterDset):
    BamtoolsVersion().check()
    tmpout = tempfile.mkdtemp(suffix="consolidation-filtration")
    filtScriptName = os.path.join(tmpout, "filtScript.json")
    _emitFilterScript(filterDset, filtScriptName)
    cmd = "bamtools filter -in {i} -out {o} -script {s}".format(
        i=inFile, o=outFile, s=filtScriptName)
    log.info(cmd)
    o, r, m = backticks(cmd)
    if r != 0:
        raise RuntimeError(m)

def _infixFname(fname, infix):
    prefix, extension = os.path.splitext(fname)
    return prefix + str(infix) + extension

def _emitFilterScript(filterDset, filtScriptName):
    """Use the filter script feature of bamtools. Use with specific filters if
    all that are needed are available, otherwise filter by readname (easy but
    uselessly expensive)"""
    filterMap = {'rname': 'reference',
                 'pos': 'position',
                 'length': 'queryBases',
                 'qname': 'name',
                 'rq': 'mapQuality'}
    cheapFilters = True
    for filt in filterDset.filters:
        for req in filt:
            if not filterMap.get(req.name):
                cheapFilters = False
    if cheapFilters:
        script = {"filters":[]}
        for filt in filterDset.filters:
            filtDict = {}
            for req in filt:
                name = filterMap[req.name]
                if name == 'reference':
                    if req.operator == '=' or req.operator == '==':
                        filtDict[name] = req.value
                    else:
                        raise NotImplementedError()
                else:
                    filtDict[name] = req.operator + req.value
            script['filters'].append(filtDict)
    else:
        names = [rec.qName for rec in filterDset]
        script = {"filters":[{"name": name} for name in names]}
    with open(filtScriptName, 'w') as scriptFile:
        scriptFile.write(json.dumps(script))

