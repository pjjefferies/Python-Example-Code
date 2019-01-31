# -*- coding: utf-8 -*-
"""

Script for auditing B-dirve Honda Files

"""

import os, re, datetime
from stat import *
CATIAFILEEXTENTIONS = ('catpart', 'catproduct', 'catdrawing')
DATEDDIRECTORIES = ('studies', 'incoming', 'outcoming')
def findReleaseDirs(top):
    releaseDirList = []
    for f in os.listdir(top):
        if "Honda" not in f:
            continue
        programPathName = os.path.join(top, f)
        programReleasePathName = os.path.join(programPathName, "released")
        try:
            mode = os.stat(programReleasePathName).st_mode
            if S_ISDIR(mode):
                # It's a directory, as it should be, add it to list
                #print("DIR:", pathname)
                releaseDirList.append(programReleasePathName)
                vpmProgramReleasePathName = os.path.join(programReleasePathName, "VPM")
                try:
                    mode = os.stat(vpmProgramReleasePathName).st_mode
                    if S_ISDIR(mode):
                        # We have a VPM directory, add it to list
                        #print("DIR:", pathname)
                        releaseDirList.append(vpmProgramReleasePathName)
                    else:
                        #Not a directory, please drive through
                        pass
                except(FileNotFoundError):
                    #print("No VPM Dir:", vpmProgramReleasePathName)
                    pass
            else:
                # Unknown file type, print a message
                #print('Skipping %s' % pathname)
                pass
        except(FileNotFoundError):
            print("File not found:", programReleasePathName + ". Skipping")
    return releaseDirList

def findReviewedDirs(top):
    reviewDirList = []
    for f in os.listdir(top):
        if "Honda" not in f:
            continue
        programPathName = os.path.join(top, f)
        programReviewPathName = os.path.join(programPathName, "reviewed")
        try:
            mode = os.stat(programReviewPathName).st_mode
            if S_ISDIR(mode):
                # It's a directory, as it should be, add it to list
                #print("DIR:", pathname)
                reviewDirList.append(programReviewPathName)
            else:
                # Unknown file type, print a message
                #print('Skipping %s' % pathname)
                pass
        except(FileNotFoundError):
            print("File not found:", programReviewPathName + ". Skipping")
    return reviewDirList

def findStudIncOutDirs(top):
    datedDirList = []
    for f in os.listdir(top):
        if "Honda" not in f:
            continue
        programPathName = os.path.join(top, f)
        for datedDirectory in DATEDDIRECTORIES:
            programDatedPathName = os.path.join(programPathName, datedDirectory)
            try:
                mode = os.stat(programDatedPathName).st_mode
                if S_ISDIR(mode):
                    # It's a directory, as it should be, add it to list
                    #print("DIR:", pathname)
                    datedDirList.append(programDatedPathName)
                else:
                    # Unknown file type, print a message
                    #print('Skipping %s' % pathname)
                    pass
            except(FileNotFoundError):
                print("File not found:", programDatedPathName + ". Skipping")
    return datedDirList

def isACATIAFile(fileName):
    return re.split('\.', fileName)[-1].lower() in CATIAFILEEXTENTIONS


def findCATIAFilesIn(aCATIADir):
    listOfCATIAFilesFound = []
    for f in os.listdir(aCATIADir):
        #Is's a file, check if a CATIA File
        if isACATIAFile(f):
            listOfCATIAFilesFound.append(f)
    return listOfCATIAFilesFound


def findFoldersIn(aCATIADir):
    listOfFoldersFound = []
    for f in os.listdir(aCATIADir):
        programDatedPathName = os.path.join(aCATIADir, f)
        try:
            mode = os.stat(programDatedPathName).st_mode
            if S_ISDIR(mode):
                # It's a directory, as it should be, add it to list
                #print("DIR:", pathname)
                listOfFoldersFound.append(programDatedPathName)
            else:
                # Not a directory, print a message
                #print('Skipping %s' % pathname)
                pass
        except(FileNotFoundError):
            print("File not found:", programDatedPathName + ". Skipping")
    return listOfFoldersFound


