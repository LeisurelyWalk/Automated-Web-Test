from selenium import webdriver
import string
from sys import argv
import sys
import time
import pickle


#The attribute class of any line. it includes some values, name,id and so on.
#len : the size of title, if the title is empty, len will be zero.
#Name : the name of the item.
#ID : the id of this item.
#IsAbled : show if the item is abled. some items may be enabled though they are in TISI system.
#StaEx : the status of any item, include "ERROR" "ok" "RUN"
#TItleName : the TiTleName of this item,include name, id,ip
#Type : the type attribute of this line.

class Attribute(object):
    len=0
    Name=""
    ID=""
    IsAbled=""
    StaEx=""
    IP=""
    TitleName=""
    Type=""
    def __init__(self,l=0,name="",id="",isabled="",staex="",ip="",title="",type=""):
        self.len=l
        self.Name=name
        self.ID=id
        self.IsAbled=isabled
        self.StaEx=staex
        self.IP=ip
        self.TitleName=title
        self.Type=type


#Initialization function
# #input : the web address
#return : the chrome driver and the table that contain all item.

def initTest(web= "https://crs.sap.corp/#nav-tesi-1407732425578"):
    from selenium import webdriver
    import string
    from sys import argv
    import sys
    import time

    #web = "https://crs.sap.corp/#nav-tesi-1407732425578"
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
    LenTable = len(TableLen)
    return browser,TableLen


#Get the Attribute of any line in the window body.
#input : the any line.
#return : the attribute class of the line.

def getAtrribute(line):
    Title = line.find_element_by_tag_name('label').get_attribute('title')
    if(len(Title)==0):
        att=Attribute(0)
        return att
    else:
        name=Title[Title.find("Name")+6:Title.find("Type")-1]
        Type=Title[Title.find("Type")+6:Title.find("IP")]
        CurId = Title[4:Title.find("Name") - 1]
        Abled=line.find_element_by_tag_name('label').get_attribute('class')
        Abled=Abled[:Abled.find(' ')]
        Static = line.find_elements_by_tag_name('td')
        CurStatic = Static[1].find_element_by_tag_name('img').get_attribute('title')
        isrunning=Static[1].find_element_by_tag_name('img').get_attribute('src')
        if(isrunning[-3:]=="gif"):
            CurStatic="RUN"
        hostName=Static[4].find_element_by_tag_name('a').get_attribute('textContent')
        att=Attribute(len(Title),name,CurId,Abled,CurStatic,hostName,Title,Type)
        return att


#expand a folder.
#table : the table that contain all item
#bro : the chrome driver
#name : the folder name
#sd : the deph of this folder.
#return : the Titlename of those items in this folder.
def expandTreeOne(Table,bro,name,sd):
    ornum = bro.find_element_by_id('oTesiTable-ariacount')
    str = ornum.get_attribute('textContent')
    sumCount = string.atoi(str[0:str.find(' ')])
    sumTable=[]
    myTable=[]
    curCount=0
    dragNum=0
    flag=0

    while (sumCount > curCount):
        for i in range(0, len(Table), 1):
            nodeStatic = Table[i].find_element_by_tag_name('span')
            nodeStaticStr = nodeStatic.get_attribute('class')
            nodeStaticStr = nodeStaticStr[len(nodeStaticStr) - 6:len(nodeStaticStr)]

            distanceStr = nodeStatic.get_attribute('style')
            distanceStr = distanceStr[distanceStr.find(':') + 2:-3]
            distance = string.atoi(distanceStr)


            Title = Table[i].find_element_by_tag_name('label').get_attribute('title')
            allTitle = Title.replace('\n', ' ')
            # allTitle=replaceNRT(Title)
            strattr = getAtrribute(Table[i])
            allTitle = allTitle + "IP: " + strattr.IP
            nodeNameTag = "%s %d" % (allTitle, distance / 17)
            if nodeNameTag in sumTable:
                continue

            if (strattr.Name == name[-1]):
                flag=1
                nodeStatic.click()
                time.sleep(5)
            elif (flag==0 and distance < sd*17 and nodeStaticStr == 'Closed' and strattr.Name in name):
                nodeStatic.click()
                time.sleep(5)
            elif(flag ==1 and distance > sd*17 and nodeStaticStr == 'Closed'):
                nodeStatic.click()
                time.sleep(5)
            elif (flag ==1 and  distance <= sd*17 and strattr.Name != name[-1]):
                flag=0


            if nodeNameTag not in sumTable:
                sumTable.append(nodeNameTag)
                curCount = curCount + 1
            if(flag==1):
                myTable.append(nodeNameTag)

        ornum = bro.find_element_by_id('oTesiTable-ariacount')
        str = ornum.get_attribute('textContent')
        sumCount = string.atoi(str[0:str.find(' ')])
        if (sumCount > curCount):
            dragNum = dragNum + 650
            bro.execute_script("var q=document.getElementById('oTesiTable-vsb-sb').scrollTop=%d" % dragNum)
            time.sleep(2)

    return myTable

