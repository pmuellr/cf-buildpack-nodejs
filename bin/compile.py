# Licensed under the Apache License. See footer for details.

# <build-dir> <cache-dir>

import os
import re
import sys
import json
import time
import semver      #from: https://github.com/k-bx/python-semver
import shutil
import urllib

#-------------------------------------------------------------------------------

Program  = os.path.basename(sys.argv[0])
BuildDir = sys.argv[1]
CacheDir = sys.argv[2]
TmpDir   = os.path.join(BuildDir, "..", "tmp")

# http://nodejs.org/dist/v0.10.20/node-v0.10.20-linux-x64.tar.gz
# http://nodejs.org/dist/v0.10.20/node-v0.10.20-darwin-x64.tar.gz

DownloadRoot = "http://nodejs.org/dist/"

if sys.platform.startswith("linux"):
    Platform = "linux-x64"    
elif sys.platform.startswith("darwin"):
    Platform = "darwin-x64"

#-------------------------------------------------------------------------------
def main():
    timeStart = time.clock()

    # set up tmp dir
    if os.path.exists(TmpDir):
        shutil.rmtree(TmpDir)
        
    os.mkdir(TmpDir)

    # read package.json
    packageJSON = getPackageJSON()

    # get node version from package.json
    nodeVersionPackage = "*"
    try:
        nodeVersionPackage = packageJSON["engines"]["node"]
    except KeyError:
        nodeVersionPackage = "*"

    log("build dir:                 %s" % BuildDir)
    log("cache dir:                 %s" % CacheDir)
    log("platform:                  %s" % Platform)
    log()

    # get list of versions available from node
    getCached("nodejs-versions.html", "http://nodejs.org/dist/")

    # get the actual version of ndoe to use
    nodeVersionActual = getActualNodeVersion(
        nodeVersionPackage, 
        cacheFileName("nodejs-versions.html")
    )

    if None == nodeVersionActual:
        error("unable to find compatible node version for %s" % nodeVersionPackage)

    log("node version from package: %s" % nodeVersionPackage)
    log("node version to install:   %s" % nodeVersionActual)

    # download the node distro
    nodeDownload = "%s/v%s/node-v%s-%s.tar.gz" % (
        DownloadRoot, 
        nodeVersionActual, 
        nodeVersionActual, 
        Platform 
    )

    nodeArchive = "node-%s.tar.gz" % nodeVersionActual
    getCached(nodeArchive, nodeDownload)

    nodeArchive = cacheFileName(nodeArchive)

    unpackDir = tmpFileName("node-unpacked")
    cmd = "tar xvf %s -C %s" % (nodeArchive, unpackDir)
    log("woulda run: %s" % cmd)

    # unpack the node distro
    timeElapsed = time.clock() - timeStart
    log()
    log("build took %.1f seconds" % timeElapsed)

#-------------------------------------------------------------------------------
def getActualNodeVersion(nodeVersionPackage, nodeVersionsHtml):
    nodeVersionsFile = open(nodeVersionsHtml)
    nodeVersionsContent = nodeVersionsFile.read()
    nodeVersionsFile.close()

    pattern = r"<a.*?>v(\d*)\.(\d*)\.(\d*)/</a>"
    regex   = re.compile(pattern)

    allVersions    = []
    stableVersions = []
    for match in regex.finditer(nodeVersionsContent):
        version = "%s.%s.%s" % (match.group(1), match.group(2), match.group(3))

        allVersions.append(version)

        minorVersion = int(match.group(2), 10)
        if minorVersion % 2 == 0:
            stableVersions.append(version)

    stableVersions.sort(semver.compare)
    stableVersions.reverse()

    allVersions.sort(semver.compare)
    allVersions.reverse()

    if nodeVersionPackage == "*": return stableVersions[0]

    for version in allVersions:
        if semver.match(version, nodeVersionPackage): return version

    return None

#-------------------------------------------------------------------------------
def getPackageJSON(): 
    packageJSONname = buildFileName("package.json")
    if not os.path.exists(packageJSONname):
        error("file package.json not found")

    packageJSONfile = open(packageJSONname)
    packageJSONstr  = packageJSONfile.read()
    packageJSONfile.close()

    return json.loads(packageJSONstr)

#-------------------------------------------------------------------------------
def getCached(cacheFile, remoteURL): 
    fullFile = cacheFileName(cacheFile)
    if os.path.exists(fullFile): 
        log("using cached version of %s" % cacheFile)
        return

    log(    "downloading new copy of %s" % cacheFile)
    urllib.urlretrieve(remoteURL, fullFile)

#-------------------------------------------------------------------------------
def tmpFileName(fileName): 
    return os.path.join(TmpDir, fileName)

#-------------------------------------------------------------------------------
def cacheFileName(fileName): 
    return os.path.join(CacheDir, fileName)

#-------------------------------------------------------------------------------
def buildFileName(fileName): 
    return os.path.join(BuildDir, fileName)

#-------------------------------------------------------------------------------
def error(message): 
    log()
    log("*** ERROR ***")
    log(message)
    log("*** ERROR ***")
    sys.exit(1)

#-------------------------------------------------------------------------------
def log(message=""): 
    if message == "":
        print ""
        return

    print "%s: %s" % (Program, message)

#-------------------------------------------------------------------------------
main()

#-------------------------------------------------------------------------------
# Copyright 2013 Patrick Mueller
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#-------------------------------------------------------------------------------
