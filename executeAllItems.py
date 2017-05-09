# -*- coding: utf-8 -*-
from selenium import webdriver
import string
from sys import argv
import sys
import time
import expand

web = "https://crs.sap.corp/#nav-tesi-1407732425578"
#web="https://crs.sap.corp/#nav-tesi-1403505865160"
print "The testing web: ", web

TesiTable = 'oTesiTable-table'
CommonParNode = 'oTesiTable-rows-row'
CommonChiNode = '-col'

IFrame = 'contentIFrame'
TreeClassName = 'sapUiTableCell'
TreeTagName = 'span'
ButtonTagName = 'img'
nodeTagName = 'label'
browser = webdriver.Chrome()
browser.get(web)
time.sleep(1)
browser.maximize_window()
time.sleep(1)
browser.switch_to_frame(IFrame)

node = browser.find_element_by_id(TesiTable)
TableLen = node.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
LenTable=len(TableLen)
#resDict=expand.expandTreeOne(TableLen,browser,["Chinwe","Backup"],2)
#expand and show all items
res=expand.checkSta(browser,"Setup NetWeaver with Base ASE","1480472686382",TableLen)
resDict=expand.expandTree(TableLen,browser)
#expand.saveData(resDict,'nodeTree.pkl')
#expand.displayItem(resDict)

#executeName=expand.loadData("executeName.txt")
#expand.execute(TableLen,browser,executeName,1)
#allResHis=[]
#for line in TableLen:
#    resHis=expand.getHistory(line,browser)
#    if len(resHis)!=0:
#        allResHis.append(resHis)
allres=expand.getLog(browser,TableLen)
expand.sendEmail(allres)