#table : the table that contain all item
#bro : the chrome driver
#name : the folder name
#sd : the deph of this folder.
#Returns whether the file is running
def getAttrOfFolder(Table, bro, name, sd,id):
    ornum = bro.find_element_by_id('oTesiTable-ariacount')
    str = ornum.get_attribute('textContent')
    sumCount = string.atoi(str[0:str.find(' ')])
    sumTable = []
    myTable = []
    curCount = 0
    dragNum = 0
    flag = 0
    isRun=0
    isBreak=0
    while (sumCount > curCount):
        for i in range(0, len(Table), 1):
            nodeStatic = Table[i].find_element_by_tag_name('span')
            nodeStaticStr = nodeStatic.get_attribute('class')
            nodeStaticStr = nodeStaticStr[len(nodeStaticStr) - 6:len(nodeStaticStr)]

            distanceStr = nodeStatic.get_attribute('style')
            distanceStr = distanceStr[distanceStr.find(':') + 2:-3]
            distance = string.atoi(distanceStr)

            Title = Table[i].find_element_by_tag_name('label').get_attribute('title')
            allTitle = Title.replace('\n', ' ')
            # allTitle=replaceNRT(Title)
            strattr = getAtrribute(Table[i])
            allTitle = allTitle + "IP: " + strattr.IP
            nodeNameTag = "%s %d" % (allTitle, distance / 17)
            if nodeNameTag in sumTable:
                continue

            if (strattr.Name == name[-1] and id==strattr.ID):
                flag = 1
                if(nodeStaticStr == 'Closed'):
                    nodeStatic.click()
                    time.sleep(5)
            elif (flag == 0 and distance < sd * 17 and nodeStaticStr == 'Closed' and strattr.Name in name):
                nodeStatic.click()
                time.sleep(5)
            elif (flag == 1 and distance > sd * 17 and nodeStaticStr == 'Closed'):
                nodeStatic.click()
                time.sleep(5)
            elif (flag == 1 and distance <= sd * 17 and strattr.Name != name[-1]):
                flag = 0
                isBreak=1
                break
            if nodeNameTag not in sumTable:
                sumTable.append(nodeNameTag)
                curCount = curCount + 1
            if (flag == 1):
                myTable.append(nodeNameTag)
                if(strattr.StaEx=="RUN"):
                    isRun=1
                    isBreak=1
                    break

        if(isBreak==1):
             break

        ornum = bro.find_element_by_id('oTesiTable-ariacount')
        str = ornum.get_attribute('textContent')
        sumCount = string.atoi(str[0:str.find(' ')])
        if (sumCount > curCount):
            dragNum = dragNum + 650
            first=getAtrribute(Table[0]).Name
            bro.execute_script("var q=document.getElementById('oTesiTable-vsb-sb').scrollTop=%d" % dragNum)
            time.sleep(2)
            last=getAtrribute(Table[0]).Name
            if(first==last):
                isBreak=1
                break
    return isRun

#check if the line is running
#return the status

