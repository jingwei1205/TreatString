##!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/3 10:13
# @Author  : jingwei
# @FileName: quickTreatingString.py
# @Software: PyCharm
# @Blog    ：https://www.cnblogs.com/Jewish/
import re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import random
import subprocess


# 保留
def saveUsefulInformation(htmlContent):
    #保留p标签
    preg=r'<p.*?>'
    plabel=re.compile(preg)
    pNum=plabel.findall(htmlContent)
    for pnumber in range(len(pNum)):
        htmlContent=plabel.sub("plabel" + str(pnumber) + "plabel", htmlContent, 1)
        pass

    # 保留/p标签
    pdreg = r'</p>'
    pdlabel = re.compile(pdreg)
    pdNum = pdlabel.findall(htmlContent)
    for pdnumber in range(len(pdNum)):
        htmlContent = pdlabel.sub("pdlabel" + str(pdnumber) + "pdlabel", htmlContent, 1)
        pass

    #保留seciton
    sectionreg=r'<section.*?>'
    section=re.compile(sectionreg)
    sectionNum=section.findall(htmlContent)
    for sectionnumber in range(len(sectionNum)):
        htmlContent=section.sub("@@" + str(sectionnumber) + "@@", htmlContent, 1)
        pass

    #保留/seciton
    devidereg=r'</section>'
    devidesection=re.compile(devidereg)
    devideNum=devidesection.findall(htmlContent)
    for devidenum in range(len(devideNum)):
        htmlContent=devidesection.sub("label" + str(devidenum) + "label", htmlContent, 1)
        pass

    # 保留表格 首先替换自己代码
    tableReg = re.compile(r'<table.*?</table>', re.S)
    tableTransfer = tableReg.findall(htmlContent)  # 保存的表格
    for n in range(len(tableTransfer)):
        htmlContent = tableReg.sub("[[" + str(n) + "]]", htmlContent, 1)
        pass

    # 保留标题标签 首先替换自己代码
    reg = re.compile(r'</?h\d+?>')
    savedH = reg.findall(htmlContent)  # 保存的标题标签
    for h in range(len(savedH)):
        htmlContent = reg.sub("[a" + str(h) + "z]", htmlContent, 1)
        pass

    # 保留图片标签，首先替换自己代码
    imageReg = r'<img.+?>'
    imageReg = re.compile(imageReg)
    imageCrash = imageReg.findall(htmlContent)
    for num in range(len(imageCrash)):
        htmlContent = imageReg.sub("{0[" + str(num) + "]}", htmlContent, 1)
        pass

    return htmlContent,tableTransfer,savedH,imageCrash

#还原
def backUsefulInformation(zero,one,two,three):
    #还原表格
    regTableInsert = re.compile(r'\[\[\d+\]\]')
    for tableNum in range(len(one)):
        zero = regTableInsert.sub(one[tableNum], zero, 1)
    # 还原seciton
    regSInsert = re.compile(r'@@\d+@@')
    zero = regSInsert.sub("<section>", zero)
    # 还原/seciton
    regDInsert = re.compile(r'label\d+label')
    zero = regDInsert.sub("</section>", zero)
    #还原p
    regPInsert = re.compile(r'plabel\d+plabel')
    zero = regPInsert.sub("<p>", zero)
    regPInsert = re.compile(r'pdlabel\d+pdlabel')
    zero = regPInsert.sub("</p>", zero)
    #还原标题
    exchange = re.compile(r'\[a\d+?z\]')
    ls = re.findall(exchange, zero)
    for num in range(len(ls)):
        zero = exchange.sub(two[num], zero, 1)
    # 还原图片
    zero = zero.format(three)
    return zero

def deleteHtmlCode(orignal):
    htmlContent,tableTransfer,savedH,imageCrash=saveUsefulInformation(orignal)
    # 剔除所有标签
    reg = r'</?(.+?)>'
    reObject = re.compile(reg)
    htmlContent = reObject.sub("", htmlContent)
    # 剔除空格
    space = r'&nbsp;?'
    htmlContent = re.sub(space, "", htmlContent)
    return backUsefulInformation(htmlContent,tableTransfer,savedH,imageCrash)

