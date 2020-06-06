import os, sys, glob, time, statistics
from datetime import datetime
#Tornado Imports
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
'''
Tizen App Connector Server (Uses Tornado to serve requests.)
''' 
#filename Hou:{ROP_NAME}:{LOCATION}:{NAME_OF_SEQUENCE}:{FRAME_RANGE}
#Global Vars
#Point this variable to directory of the '.echo' files provided (Assoc Folder).
echo_file = os.path.join("PATH_HERE")

#########################################################################################################
class WSHandler(tornado.websocket.WebSocketHandler):  

    def open(self):
        print ('New Connection Acquired.')
    
    def on_message(self, message):
        print ('Message Received: %s' % message)
        msgB = processRequest(message)
        print ('Sending back message: %s' % msgB)
        self.write_message(msgB)
        print("Message Sent!")

    def on_close(self):
        print ('Connection Closed. \n')
 
    def check_origin(self, origin):
        return True
########################################################################################
def processRequest(reqStr):
    #Main Control of Request.

    #Set Target File based on request string
    if reqStr == "HtoA":
        tarFile = os.path.join(echo_file + "\Hou_arnold.echo")
    elif reqStr == "MtoA":
        tarFile = os.path.join(echo_file + "\Maya_arnold.echo")
    elif reqStr == "mantra":
        tarFile = os.path.join(echo_file + "\Hou_mantra.echo")
    elif reqStr == "RS_HOU":
        tarFile = os.path.join(echo_file + "\Hou_redshift.echo")
    elif reqStr == "RS_MAYA":
        tarFile = os.path.join(echo_file + "\Maya_redshift.echo")
    else:
        #Echo String if none is applicable.
        return reqStr

    #Call to Read File.
    fileContents = procFile(tarFile)
    #Check file contents are not empty of failed.
    if fileContents != "FAILED_FILE_OP" and fileContents != "FAILED_FILE_EMPTY":
        #Split File String.
        split_char = "?"
        split_file = fileContents.split(split_char)

        #ROP
        rop = split_file[1]

        #Split Dir and File
        split_path = os.path.split(split_file[2])
        rndrLoc = split_path[0]
        rndrName = split_path[1]
        #Replace $F with an asterisk
        rndrName_pattern = rndrName.replace("$F","*")
        #Get Frames available and Average Delta List.
        framesFound, timeDelta = procDirTime(rndrLoc,rndrName_pattern)
        #Process Average Time from timeDelta
        if timeDelta:
            if framesFound != "0":
                averageTime = getAverageTime(timeDelta)
            else:
                averageTime = "??h ??m ??s"
        else:
            averageTime = "??h ??m ??s"

        #Frame Range
        frange = split_file[4]

        #Final String
        #msgB = (jname+":"+rop+":"+str(counter)+":"+frange+":"+avgStr)
        msgB = (rndrName + ":" +  rop + ":" + framesFound + ":" + frange + ":" + averageTime)
        return msgB 

    else:
        #If failed checks return 'null' string
        return "NULL:NULL:NULL:NULL:NULL"

def procFile(fileToRead):
    try:
        readFile = open(fileToRead, "r")
        fileContent = readFile.read()
        readFile.close()
        #return contents
        if fileContent != "":
            return fileContent
        else:
            return "FAILED_FILE_EMPTY"
    except:
        return "FAILED_FILE_OP"

def procDirTime(rndrLoc,filePattern):
    counter = 0
    lstDiff=[]
    print("Checking Files Dir...")
    try:
        for name in glob.glob(rndrLoc+"\\"+filePattern):
            #print(name)
            #increment Counter whjen File is found
            counter = counter + 1

            #Variables to store the time of creation and modification.
            created = time.ctime(os.path.getctime(name))
            modified = time.ctime(os.path.getmtime(name))
            #print(str(created), str(modified))

            #Split Larger sting into only Numbers and not days
            creatSplit = created.split(" ")[3]
            modSplit = modified.split(" ")[3]
            #print(str(creatSplit), str(modSplit))

            #Format of string for processing maths
            FMT = '%H:%M:%S'
            tdelta = datetime.strptime(modSplit, FMT) - datetime.strptime(creatSplit, FMT)
            #print(tdelta)

            #Append to the List of data.
            lstDiff.append(str(tdelta))

        #Return framesFound and the ListofDifference.
        counterStr = str(counter)
        return counterStr,lstDiff
    except:
        #Return framesFound and the ListofDifference.
        counterStr = str(counter)
        return counterStr,lstDiff

def getAverageTime(lstDiff):
    print("Calculating Average...")
    lstHr=[]
    lstMn=[]
    lstSc=[]
    for each in lstDiff:
        Hr = each.split(":")[0]
        lstHr.append(int(Hr))
        Mn = each.split(":")[1]
        lstMn.append(int(Mn))
        Sc = each.split(":")[2]
        lstSc.append(int(Sc))

    avHr = int(statistics.mean(lstHr))
    avMn = int(statistics.mean(lstMn))
    avSc = int(statistics.mean(lstSc))
    avgStr = str(avHr)+"h "+str(avMn)+"m "+str(avSc)+"s"
    return avgStr

######################################################################################## 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    #ADDR = '0.0.0.0'
    PORT = 8899
    http_server.listen(PORT)
    myIP = socket.gethostbyname(socket.gethostname())
    print('Project Tizen: Render Status Server')
    print('TORNADO PY3 ECHOPR TIZEN SERVER')
    print('Serving: ' + echo_file)
    print("Listening on Port:" + str(PORT))
    print('Websocket Server Started at %s' % myIP)
    print('Awaiting Connection... \n')
    tornado.ioloop.IOLoop.instance().start()