def checkIsRun(Table, bro,line):
    attr=getAtrribute(line)
    nodeStatic = line.find_element_by_tag_name('span')

    distanceStr = nodeStatic.get_attribute('style')
    distanceStr = distanceStr[distanceStr.find(':') + 2:-3]
    distance = string.atoi(distanceStr)
    distance=distance/17
    name=[attr.Name]
    isRun=getAttrOfFolder(Table,bro,name,distance,attr.ID)
    return isRun

#expand all line in the table.

def expandTree(Table,bro):
    ornum = bro.find_element_by_id('oTesiTable-ariacount')
    str = ornum.get_attribute('textContent')
    sumCount = string.atoi(str[0:str.find(' ')])
    sumTable=[]#add line to it.
    curCount=0#the nums we haved expanded.
    dragNum=0#control the scroll bar

    while (sumCount > curCount):
        for i in range(0,len(Table),1):
            nodeStatic = Table[i].find_element_by_tag_name('span')

            nodeStaticStr = nodeStatic.get_attribute('class')
            nodeStaticStr = nodeStaticStr[len(nodeStaticStr) - 6:len(nodeStaticStr)]

            distanceStr=nodeStatic.get_attribute('style')
            distanceStr=distanceStr[distanceStr.find(':') + 2:-3]
            distance=string.atoi(distanceStr)

            Title = Table[i].find_element_by_tag_name('label').get_attribute('title')
            allTitle=Title.replace('\n',' ')
            #allTitle=replaceNRT(Title)
            strattr=getAtrribute(Table[i])
            allTitle=allTitle+"IP: " + strattr.IP
            nodeNameTag="%s %d" %(allTitle,distance/17)
            Title = Title[Title.find('Name') + 6:Title.find('Type')-1]
            if nodeNameTag not in sumTable:
                sumTable.append(nodeNameTag)
                curCount=curCount+1

            if(nodeStaticStr=='Closed'):
                nodeStatic.click()
                time.sleep(5)

        ornum = bro.find_element_by_id('oTesiTable-ariacount')
        str = ornum.get_attribute('textContent')
        sumCount = string.atoi(str[0:str.find(' ')])
        if(sumCount > curCount):
            dragNum=dragNum+650
            bro.execute_script("var q=document.getElementById('oTesiTable-vsb-sb').scrollTop=%d" %dragNum)
            time.sleep(2)
    return sumTable

#dispaly all items.
def displayItem(tableList):
    for s in tableList:
        name=s[0:-2]
        num=string.atoi(s[-1])
        tempStr='\t'*num
        print "%s%s"%(tempStr,name)

#save data.
def saveData(dict,fileName):
    path="C:\Users\i336792\Documents\python\\"
    fileName=path+fileName
    output=open(fileName,'wb')
    pickle.dump(dict,output)
    output.close()
    fileTxt=fileName[:-3]+'txt'
    f=open(fileTxt,'wb')
    for s in dict:
        f.write(s[:-2] + "\n")
    f.close()


#the node that we need to set env.
#fileName show the var of enc, ID ,Name
class envNode(object):
    fileName=""
    ID=""
    Name=""

    def __init__(self,filen,id,n):
        self.Name=n
        self.fileName=filen
        self.ID=id


#we need to run the node.
class eNode(object):
    IP=""
    num=-1
    ID=""
    Name=""

    def __init__(self,ip,id,n,name):
        self.Name=name
        self.IP=ip
        self.num=n
        self.ID=id


#the node have these child node.
class node(object):
    env=envNode("","","")
    error=eNode("","","","")
    execu=eNode("","","","")

    def __init__(self,en,ex,er):
        self.error=er
        self.execu=ex
        self.env=en