def deleteHtmlCodeAndImage(htmlContent):
    # # 保留图片标签，首先替换自己代码
    # imageReg = r'<img.+?>'
    # imageReg = re.compile(imageReg)
    # imageCrash = imageReg.findall(htmlContent)
    # for num in range(len(imageCrash)):
    # htmlContent = imageReg.sub("@@" + str(num) + "@@", htmlContent, 1)
    # 保留表格 首先替换自己代码
    tableReg = re.compile(r'<table.*?</table>', re.S)
    tableTransfer = tableReg.findall(htmlContent)  # 保存的表格
    for n in range(len(tableTransfer)):
        htmlContent = tableReg.sub("[[" + str(n) + "]]", htmlContent, 1)
    reg = r'</?(.+?)>'
    reObject = re.compile(reg)
    revisedContent = reObject.sub("", htmlContent)
    space=r'&nbsp;?'
    revisedContent=re.sub(space,"",revisedContent)
    '''
       还原表格
       '''
    regTableInsert = re.compile(r'\[\[\d+\]\]')
    for tableNum in range(len(tableTransfer)):
        revisedContent = regTableInsert.sub(tableTransfer[tableNum], revisedContent, 1)
    # '''
    # 还原图片
    # '''
    # regNInsert = re.compile(r'@@\d+@@')
    # revisedContent = regNInsert.sub("<h3></h3>", revisedContent)
    return revisedContent

#将结果写入新文件
def writeAnswerInAnotherTxt(result):
    try:
        results = open('results.txt', 'wt',encoding='UTF-8')
        results.write(result)
        results.close()
    except Exception as e:
        print(str(e) + "\n文件写入失败")
        return 0

#删除无效空行
def deleteNull():
    try:
        haveNullTxt = open('results.txt', 'rt',encoding='UTF-8')
        lines = haveNullTxt.readlines()
        n = len(lines)
        label = []
        for i in range(n):
            if lines[i] == '\n':
                label.append(i)
        reversedLabel = label[::-1]
        for elem in reversedLabel:
            lines.pop(elem)
        strings = "".join(lines)
        try:
            results = open('results.txt', 'wt',encoding='UTF-8')
            results.write(strings)
            results.close()
        except Exception as e:
            print(str(e) + "\n文件写入失败")
            return 0
    except Exception as e:
        print("文件不存在\n")
        print(e)
        return 0

def AIJudgeHAndLeaveImage(halfDone):
    autoFile = open("autoFile.txt", "wt", encoding='UTF-8')
    autoFile.write(halfDone)
    autoFile.close()
    autoFile = open("autoFile.txt", "rt", encoding='UTF-8')
    clear = open("titledResults.txt", "wt", encoding="UTF-8")
    clear.close()
    reg = re.compile(r'(.*?[：|、|:]?\w+\n$)', re.S)
    line = autoFile.readline()
    while line:
        print(line)
        success = reg.findall(line)
        print(success)
        if len(success) == 0:
            titled = open("titledResults.txt", "a", encoding="UTF-8")
            titled.write(line)
        else:
            title = "<h3>" + success[0] + "</h3>"
            newLine = reg.sub(title, line)
            titled = open("titledResults.txt", "a", encoding="UTF-8")
            titled.write(newLine)
        line = autoFile.readline()
    titled.close()
    titled = open("titledResults.txt", "rt", encoding="UTF-8")
    finalAI=titled.read()
    print(finalAI)
    titled.close()
    autoFile.close()
    return finalAI

#使用说明窗口
class authorWindow(QDialog):
    def __init__(self,parent=None):
        super(authorWindow, self).__init__(parent)
        self.setWindowTitle('使用说明&版本')
        if (random.randint(0, 1)):
            iconName = "icon1.png"
        else:
            iconName = "icon2.png"
        self.setWindowIcon(QIcon(iconName))
        self.resize(600, 400)
        self.title=QLabel("说明\ntips：这是一个处理带有html代码的小工具，此为最新版本为2.0Beta版。\n"
                          +"本版本较上版本界面以及功能有稍微改动，\n加入了批量替换文本、自动为文本添加三级标题（此为版本测试功能）等功能。\n"
                          +"本工具共有3个主要功能：\n"
                          +"1.剔除代码：\n"
                          +"剔除代码是去除文本段中多余的标签格式，并且保留表格，此功能又分为两个功能，保留图片不保留图片。\n"
                          +"使用步骤：将文本复制进文本框后选择按钮之一，就会跳出处理后的结果，并且在目录下生成results.txt文本。\n"
                          +"\n2.自动添加三级标题：\n本功能整合了第一个的所有功能的基础上添加了自动加三级标题的功能，此为侧式功能。\n"
                          +"使用步骤：与第一个相似。\n\n3.置换功能：\n如果想批量替换文本中的某些词语或者句子，可以使用本功能。（支持正则搜索替换）\n"
                          +"使用步骤：建议使用此功能前，先使用上方两个功能进行处理。\n左边的置换按钮是直接将处理过的文本进行替换，即自动打开上面功能中生成的txt文件处理，不需要将内容复制。\n"
                          +"右边的置换按钮是将文本复制到文本框，然后操作文本框的内容，并且弹出新的txt文件。\n"
                          +"\n在使用中有任何bug或者建议可以发送email:1349281263@qq.com\n\n"
                          +"本软件的版权归作者所有。\nCopyright 2019 史经伟 All rights Reserved.",self)
        self.title.adjustSize()
        self.verticalLayout=QVBoxLayout()
        self.verticalLayout.addWidget(self.title)