def separateCATIAFileList(aCATIAFileList):
    aCATIAFileListParts, aCATIAFileListProducts, aCATIAFileListDrawings = [], [], []
    for aCATIAFile in aCATIAFileList:
        if re.split('\.', aCATIAFile)[-1].lower() == "catpart":
            aCATIAFileListParts.append(aCATIAFile)
        elif re.split('\.', aCATIAFile)[-1].lower() == "catproduct":
            aCATIAFileListProducts.append(aCATIAFile)
        elif re.split('\.', aCATIAFile)[-1].lower() == "catdrawing":
            aCATIAFileListDrawings.append(aCATIAFile)
        else:
            #Not a CATIA File, ignoring
            pass
    return aCATIAFileListParts, aCATIAFileListProducts, aCATIAFileListDrawings


def performSubCATIARelDirQualChekc(subCATIAFileList):
    tempAddToCQualRep = ""
    partListLength = len(subCATIAFileList)
    for aCATIAPartSeqNo in range(partListLength):
        aCATIAPart = subCATIAFileList[aCATIAPartSeqNo]
        try:
            aCATIAPartNo = int(re.split('[_ .]', aCATIAPart)[0])
            if aCATIAPartNo < 100000:
                #Not a real part number, skip
                continue
        except ValueError:
            #Not a part number, go to next
            continue
        try:
            aCATIAPartRevNo = re.split('[_ .]', aCATIAPart)[1]
            if (re.search("[a-zA-Z]", aCATIAPartRevNo[0]) and
                len(aCATIAPartRevNo) > 1):
                aCATIAPartRevNo = int(aCATIAPartRevNo[1:])
            else:
                aCATIAPartRevNo = int(aCATIAPartRevNo)
        except ValueError:
            tempAddToCQualRep += ("Non-standard or proto Format Rev.: " + aCATIAPart + "\n")
            continue
        for bCATIAPartSeqNo in range(aCATIAPartSeqNo+1, partListLength):
            bCATIAPart = subCATIAFileList[bCATIAPartSeqNo]
            try:
                bCATIAPartNo = int(re.split('[_ .]', bCATIAPart)[0])
                if bCATIAPartNo < 100000:
                    #Not a real part number, skip
                    continue
            except ValueError:
                #Not a part number, go to next
                continue
            try:
                bCATIAPartRevNo = re.split('[_ .]', bCATIAPart)[1]
                if (re.search("[a-zA-Z]", bCATIAPartRevNo[0]) and
                    len(bCATIAPartRevNo) > 1):
                    bCATIAPartRevNo = int(bCATIAPartRevNo[1:])
                else:
                    bCATIAPartRevNo = int(bCATIAPartRevNo)
            except ValueError:
                #Don't record, just skip, will get caught as aCATIAPart
                continue
            if re.split('[_ .]', aCATIAPart)[0] == re.split('[_ .]', bCATIAPart)[0]:
                #found duplicate part numbers, see if INSTALLED, ORBITAL, SWAGED in name
                if (("INSTALLED" in aCATIAPart or "INSTALLED" in bCATIAPart) or
                    ("ORBITAL" in aCATIAPart or "ORBITAL" in bCATIAPart) or
                    ("SWAGED" in aCATIAPart or "SWAGED" in bCATIAPart) or
                    ("CRIMPED" in aCATIAPart or "CRIMPED" in bCATIAPart) or
                    ("GAUGE" in aCATIAPart or "GAUGE" in bCATIAPart)):
                    #OK if revs are the same, let's see...
                    if (aCATIAPartRevNo == bCATIAPartRevNo):
                        #Installed, etc. part matching rev. level, no concern
                        continue
                    else:
                        tempAddToCQualRep += ("Alt. Part Rev. not matching:       " + aCATIAPart + "\n"
                                            + "                                   " + bCATIAPart + "\n")
                else:
                    tempAddToCQualRep += ("Duplicate Part Numbers:            " + aCATIAPart + "\n"
                                        + "                                   " + bCATIAPart + "\n")
    return tempAddToCQualRep


def isADate(possibleDateString):   #YYYY-MM-DD
    if len(possibleDateString) != 10:
        return False
    try:
        year = int(possibleDateString[:4])
        month = int(possibleDateString[5:7])
        day = int(possibleDateString[8:])
        theDate = date(year, month, day)
        return True
    except ValueError:
        return False


def properFormatDatedFolder(oneCATIADatedFolderName):
    return (isADate(oneCATIADatedFolderName[:10]) and
           (oneCATIADatedFolderName[10:13] == " - "))