#load data, dispaly == 1 print the data.
#we can get execute items consist of ID,Name,IP. error items consist of ID,IP,Name
#num: items with the same number cannot be executed at the same time
#env include the var of env.S
def loadData(filename):
    path = "C:\Users\i336792\Documents\python\\"+filename
    if(filename[-3:]=="txt"):
        items=[]

        execu=[]
        error=[]
        num=[]
        ENV=[]
        for line in open(path):
            if(line[1:4]=="NUM"):
                num.append(int(line[4:6]))
            elif(line[1:6]=="ERROR"):
                error.append(line[7:-1])
            elif(line[1:6]=="EXECU"):
                execu.append(line[7:-1])
            elif(line[1:6]=="ENVIR"):

                if(line[7:11]=="NULL"):
                    tpEnv=envNode("NULL","NULL","NULL")
                else:
                    str=line[7:-1]
                    id=str[4:str.find("Name")-1]
                    name=str[str.find("Name")+6:str.find("FileName")-1]
                    file=str[str.find("FileName")+9:]
                    tpEnv=envNode(file,id,name)
                ENV.append(tpEnv)
        exid,exname,exip=transform(execu)
        erid,ername,erip=transform(error)
        for i in range(0,len(num)):
            ex=eNode(exip[i],exid[i],num[i],exname[i])
            er=eNode(erip[i],erid[i],num[i],ername[i])
            item=node(ENV[i],ex,er)
            items.append(item)


        return items
    else:
        infile=open(path,'rb')
        data=pickle.load(path)
        infile.close()
        return data

# def loadData(filename,dispaly=1):
#     path = "C:\Users\i336792\Documents\python\\"+filename
#     if(filename[-3:]=="txt"):
#         execu=[]
#         error=[]
#         for line in open(path):
#             if(line[1:6]=="ERROR"):
#                 error.append(line.strip())
#             elif(line[1:6]=="EXECU"):
#                 execu.append(line.strip())
#         if (dispaly == 1):
#             for s in execu:
#                 print s
#         return execu,error
#     else:
#         infile=open(path,'rb')
#         data=pickle.load(path)
#         infile.close()
#         if (dispaly == 1):
#             for s in data:
#                 print s
#         return data


#transform data to get ID,IP,Name.
def transform(data):
    ID=[]
    IP=[]
    Name=[]
    for s in data:
        tempid=s[4:s.find("Name")-1]
        ID.append(tempid)
        tempName=s[s.find("Name")+6:s.find("Type")-1]
        Name.append(tempName)
        ip=s[s.find("IP")+4:]
        IP.append(ip)
    return ID,Name,IP


#search any item by Name.
def search(bro,name):
    YCom = bro.find_element_by_id(u'__field0')
    Sea=YCom.find_element_by_id(u'__field0-cb-input')
    Sea.clear()
    time.sleep(1)
    Sea.send_keys(name)
    time.sleep(1)
    YCom.find_element_by_tag_name('button').click()
    time.sleep(2)

#check the statuse of items by ID and Name.
def checkSta(bro,name,id,table):
    search(bro, name)
    res=0
    resSta=0

    for line in table:
        AttLine = getAtrribute(line)
        print AttLine.TitleName
        if (AttLine.len == 0):
            break
        CurId = AttLine.ID
        if (CurId != id):
            continue
        else:
            res=line
            resSta=AttLine.StaEx
            break
    AttLine = getAtrribute(res)
    if(AttLine.Type=="Folder"):
        resSta=checkIsRun(table,bro,res)
    return resSta

