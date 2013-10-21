# coding=gbk
__author__ = 'yiqiu.wsh'


import urllib.request
import codecs
import operator



# 支持bom-utf-8，utf-8,utf-16,gbk,gb2312
# 返回文件内容
def readTextFile(bytes):
    if bytes[:3] == codecs.BOM_UTF8:
        content = bytes[3:].decode('utf-8')
    else:
        try:
            content = bytes.decode('gb2312')
        except UnicodeDecodeError as err:
            try:
                content = bytes.decode('utf-16')
            except UnicodeDecodeError as err:
                try:
                    content = bytes.decode('utf-8')
                except UnicodeDecodeError as err:
                    try:
                        content = bytes.decode('gbk')
                    except UnicodeDecodeError as err:
                        content = ''
                        print('不支持此种类型的文本文件编码', err)
    return content

def downLoadHosts(urlStr , filePath):
    urlItem = urllib.request.urlopen(urlStr)
    htmSource = urlItem.read()
    urlItem.close()
    str = readTextFile(htmSource)
    filehandler = open(filePath,'w')
    filehandler.write("\r\n#UPDATE_SMART_HOST_START\r\n")
    filehandler.write(str)
    filehandler.write("\r\n#UPDATE_SMART_HOST_END\r\n")
    filehandler.close()
    print(htmSource)

def updateHosts(hostFilePath , updateFile , fileName):
    filehandler = open(hostFilePath + "\\"+fileName,'r+')
    filehandler.seek(0)
    alllines=filehandler.readlines();
    tempFp = open(updateFile,'r+')
    tempFp.seek(0)
    isOutHostsUpdate = True
    hostsList = list()
    for eachLine in alllines:
        resultStartCode = operator.eq(eachLine ,"#UPDATE_SMART_HOST_START")
        resultEndCode = operator.eq(eachLine ,"#UPDATE_SMART_HOST_END")
        if resultStartCode:
            isOutHostsUpdate = False
            continue
        if resultEndCode:
            isOutHostsUpdate = True
            continue
        if isOutHostsUpdate:
            hostsList.append(eachLine)
            print(eachLine)
    filehandler.close()
    tempFp.writelines(hostsList)
    tempFp.close()
    tempFp = open(updateFile,'r')
    alllines = tempFp.readlines();
    filehandler = open(hostFilePath + "\\"+fileName,'w')
    filehandler.writelines(alllines);
    filehandler.close()

downLoadHosts("https://smarthosts.googlecode.com/svn/trunk/hosts_us" , 'D:\develop\python\FuckGFW\hosts');

updateHosts("C:\Windows\System32\drivers\etc" , "D:\develop\python\FuckGFW\hosts" , "hosts")