def performCATIADatedDirQualityCheck(datedCATIAFolderList):
    tempAddToCQualRep = ""
    for aCATIADatedFolderName in datedCATIAFolderList:
        if not properFormatDatedFolder(aCATIADatedFolderName):
            tempAddToCQualRep += ("Improperly formated dated folder: " + aCATIADatedFolderName)
    return tempAddToCQualRep


def performCATIAReleaseDirQualityCheck(CATIAFileList):
    additionToCATIAQualityReport = ""
   
    cFileListParts, cFileListProducts, cFileListDrawings = separateCATIAFileList(CATIAFileList)

    additionToCATIAQualityReport += performSubCATIARelDirQualChekc(cFileListParts)
    additionToCATIAQualityReport += performSubCATIARelDirQualChekc(cFileListProducts)
    additionToCATIAQualityReport += performSubCATIARelDirQualChekc(cFileListDrawings)

    return additionToCATIAQualityReport



if __name__ == '__main__':
    rootFile = "B:\\cpp_mechs\\adjusters"
    reportSaveLoc = "C:\\Users\\ajeffep\\Documents\\Data\\Engineering\\Software\\B-DriveCheck"
    tempSaveFile = "C:\\Users\\ajeffep\\Documents\\Data\\Engineering\\Software\\B-DriveCheck\\tempDictOfCATIAFiles.json"
    datetimeNow = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    reportFileName = reportSaveLoc + "\\Honda CATIA Flat File Report - " + datetimeNow

    hondaDirReport = "Honda CATIA Release Folder Quality Audit - " + datetimeNow +"\n\n"

    #Create Release directory summary of duplicate and other inappropriate files
    listOfReleaseDirs = findReleaseDirs(rootFile)
    CATIAFilesIn = {}
    for releaseDir in listOfReleaseDirs:
        CATIAFilesIn[releaseDir] = findCATIAFilesIn(releaseDir)

    for releaseDir in iter(CATIAFilesIn):
        hondaDirReport += ("In directory " + releaseDir)
        if not "Honda Accord 2011x" in releaseDir:
            reportToAdd = performCATIAReleaseDirQualityCheck(CATIAFilesIn[releaseDir])
            if reportToAdd == "":
                hondaDirReport += ": OK\n\n"
            else:
                hondaDirReport += ("\n" + reportToAdd + "\n\n")
        else:
            hondaDirReport += " -- Skipping, no interest\n\n"
            
    #Create Reviewed directory summary of files not released
    listOfReviewedDirs = findReviewedDirs(rootFile)
    CATIAFilesIn = {}
    for reviewedDir in listOfReviewedDirs:
        CATIAFilesIn[reviewedDir] = findCATIAFilesIn(reviewedDir)

    hondaDirReport += "\n\nHonda CATIA Reviewed Directory Quality Audit\n\n"

    for reviewedDir in iter(CATIAFilesIn):
        hondaDirReport += ("In directory " + reviewedDir)
        if len(CATIAFilesIn[reviewedDir]) == 0:
            hondaDirReport += ": Empty - OK\n\n"
        else:
            hondaDirReport += ("\n")
            for reviewedFile in CATIAFilesIn[reviewedDir]:
                hondaDirReport += (reviewedFile+ "\n")
            hondaDirReport += ("\n")
    
    #Create Study, Incomming, Outgoing Directory summary of folders not formatted correctly
    listOfStudIncOutDirs = findStudIncOutDirs(rootFile)
    CATIAFilesIn = {}
    for datedDir in listOfStudIncOutDirs:
        CATIAFilesIn[datedDir] = findFoldersIn(datedDir)

    hondaDirReport += "\n\nHonda CATIA Study/Incoming/Outgoing Directory Quality Audit\n\n"

    for dateddDir in iter(CATIAFilesIn):
        hondaDirReport += ("In directory " + datedDir)
        reportToAdd = performCATIADatedDirQualityCheck(CATIAFilesIn[datedDir])
        if reportToAdd == "":
            hondaDirReport += ": OK\n\n"
        else:
            hondaDirReport += ("\n" + reportToAdd + "\n\n")

    with open(reportFileName, "w") as text_file:
        text_file.write(hondaDirReport)