#窗口函数
class TextEditDemo(QWidget):
    def __init__(self,parent=None):
        super(TextEditDemo, self).__init__(parent)
        self.setWindowTitle('clear unnecessary html code')
        if(random.randint(0,1)):
            iconName="icon1.png"
        else:
            iconName="icon2.png"
        self.setWindowIcon(QIcon(iconName))
        #定义窗口的初始大小
        self.resize(494.4,750)
        #创建多行文本框
        self.textEdit=QTextEdit()
        self.textEdit.setPlaceholderText("请复制将要操作的文章！")
        #创建按钮
        self.btnPress=QPushButton('剔除代码（保留图片）')
        self.btnPress2=QPushButton('剔除代码（不保留图片）')
        self.btnPress3=QPushButton('置换（置换刚刚生成结果内容不需文本输入）')
        self.btnPress4=QPushButton('关于QTS 2.0 BETA')
        self.btnPress5=QPushButton('置换（置换文本框内内容需文本输入）')
        self.autoTitle=QPushButton('【测试版功能】剔除同时AI判断标题（自动三级标题，保留图片）')
        self.autoTitle1 = QPushButton('【测试版功能】剔除同时AI判断标题（自动三级标题，不保留图片）')
        #创建用来接受用户输入的一个文本框
        self.inputName = QLineEdit()
        self.inputName.setPlaceholderText("输入你想替换的原文(支持正则表达式）")
        self.inputContent=QLineEdit()
        self.inputContent.setPlaceholderText("输入你替换的内容")

        #主垂直布局
        mainLayout=QVBoxLayout()

        #局部水平布局 按钮1
        littleLayout=QHBoxLayout()
        #局部水平布局 按钮2
        horizontalLayout=QHBoxLayout()
        #局部水平布局 按钮3
        horizontalLayout3=QHBoxLayout()
        #局部垂直布局 1
        aboutLayout=QVBoxLayout()
        #局部垂直布局 2
        partlyVLayout=QVBoxLayout()

        little=QWidget()
        verticalLay1=QWidget()
        partlyVLayout1=QWidget()
        horizontal2=QWidget()
        horizontal3=QWidget()

        #相关控件添加到垂直布局中
        aboutLayout.addWidget(self.btnPress4)
        aboutLayout.addWidget(self.textEdit)
        littleLayout.addWidget(self.btnPress)
        littleLayout.addWidget(self.btnPress2)
        partlyVLayout.addWidget(self.inputName)
        partlyVLayout.addWidget(self.inputContent)
        horizontalLayout.addWidget(self.btnPress3)
        horizontalLayout.addWidget(self.btnPress5)
        horizontalLayout3.addWidget(self.autoTitle)
        horizontalLayout3.addWidget(self.autoTitle1)

        verticalLay1.setLayout(aboutLayout)
        little.setLayout(littleLayout)
        partlyVLayout1.setLayout(partlyVLayout)
        horizontal2.setLayout(horizontalLayout)
        horizontal3.setLayout(horizontalLayout3)

        mainLayout.addWidget(verticalLay1)
        mainLayout.addWidget(little)
        mainLayout.addWidget(horizontal3)
        mainLayout.addWidget(partlyVLayout1)
        mainLayout.addWidget(horizontal2)

        #设置布局
        self.setLayout(mainLayout)
        #将按钮的点击信号与相关的槽函数进行绑定，点击即触发
        self.btnPress.clicked.connect(self.btnPress_clicked)
        self.btnPress2.clicked.connect(self.btnPress2_clicked)
        self.btnPress3.clicked.connect(self.btnPress3_clicked)
        self.btnPress4.clicked.connect(self.btnPress4_clicked)
        self.btnPress5.clicked.connect(self.btnPress5_clicked)
        self.autoTitle.clicked.connect(self.autoTitle_clicked)
        self.autoTitle1.clicked.connect(self.autoTitle1_clicked)

    def btnPress_clicked(self):
        if self.textEdit.toPlainText()=="":
            QMessageBox.warning(self, "错误", "您好,请输入待处理的文本！", QMessageBox.Yes)
            return 0
        writeAnswerInAnotherTxt(self.getContent())
        if (deleteNull() != 0):
            #os.system("results.txt")
            self.textEdit.clear()
            cmd = 'results.txt'
            res = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def btnPress2_clicked(self):
        if self.textEdit.toPlainText()=="":
            QMessageBox.warning(self, "错误", "您好,请输入待处理的文本！", QMessageBox.Yes)
            return 0
        writeAnswerInAnotherTxt(self.getNoImageContent())
        if (deleteNull() != 0):
            #os.system("results.txt")
            self.textEdit.clear()
            cmd = 'results.txt'
            res = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def btnPress3_clicked(self):
        try:
            afterFile=open("results.txt","rt",encoding='UTF-8')
            results=afterFile.read()
            afterFile.close()
            if self.inputName.text()=="":
                QMessageBox.warning(self, "错误", "您好，规则不能为空！", QMessageBox.Yes)
                return 0
            else:
                needBeSub=self.inputName.text()
                needBeSub=r''+needBeSub
                print("正则表达式：\n"+needBeSub)
                youNeedContent=self.inputContent.text()
                print("你需要改的：\n"+youNeedContent)
                complete,tableTransfer,savedH,imageCrash=saveUsefulInformation(results)
                needBeSub=re.compile(needBeSub)
                complete=needBeSub.sub(youNeedContent,complete)
                # 还原图片
                complete = backUsefulInformation(complete,tableTransfer,savedH,imageCrash)
                subFile=open("subResults.txt","w",encoding='UTF-8')
                subFile.write(complete)
                subFile.close()
                cmd = 'subResults.txt'
                res = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                return 1
        except Exception as e:
            QMessageBox.warning(self, "错误", "您好，未找到目录下的results.txt文件或者正则出错，请您使用上一个功能后再使用本工具！", QMessageBox.Yes)
            return 0

    def btnPress4_clicked(self):
        self.author=authorWindow()
        self.author.show()

    def btnPress5_clicked(self):
        try:
            if self.inputName.text()=="":
                QMessageBox.warning(self, "错误", "您好，规则不能为空！", QMessageBox.Yes)
                return 0
            else:
                results=self.textEdit.toPlainText()
                needBeSub = self.inputName.text()
                needBeSub = r'' + needBeSub
                print("正则表达式：\n" + needBeSub)
                youNeedContent = self.inputContent.text()
                print("你需要改的：\n" + youNeedContent)
                complete, tableTransfer, savedH, imageCrash = saveUsefulInformation(results)
                needBeSub = re.compile(needBeSub)
                complete = needBeSub.sub(youNeedContent, complete)
                # 还原图片
                complete = backUsefulInformation(complete, tableTransfer, savedH, imageCrash)
                subFile = open("subResults.txt", "w", encoding='UTF-8')
                subFile.write(complete)
                subFile.close()
                cmd = 'subResults.txt'
                res = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                return 1
        except Exception as e:
            QMessageBox.warning(self, "错误", "您好，字符串中可能有未识别的编码，主要原因：正则错误！", QMessageBox.Yes)
            return 0

    def autoTitle_clicked(self):
        if self.textEdit.toPlainText()=="":
            QMessageBox.warning(self, "错误", "您好,请输入待处理的文本！", QMessageBox.Yes)
            return 0
        halfDone=self.getContent()
        done=AIJudgeHAndLeaveImage(halfDone)
        try:
            results = open('results.txt', 'wt', encoding='UTF-8')
            results.write(done)
            results.close()
        except Exception as e:
            print(str(e) + "\n文件写入失败")
            return 0
        if (deleteNull() != 0):
            self.textEdit.clear()
            cmd = 'results.txt'
            res = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def autoTitle1_clicked(self):
        if self.textEdit.toPlainText() == "":
            QMessageBox.warning(self, "错误", "您好,请输入待处理的文本！", QMessageBox.Yes)
            return 0
        halfDone = self.getNoImageContent()
        done = AIJudgeHAndLeaveImage(halfDone)
        try:
            results = open('results.txt', 'wt', encoding='UTF-8')
            results.write(done)
            results.close()
        except Exception as e:
            print(str(e) + "\n文件写入失败")
            return 0
        if (deleteNull() != 0):
            self.textEdit.clear()
            cmd = 'results.txt'
            res = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

    def getContent(self):
        needToBeTreated=self.textEdit.toPlainText()
        done=deleteHtmlCode(needToBeTreated)
        return done

    def getNoImageContent(self):
        needToBeTreated = self.textEdit.toPlainText()
        needToBeTreated = deleteHtmlCodeAndImage(needToBeTreated)
        return needToBeTreated
        print(needToBeTreated)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=TextEditDemo()
    win.show()
    sys.exit(app.exec_())