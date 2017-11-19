# encoding:utf8
import subprocess
import re
import os
import sys
import urllib

def hasSetup():
    return False


def setup():
    subprocess.Popen("git config --global core.quotepath false", shell=True).wait()
    pass


def updateGitStatus():
    subprocess.Popen("git add -A .", shell=True).wait()


def getNewFileList():
    ret = subprocess.check_output("git status", shell=True)
    newFileList = re.findall("\s*new file:\s*([^\s]*)\s*", ret)
    return newFileList


def commitAndPublish(filelist):
    msg = '新增%s张图片'%len(filelist)
    for f in filelist:
        msg += f+"\n"
    subprocess.Popen('git commit -m "%s"' % msg, shell=True).wait()
    subprocess.Popen('git push origin master', shell=True).wait()
    generateNewHtml(filelist)


def generateNewHtml(filelist):
    body = ''
    rawBaseUrl = getRawBaseUrl()
    for file in filelist:
        fileUrl = "%s%s"%(rawBaseUrl, file)
        body += '<img src="%s"/><br/>\n'%os.path.abspath(file)
        body += '<a href="%s">%s</a><br/>\n' % (fileUrl, fileUrl)
    tmplfile = open("tmpl/newfileurl.html")
    tmplcontent = tmplfile.read()
    content = tmplcontent.replace("<?placeholder?>", body)
    fd = os.open("display.html", os.O_CREAT)
    os.close(fd)
    # print content
    displayfile = open("display.html", "w+")
    displayfile.write(content)

def getRemotePath():
    ret = subprocess.check_output("git remote -v", shell=True)
    mo = re.search("[^\s]*\s*(.*)\(fetch\)", ret)
    if mo:
        return mo.group(1)
    else:
        raise Exception("fail to get remote path")


def getRawBaseUrl():
    remoteUrl = getRemotePath()
    print remoteUrl
    accountname = re.search("github\.com/([^/]*)", remoteUrl).group(1)
    reponame = re.search("([^/]*)\.git\s*$", remoteUrl, re.M).group(1)
    return "https://raw.githubusercontent.com/%s/%s/master/" % (accountname, reponame)

def validateFilename():
    files = os.listdir("pics")
    for f in files:
        fr = f.replace(" ", "")
        if fr != f:
            os.rename(os.path.join("pics", f), os.path.join("pics", fr))

def main():
    if not hasSetup():
        setup()
    validateFilename()
    updateGitStatus()
    newFiles = getNewFileList()
    commitAndPublish(newFiles)


if __name__ == '__main__':
    main()

