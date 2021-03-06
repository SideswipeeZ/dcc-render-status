'''
    Tizen App (VER:1.0.0)
    Created by Bilal Malik.
    Contact:echopraxiavfx@gmail.com
    
    This allows the writing of parameters to file for the tizen tornado server.
    Currently in development.
    
    Code Partially Generated by PYQT-UI Generator Also on my Github.
'''
import os, sys, hou, re
#Location of Assets
app_location = os.path.join("PATH_HERE")
echo_file = os.path.join(app_location + "\Assoc")
#Add Path to Qt Module
sys.path.insert(0, hou.getenv('PYUI'))

#Qt Import Block 
from Qt import QtCore, QtWidgets, QtCompat , QtGui
from Qt.QtWidgets import QFileDialog

#global vars
supportedLst = ['arnold','ifd','Redshift_ROP']
nodeSel = []
wVars = ""
fType = ""

#Class Creation QT
class Tizn(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Tizn, self).__init__(parent, QtCore.Qt.WindowStaysOnTopHint)
        #File Interface File goes here
        file_interface = os.path.join(app_location+"\Assets\Tizen_Conn_V1.ui")
        self.mw = QtCompat.loadUi(file_interface)
        self.setCentralWidget(self.mw)
        #Set Window Title Here
        self.setWindowTitle("Tizen Connector 1.0.0 (Houdini)")
        stylesheet = hou.qt.styleSheet()
        self.setStyleSheet(stylesheet)
        #Set Windows Flags
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
                
        #Pixmap
        header = os.path.join(app_location+"\Assets\DDC_HEADER.png")
        pixmap = QtGui.QPixmap(header)
        self.mw.lbl_Header.setPixmap(pixmap)
        header2 = os.path.join(app_location+"\Assets\Tizen_header.png")
        pixmap2 = QtGui.QPixmap(header2)
        self.mw.lbl_headtext.setPixmap(pixmap2)  
        
                        
        #Button Assignment
        self.mw.bttn_node.clicked.connect(self.getNodeType)
        self.mw.bttn_write.clicked.connect(self.writeToFile)
        self.mw.bttn_reset.clicked.connect(self.resetAll)
        self.mw.bttn_help.clicked.connect(lambda: self.changePage(0))
        self.mw.bttn_returnMain.clicked.connect(lambda: self.changePage(1))
            #Read Buttons
        self.mw.bttn_readArnold.clicked.connect(lambda: self.getParm(0,'arnold'))
        self.mw.bttn_readMantra.clicked.connect(lambda: self.getParm(0,'ifd'))
        self.mw.bttn_readRedshift.clicked.connect(lambda: self.getParm(0,'Redshift_ROP'))
        
        #Params
        self.mw.bttn_write.setEnabled(False)
    
    def changePage(self, indexV):
        if indexV == 0:
            self.resetAll()
            self.mw.stackWidget.setCurrentIndex(0)
        elif indexV == 1:
            self.mw.stackWidget.setCurrentIndex(1)
        
    def resetAll(self):
        #Reset Vars
        my_window.resize(360,460)
        nodeSel = []
        wVars = ""
        fType = ""
        #Reset Labels
        self.mw.lbl_fileType.setText("Reading: ")
            #Read Labels
        self.mw.lbl_r_rop.setText("ROP: ")
        self.mw.lbl_r_loc.setText("Location: ")
        self.mw.lbl_r_name.setText("Name: ")
        self.mw.lbl_r_frange.setText("Frame Range: ")
            #Write Labels
        self.mw.lbl_w_rop.setText("ROP: ")
        self.mw.lbl_w_loc.setText("Location: ")
        self.mw.lbl_w_name.setText("Name: ")
        self.mw.lbl_w_frange.setText("Frame Range: ")        
        #Buttons
        self.mw.bttn_write.setEnabled(False)
        self.mw.bttn_node.setEnabled(True)
        
        
       #Start File Read.
    def getNodeType(self):
        global nodeSel
        nodeSel = hou.selectedNodes()[0]
        nodetypeName = nodeSel.type().name()
        self.mw.bttn_node.setEnabled(False)
        if nodetypeName in supportedLst:
            if nodetypeName == 'arnold':
                self.getParm(1,'arnold')
                self.mw.bttn_write.setEnabled(True)
            elif nodetypeName == 'ifd':
                self.getParm(1,'ifd')
                self.mw.bttn_write.setEnabled(True)
            elif nodetypeName == 'Redshift_ROP':
                self.getParm(1,'Redshift_ROP')
                self.mw.bttn_write.setEnabled(True)
        else:
            print("InValid Node")

    def getParm(self,flag,ropver):
        #Flag 1=Write aswell, 0=Read Only
        #Template to Follow. Hou:{ROP_NAME}:{LOCATION}:{NAME_OF_SEQUENCE}:{FRAME_RANGE}
        my_window.resize(360,760)
        #Read File from Disk or create one if it doesnt exist.
        #If exists and isnt empty populate read vars.
        if ropver == 'arnold':
            fStat = self.openFile('arnold')
        elif ropver == 'ifd':
            fStat = self.openFile('ifd')
        elif ropver == 'Redshift_ROP':
            fStat = self.openFile('Redshift_ROP')

        if fStat != "NEW_FILE":
            #Parse Items and populate
            splitArgs = fStat.split("?")
            #Populate Fields.
            self.mw.lbl_r_rop.setText("ROP: " + splitArgs[1])
            self.mw.lbl_r_loc.setText("Location: " + splitArgs[2])
            self.mw.lbl_r_name.setText("Name: " + splitArgs[3])
            self.mw.lbl_r_frange.setText("Frame Range: " + splitArgs[4])
        else:
            self.mw.lbl_fileType.setText("File Did not exist so it was created.")
            self.resetAll()
        #Get write paramters if flag is 1
        if flag == 1:
            #Get Write from node and populate vars
            #print(nodeSel.name())
            wRRname = nodeSel.name()
            self.mw.lbl_w_rop.setText("ROP: " + wRRname)
            
            #Location Parse
            if ropver == 'arnold':
                wRLoc = nodeSel.parm('ar_picture').eval()
                rawLoc = nodeSel.parm('ar_picture').unexpandedString()
            elif ropver == 'ifd':
                wRLoc = nodeSel.parm('vm_picture').eval()
                rawLoc = nodeSel.parm('vm_picture').unexpandedString()
            elif ropver == 'Redshift_ROP':
                wRLoc = nodeSel.parm('RS_outputFileNamePrefix').eval()
                rawLoc = nodeSel.parm('RS_outputFileNamePrefix').unexpandedString()

            if "$F" in rawLoc:
                repStr = "_FRAMENO_"
                fS = "$F"
                if "$F2" in rawLoc:
                    rawLoc = rawLoc.replace("$F2",repStr)
                    fS = "$F2"
                elif "$F3" in rawLoc:
                    rawLoc = rawLoc.replace("$F3",repStr)
                    fS = "$F3"
                elif "$F4" in rawLoc:
                    rawLoc = rawLoc.replace("$F4",repStr)
                    fS = "$F3"
                else:
                    rawLoc = rawLoc.replace("$F",repStr)
                    
                rawLoc = hou.expandString(rawLoc)
                rawLoc = rawLoc.replace(repStr,"$F")
                wRLoc = rawLoc  
            self.mw.lbl_w_loc.setText("Location: " + wRLoc)
            
            #Name Parse
            if ropver == 'arnold':
                wRName = os.path.basename(os.path.normpath(nodeSel.parm('ar_picture').eval()))
            elif ropver == 'ifd':
                wRName = os.path.basename(os.path.normpath(nodeSel.parm('vm_picture').eval()))
            elif ropver == 'Redshift_ROP':
                wRName = os.path.basename(os.path.normpath(nodeSel.parm('RS_outputFileNamePrefix').eval()))

            locName  = os.path.split(wRLoc)
            #print(locName[1])
            wRName = str(locName[1])
            self.mw.lbl_w_name.setText("Name: " + wRName)
            #Frame Range Parse
            wRRange = str(nodeSel.parm('f2').eval())
            self.mw.lbl_w_frange.setText("Frame Range: " + wRRange)

            #Final String
            global wVars
            wVars = "Hou?" + wRRname + "?" + wRLoc + "?" + wRName + "?" + wRRange

            
    #Open the File specified.
    def openFile(self,fileType):
        global fType
        #Set Target File
        if fileType == 'arnold':
            tarFile = os.path.join(echo_file + "\Hou_arnold.echo")
            fType = 'arnold'
        elif fileType == 'ifd':
            tarFile = os.path.join(echo_file + "\Hou_mantra.echo")
            fType = 'ifd'
        elif fileType == 'Redshift_ROP':
            tarFile = os.path.join(echo_file + "\Hou_redshift.echo")
            fType = 'Redshift_ROP'
        #print(tarFile)

        #File Parse
        if os.path.exists(tarFile) == True:
            rF = open(tarFile,"r")
            content = rF.read()
            if content != "":
                return content
            else:
                return "NEW_FILE"
        else:
            createFile = open(tarFile,"w")
            createFile.write("Maya?ROP?L:\ExoRec\tstR\file_$F.png?file_$F.png?240.0")
            createFile.close()
            ret = "NEW_FILE"
            return ret
            
            
    #Writes to File.
    def writeToFile(self):
        global wVars
        #Set Target File
        if fType == 'arnold':
            tarFile = os.path.join(echo_file + "\Hou_arnold.echo")
        elif fType == 'ifd':
            tarFile = os.path.join(echo_file + "\Hou_mantra.echo")
        elif fType == 'Redshift_ROP':
            tarFile = os.path.join(echo_file + "\Hou_redshift.echo")
        #print(tarFile)

        #File Parse
        if os.path.exists(tarFile) == True:
            wF = open(tarFile,"w")
            wF.write(wVars)
            wF.close()
            #self.mw.bttn_write.setEnabled(False)
            self.resetAll()
            self.mw.lbl_fileType.setText("FILE WRITTEN TO DISK")

        
isPanel = False
#Create the UI Block
if isPanel == True:
    #Create Interface Python Panel
    def onCreateInterface():
        my_window = Tizn()
        my_window.show()
        return my_window
elif isPanel == False:
    #Create Interface Shelf.
    try:
        my_window.close()
    except:
        pass
    my_window = Tizn()
    my_window.resize(360,460) #720
    my_window.show() 