#execute any item.
#newStart==1, Start from the beginning
def executeItem(table,bro,name,id,ip,newStart):
        search(bro, name)
        for line in table:
            AttLine = getAtrribute(line)

            print AttLine.TitleName
            if (AttLine.len == 0):
                break
            CurId = AttLine.ID
            if (CurId != id):
                continue

            elif (AttLine.StaEx == 'NA' or AttLine.IsAbled == "disabled_action"):
                print "The file has been deleted!"
                break
            else:
                if(ip != AttLine.IP):
                    changeIP(line,bro,ip)

                ExecCom = line.find_elements_by_tag_name('td')
                # click excute
                ExecCom[5].find_element_by_tag_name('img').click()
                time.sleep(3)

                opt = bro.find_element_by_tag_name('html')
                opt1 = opt.find_element_by_class_name('sapUiBody')
                opt2 = opt1.find_element_by_id('sap-ui-static')

                if (AttLine.StaEx == "OK"):
                    opt3 = opt2.find_element_by_class_name('sapUiDlgFooter')
                    opt4 = opt3.find_element_by_class_name('sapUiDlgBtns')
                    opt5 = opt4.find_elements_by_tag_name('button')
                    OKorCan = raw_input(u"Please enter: (OK/ok or Cancel/cancel)")
                    if (OKorCan == 'OK' or OKorCan == 'ok'):
                        opt5[0].click()
                    else:
                        opt5[1].click()

                    time.sleep(3)
                elif (AttLine.StaEx == "ERROR"):
                    opt3 = opt2.find_element_by_id('oExecuteActionRBG').find_elements_by_tag_name('span')

                    print "Start from the beginning or Continue from the previous run."
                    Action = raw_input(u"Please enter: (start or continue)")
                    if (newStart == 0):
                        opt3[1].click()
                        time.sleep(3)
                    opt4 = opt2.find_element_by_class_name('sapUiDlgCont').find_elements_by_tag_name('button')
                    opt4[0].click()
                    time.sleep(3)
                break

#the main function. profileName: the profile file name.
def mainExecute(table,bro,profileName):
    items=loadData(profileName)
    curSta=[0]*len(items)#0inint 1run 2finished
    errSta=[0]*len(items)
    exSet=set()
    erSet=set()
    while(sum(curSta)==len(items)*2 and sum(errSta)==len(items)*2):
        for i in range(0,len(items)):
            item=items[i]
            if item.execu.num not in exSet and curSta[i]==0:
                if (item.env.ID != "NULL"):
                    setEnvbyName(bro,table,item.env.Name,item.env.ID,item.env.fileName)
                exSet.add(item.execu.num)
                executeItem(table,bro,item.execu.Name,item.execu.ID,item.execu.IP,1)
                curSta[i]=1
            elif(curSta[i]==1 and checkSta(bro,item.execu.Name,item.execu.ID,table)=="ERROR"):


                if(errSta[i]==0 and item.error.num not in erSet):
                    executeItem(table,bro,item.error.Name,item.error.ID,item.error.IP,1)
                    errSta[i]=1
                    erSet.add(item.error.num)
                elif(errSta[i]==1 and checkSta(bro,item.error.Name,item.error.ID,table)=="ERROR"):
                    print "install and uninstall are failed!!"
                    # exSet.remove(item.execu.num)
                    # if item.execu.num in erSet:
                    #     erSet.remove(item.execu.num)
                    errSta[i] = 2
                    curSta[i] = 2

                elif(errSta[i]==1 and checkSta(bro,item.error.Name,item.error.ID,table)=="OK"):
                    print "install is failed!!, uninstall is finished!"
                    exSet.remove(item.execu.num)
                    if item.execu.num in erSet:
                        erSet.remove(item.execu.num)
                    errSta[i] = 2
                    curSta[i] = 2

            elif(curSta[i]==1 and checkSta(bro,item.execu.Name,item.execu.ID,table)=="OK"):
                exSet.remove(item.execu.num)
                if item.execu.num in erSet:
                    erSet.remove(item.execu.num)
                errSta[i]=2
                curSta[i]=2



#newStart==1,Start from the beginning.  ==0,Continue from the previous run
def execute(table,bro,data,newStart):
    id,name,ip=transform(data)
    for i in range(0,len(name),1):
        executeItem(table,bro,name[i],id[i],ip[i],newStart)


