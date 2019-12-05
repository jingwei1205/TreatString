# -*- coding: utf-8 -*-
# @Time    : 2019/8/3 11:24
# @Author  : jingwei
# @FileName: windowsUse.py
# @Software: PyCharm
# @Blog    ：https://www.cnblogs.com/Jewish/

import re
# from bs4 import BeautifulSoup
#
# #剔除剩余的html代码(不剔除图片标签）
# def deleteHtmlCode(htmlContent):
#     #保留表格 首先替换自己代码
#     tableReg = re.compile(r'<table.*?</table>', re.S)
#     tableTransfer = tableReg.findall(htmlContent)  # 保存的表格
#     for n in range(len(tableTransfer)):
#         htmlContent = tableReg.sub("[[" + str(n) + "]]", htmlContent, 1)
#
#     #保留标题标签 首先替换自己代码
#     reg = re.compile(r'</?h\d+?>')
#     savedH = reg.findall(htmlContent)#保存的标题标签
#     for h in range(len(savedH)):
#         htmlContent = reg.sub("[a" + str(h) + "z]", htmlContent, 1)
#
#     #保留图片标签，首先替换自己代码
#     imageReg = r'<img.+?>'
#     imageReg = re.compile(imageReg)
#     imageCrash = imageReg.findall(htmlContent)
#     for num in range(len(imageCrash)):
#         htmlContent = imageReg.sub("{0["+str(num)+"]}", htmlContent,1)
#
#     #剔除所有标签
#     reg = r'</?(.+?)>'
#     reObject = re.compile(reg)
#     revisedContent = reObject.sub("", htmlContent)
#
#     #剔除空格
#     space=r'&nbsp;?'
#     revisedContent=re.sub(space,"",revisedContent)
#     #还原图片
#     revisedContent=revisedContent.format(imageCrash)
#     '''
#     还原标题
#     '''
#     exchange = re.compile(r'\[a\d+?z\]')
#     ls = re.findall(exchange, revisedContent)
#     for num in range(len(ls)):
#         revisedContent = exchange.sub(savedH[num], revisedContent, 1)
#
#     '''
#     还原表格
#     '''
#     regTableInsert = re.compile(r'\[\[\d+\]\]')
#     for tableNum in range(len(tableTransfer)):
#         revisedContent=regTableInsert.sub(tableTransfer[tableNum],revisedContent,1)
#     return revisedContent

# def AIJudgeHAndLeaveImage(halfDone):
#     autoFile = open("autoFile.txt", "wt", encoding='UTF-8')
#     autoFile.write(halfDone)
#     autoFile.close()
#     autoFile = open("autoFile.txt", "rt", encoding='UTF-8')
#     clear = open("titledResults.txt", "wt", encoding="utf8")
#     clear.close()
#     reg = re.compile(r'(.*?[：|、|:]?\w+\n$)', re.S)
#     line = autoFile.readline()
#     while line:
#         print(line)
#         success = reg.findall(line)
#         print(success)
#         if len(success) == 0:
#             titled = open("titledResults.txt", "a", encoding="utf8")
#             titled.write(line)
#         else:
#             title = "<h3>" + success[0] + "</h3>"
#             newLine = reg.sub(title, line)
#             titled = open("titledResults.txt", "a", encoding="utf8")
#             titled.write(newLine)
#         line = autoFile.readline()
#     titled.close()
#     titled = open("titledResults.txt", "rt", encoding="utf8")
#     finalAI=titled.read()
#     print(finalAI)
#     titled.close()
#     autoFile.close()
#     return finalAI


if __name__=='__main__':
    su=[]
    yes=open("testForSection.txt","rt",encoding="utf8")
    content=yes.read()
    reg=r'<\w+.*?style.*?>'
    section=re.compile(reg,re.S)
    half=section.findall(content)
    sureg=r'<\w+'
    for sth in half:
        su.append(re.findall(sureg,sth))
    print(su)
    for n in range(len(su)):
        content = section.sub("[[" + str(n) + "]]", content, 1)
        pass
    regTableInsert = re.compile(r'\[\[\d+\]\]')
    for tableNum in range(len(su)):
        content = regTableInsert.sub(su[tableNum][0]+">", content, 1)
    print(content)
    # clear=open("titledResults.txt","wt",encoding="utf8")
    # clear.close()
    # htmlContent=open("table.txt","rt",encoding="utf8")
    # reg = re.compile(r'(.*?[：|、|:]?\w+\n$)',re.S)
    # line=htmlContent.readline()
    # while line:
    #     print(line)
    #     success=reg.findall(line)
    #     print(success)
    #     if len(success)==0:
    #         titled = open("titledResults.txt", "a", encoding="utf8")
    #         titled.write(line)
    #     else:
    #         title="<h3>"+success[0]+"</h3>"
    #         newLine=reg.sub(title,line)
    #         titled=open("titledResults.txt","a",encoding="utf8")
    #         titled.write(newLine)
    #     line = htmlContent.readline()