# def mianExecute(table,bro,execu,error):
#     execute(table,bro,execu,1)
#     time.sleep(300)#Detect the status every five minutes
#     Eid,Ename,Eip=transform(error)
#     staList=[0]*len(error)
#     flag=1
#     ErrorStr=""
#     id,name,ip=transform(execu)
#     while(flag):
#         flag=0
#         for i in range(0,len(execu),1):
#             resSta=checkSta(bro,name[i],id[i],table)
#             if(resSta=="ERROR"):
#
#                 if(staList[i]==0):
#                     executeItem(table,bro,Ename[i],Eid[i],Eip[i],1)
#                     flag = 1
#                 elif(staList[i]==2):
#                     executeItem(table,bro,name[i],id[i],ip[i],1)
#                     staList[i]=0
#                     flag=1
#                 elif(staList[i]==3):
#                     ErrorStr+="ERROR Step: %s %s %s"%(Ename[i],id[i],ip[i])
#                     ErrorStr+="\n"
#                 else:
#                     flag=1
#
#                 time.sleep(5)
#
#                 ErrSta=checkSta(bro,Ename[i],Eid[i],table)
#                 resSta = checkSta(bro, name[i], id[i], table)
#                 if(ErrSta=="RUN"):
#                     staList[i]=1
#                 elif(ErrSta=="OK" and resSta !="RUN"):
#                     staList[i]=2
#                 elif(resSta=="RUN"):
#                     staList[i]=0
#                 else:
#                     staList[i]=3
#             elif(resSta=="RUN"):
#                 flag=1
#             else:
#                 continue
#         time.sleep(300)

#change ip of any item.
def changeIP(line,bro,ip):
    trTable = line.find_elements_by_tag_name('td')
    trTable[4].find_element_by_tag_name('a').click()
    time.sleep(3)
    NewBody = bro.find_element_by_tag_name('body')
    ipMain=NewBody.find_element_by_css_selector("div[role=\"Main\"]")
    ipContent = ipMain.find_element_by_css_selector("div[class=\"sapUiUx3TVFacetThingGroupContent\"]")
    iptbody=ipContent.find_element_by_tag_name('table').find_element_by_tag_name('tbody')
    iptr=iptbody.find_elements_by_tag_name('tr')
    iptd=iptr[1].find_elements_by_tag_name('td')
    ipChange=iptd[1].find_element_by_tag_name('input')
    ipChange.clear()
    time.sleep(1)
    ipChange.send_keys(ip)
    time.sleep(1)

    checkSaveAndClose=ipMain.find_elements_by_css_selector("li[class=\"sapUiUx3ActionBarItemRight\"]")
    saveAndClose=checkSaveAndClose[1]
    saveAndCloseSta=saveAndClose.find_element_by_tag_name('button').get_attribute('aria-disabled')
    if(saveAndCloseSta=="false"):
        saveAndClose.find_element_by_tag_name('button').click()
        time.sleep(1)
    else:
        checkSaveAndClose[3].find_element_by_tag_name('button').click()
        time.sleep(1)

#open history window.
def openHis(line):
    trTable = line.find_elements_by_tag_name('td')
    trTable[1].find_element_by_tag_name('img').click()
    time.sleep(3)

#close history window.
def closeHis(window):
    closeBtn=window.find_element_by_css_selector("a[id=\"oHistoryWindow-close\"]")
    closeBtn.click()
    time.sleep(2)

#get history execute message.
def getHisAtt(tr):
    attKeys=["Parent Folder","Step Name","Started At","Duration","Staus"]
    att={}
    hdden=tr.get_attribute('class')
    if(hdden.find("Hidden") == -1):
        td=tr.find_elements_by_tag_name('td')

        for i in range(1,6,1):
            attrTitle=td[i].find_element_by_tag_name('span').get_attribute('title')
            att[attKeys[i-1]]=attrTitle
    return att

#get history of any line.
def getHistory(line,bro):
    openHis(line)
    hisWindow = bro.find_element_by_css_selector("div[id=\"oHistoryWindow\"]")
    allHis = []
    att = getAtrribute(line)
    if(att.StaEx=="OK" or att.StaEx=="NA" or att.TitleName.find("Folder") ==-1):
        closeHis(hisWindow)
        return allHis
    histTable=hisWindow.find_element_by_css_selector("table[id=\"oHistoryTable-table\"]")
    hisTr=histTable.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

    for tr in hisTr:
        tempHis=getHisAtt(tr)
        if(len(tempHis)!=0):
            allHis.append(tempHis)

    closeHis(hisWindow)
    return allHis

#open console window.
def openConsole(tr):
    hdden=tr.get_attribute('class')
    if(hdden.find("Hidden") == -1):
        td=tr.find_elements_by_tag_name('td')
        consoleTd=td[7].find_element_by_tag_name('img')
        consoleTd.click()
        time.sleep(3)
        return 1
    else:
        return 0


#get console Log.
def getConLog(node):
    hisWin = node.find_element_by_tag_name('body').find_element_by_css_selector("div[id=\"historyLogOverlay\"]")
    hisName = hisWin.find_element_by_css_selector(u"div[id=\"historyLogLayout--top\"]").find_element_by_tag_name(
        'span').get_attribute('title')
    hisLog = hisWin.find_element_by_css_selector(u"div[id=\"historyLogLayout--center\"]").find_element_by_tag_name(
        'span').get_attribute('textContent')
    return hisName, hisLog


#close console window.
def closeCon(node):
    hisWin = node.find_element_by_tag_name('body').find_element_by_css_selector("div[id=\"historyLogOverlay\"]")
    hisBtn=hisWin.find_elements_by_css_selector("a[role=\"button\"]")
    hisBtn[1].click()
    time.sleep(3)


#save.
def saveLog(dic):
    fileName="C:\Users\i336792\Documents\python\Log.txt"
    f=open(fileName,'wb')
    for k,v in dic.items():
        f.write("**************************"*5+"\n")
        f.write("******"+k + "\n"*2)
        f.write(v+"\n"*3)
    f.close()


#get all Log of all error.
def getLog(bro,table):
    TesiTable = 'oTesiTable-table'
    node = bro.find_element_by_id(TesiTable)
    bro.execute_script("var q=document.getElementById('oTesiTable-vsb-sb').scrollTop=0")

    openHis(table[0])
    hisWindow = bro.find_element_by_css_selector("div[id=\"oHistoryWindow\"]")
    allHisLog = {}
    att = getAtrribute(table[0])
    if (att.StaEx == "OK" or att.StaEx == "NA" or att.TitleName.find("Folder") == -1):
        closeHis(hisWindow)
    else:
        histTable = hisWindow.find_element_by_css_selector("table[id=\"oHistoryTable-table\"]")
        hisTr = histTable.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
        for tr in hisTr:
            isOpen = openConsole(tr)
            execHis=getHisAtt(tr)
            str=[]
            for k, v in execHis.items():
                temp = k + ':' + v
                str.append(temp)
            strName=', '.join(str)

            if (isOpen == 1):
                hisName, hisLog = getConLog(bro)
                hisName=hisName+'  '+strName
                allHisLog[hisName]=hisLog
                closeCon(bro)
        saveLog(allHisLog)
    closeHis(hisWindow)
    return allHisLog

#send all message in the console window by email.
def sendEmail(content):
    import smtplib
    from email.mime.text import MIMEText
    str=""
    for k,v in content.items():
        str=str+ "\n"*2 + "**************"*5+"\n"
        str=str+k+"\n"*3+v

    mail_host = "smtp.163.com"
    mail_user = "kzhouxd@163.com"
    mail_pass = "zk521789"

    sender = 'kzhouxd@163.com'
    receivers = ['983704737@qq.com','kang.zhou01@sap.com','sean.jia@sap.com']


    title = 'TESI Execution History'
    message = MIMEText(str, 'plain', 'utf-8')
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("mail has been send successfully.")

#open envrionment window.
def openSetEnv(line):
    attrline=getAtrribute(line)
    if(attrline.len==0):
        return -1
    trTable = line.find_elements_by_tag_name('td')
    envDiv=trTable[6].find_elements_by_css_selector("div[class=\"sapUiHLayoutChildWrapper\"]")
    envSrc=envDiv[1].find_element_by_tag_name('img').get_attribute('src')
    if(envSrc[-9:-4]!='Empty'):
        envDiv[1].find_element_by_tag_name('img').click()
        time.sleep(3)
        return 1
    else:
        print "There is no data for the environment"
        return -1

#load var data of env.
def loadEnv(filename):
    path = "C:\Users\i336792\Documents\python\\"+filename
    dic={}
    for line in open(path):
        idex=line.find(':')
        dic[line[0:idex]]=line[idex+1:-1]
    return dic


#set these env.
def setEnv(line,bro,filename):
    flag=openSetEnv(line)
    if(flag==1):
        dic=loadEnv(filename)
        envMain = bro.find_element_by_css_selector("div[class=\"sapUiUx3TVContent\"]")
        closeEnv=envMain.find_element_by_css_selector("ul[class=\"sapUiUx3ActionBarBusinessActions\"]")
        closeBtn = closeEnv.find_elements_by_tag_name('li')
        envTable=envMain.find_element_by_css_selector("div[class=\"sapUiTableCtrlCnt\"]")
        envTbody=envTable.find_element_by_tag_name('tbody')
        envTr=envTbody.find_elements_by_tag_name('tr')
        for tr in envTr:
            envTd=tr.find_elements_by_tag_name('td')
            envTitle=envTd[1].find_element_by_tag_name('input').get_attribute('value')
            if envTitle in dic.keys():
                envIn=envTd[2].find_element_by_tag_name('input')
                envIn.clear()
                time.sleep(1)
                envIn.send_keys(dic[envTitle])
                time.sleep(1)
        closeFlag=closeBtn[1].find_element_by_tag_name('button').get_attribute(r"aria-disabled")
        if(closeFlag!="true"):
            btn=closeBtn[1].find_element_by_tag_name('button')
            btn.click()
            time.sleep(5)
        else:
            btn=closeBtn[1].find_element_by_tag_name('button')
            btn.click()

            btn = closeBtn[3].find_element_by_tag_name('button')
            btn.click()
            time.sleep(5)

#set env by name of item.
def setEnvbyName(bro,table,name,id,filename):
    search(bro, name)

    for line in table:
        AttLine = getAtrribute(line)
        print AttLine.TitleName
        if (AttLine.len == 0):
            break
        CurId = AttLine.ID
        if (CurId != id):
            continue
        else:
            setEnv(line,bro,filename)
            break


#save
def saveEnv(dic):
    fileName='env.txt'
    path = "C:\Users\i336792\Documents\python\\"
    fileName = path + fileName
    f = open(fileName, 'wb')
    for k,v in dic.items():
        f.write(k+':'+v+'\n')
    f.close()


#get enc var in TESI.
def getEnv(line,bro):
    flag = openSetEnv(line)
    dic = {}
    if (flag == 1):

        envMain = bro.find_element_by_css_selector("div[class=\"sapUiUx3TVContent\"]")
        closeEnv = envMain.find_element_by_css_selector("ul[class=\"sapUiUx3ActionBarBusinessActions\"]")
        closeBtn = closeEnv.find_elements_by_tag_name('li')
        envTable = envMain.find_element_by_css_selector("div[class=\"sapUiTableCtrlCnt\"]")
        envTbody = envTable.find_element_by_tag_name('tbody')
        envTr = envTbody.find_elements_by_tag_name('tr')
        for tr in envTr:
            envTd = tr.find_elements_by_tag_name('td')
            envTitle = envTd[1].find_element_by_tag_name('input').get_attribute('value')
            envValue=envTd[2].find_element_by_tag_name('input').get_attribute('value')
            dic[envTitle]=envValue

        closeFlag = closeBtn[1].find_element_by_tag_name('button').get_attribute(r"aria-disabled")
        if (closeFlag != "true"):
            btn = closeBtn[1].find_element_by_tag_name('button')
            btn.click()
            time.sleep(5)
        else:
            btn = closeBtn[1].find_element_by_tag_name('button')
            btn.click()

            btn = closeBtn[3].find_element_by_tag_name('button')
            btn.click()
            time.sleep(5)

        saveEnv(dic)
    return dic

