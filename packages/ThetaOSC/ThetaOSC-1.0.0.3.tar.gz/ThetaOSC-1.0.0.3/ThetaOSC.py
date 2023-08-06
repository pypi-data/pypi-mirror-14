#!python
#-*- coding:utf-8 -*-
"""
  A module to control Ricoh Theta-S based on OSC(Open Sperical Camera)API
  aka, Richo Theta API-2.
  https://developers.theta360.com/ja/docs/v2/api_reference/
  https://developers.google.com/streetview/open-spherical-camera/
"""
import traceback

import httplib
import urllib
import json
import struct
import os.path
import types
import thread
import struct
import time
import datetime
try:
    import  cv2, numpy
    opencv_available=True
except:
    opencv_available=False

class OscException(Exception):
    pass


_Options=(
    "aperture",
    "_captureInterval",
    "captureMode",
    "_captureNumber", # 0: limitless, 2<= _captureNumber <= 9999
    #"_dateTimeZone", # YYYY:MM:DD hh:mm:ss+(-)hh:mm
    "dateTimeZone", # YYYY:MM:DD hh:mm:ss+(-)hh:mm
    "exposureCompensation", #-2.0, -1.7, -1.3, -1.0, -0.7, -0.3, 0.0, 0.3, 0.7, 1.0, 1.3, 1.7, 2.0
    "exposureProgram", # 1: manual, 2: Normal, 4: shutterSpeed 9:ISO
    "fileFormat", #
    "_filter", # off: no filter, DR Comp: DR compensation, Noise Reduction:Noise Reduction
    "gpsInfo",
    "_HDMIreso", # L:1920x1080, M: 1280x720, S:720x480
    "iso", # 0: Auto, 100, 125, 160, 200, 250, 320, 400, 500, 640, 800, 1000, 1250, 1600
    "offDelay",  # 30 <= offDelay <= 1800, or 65535=Never
    "remainingPictures",
    "remainingSpace",
    "_remainingVideos",
    "shutterSpeed",
    "_shutterVolume",
    "sleepDelay", # 30 <= offDelay <= 1800, or 65535=Never
    "totalSpace",
    "whiteBalance",# auto/daylight/shade/cludy-daylight/icandescent/_warmWhiteFluorescent/_dayLightFluorescent/_dayWhiteFluorescent//fluorescent/_bulbFlowrescent
    "_wlanChannel", #0,1,6,11
)


class ThetaS:
    """
    class to control Richo Theta S model through OSC API over WiFi.
    Prevous models should use PTP-IP protocol.
    """
    port=80
    host="192.168.1.1"
    _jsonHeaders={
            "Content-type": "application/json;charset=utf-8",
            "Accept":"application/json",
        }

    def __init__(self):
        self.connection=httplib.HTTPConnection(self.host,self.port)
        self.commandInprogress=dict()
        self.sessionId=None
        self.stateFingerprint="FIG_0000"
        
    def __del__(self):
        self.closeSession()
        self.connection.close()
        self._finishWlan()

    def connect(self):
        """
        This method is left over from PTP-IP version. New user should use startSession() method 
        directory.
        """
        self.startSession()
        
    def Info(self):
        """
        Get basic information or supported functions on a camera.
        returns information as python dictionary.
        Input:
          None
        Output:
          manufacturer : name of the maker.
          model:    model number
          serialNumber: Serial number
          firmwareVersio: version of the firmware
          supportUrl: URL of the support web page.
          gps: Flag if the camera has GPS or not
          gyro: Flag indicates existence of a gyro
          uptime: seconds from start.
          api: list of supported APIs
          endpoints: information on Endpoint. as json object
        
        Endpoint:
          httpPort: port number for APIs.
          httpUpdatesPort: port number for CheckForUpdates.
        """
        self.connection.connect()
        self.connection.request("GET","/osc/info")
        res=self.connection.getresponse()
        self.connection.close()
        return json.loads(res.read())

    def State(self):
        """
        Input:       
        None.
        Output:
        Name 	        Type 	Description
        fingerprint 	String 	Current status ID         Obtain a unique value for each status
        state 	        Object 	Camera status (Details in the following item) 
        """
        self.connection.connect()
        self.connection.request("POST","/osc/state",None, ThetaS._jsonHeaders)
        res=self.connection.getresponse()
        self.connection.close()
        return json.loads(res.read())
        
    def CheckForUpdates(self,
                        stateFingerprint="",
                        waitTimeout=None):
        """
        Get status ID and check for the change of state.
        Input
          stateFingerprint: State ID
        Output
          steteFingerprint: current State ID
        """
        if waitTimeout:
            params=json.dumps(dict(stateFingerprint=stateFingerprint,
                                   waitTimeout=waitTimeout))
        else:
            params=json.dumps(dict(stateFingerprint=stateFingerprint))
            
        self.connection.connect()
        self.connection.request("POST",
                                "/osc/checkForUpdates",
                                params, ThetaS._jsonHeaders)
        res=self.connection.getresponse()
        self.connection.close()
        
        return json.loads(res.read())
        
    def _sendOscCommand(self,
                        oscCommand,
                        params,
                        headers= _jsonHeaders):
        self.connection.connect()
        self.connection.request("POST",
                                oscCommand,
                                params,
                                headers=headers)
        res=self.connection.getresponse()
        if res.status != 200:
            print (res.status, res.reason)
        self.connection.close()
        if res:
            rheaders=dict(res.getheaders())
            print (res.getheader("content-type"))
            if "json" in rheaders["content-type"]: # image/jpeg or video/mp4
                output=json.loads(res.read())
                if output["state"] == "done":
                    if output.has_key("id") and self.commandInprogress.has_key(output["id"]):
                        del self.commandInprogress[output["id"]]
                    if output.has_key("results"):
                        return output["results"]
                    else:
                        return True
                elif output["state"] == "inProgress":
                    self.commandInprogress[output["id"]]=output
                    return False
                else:
                    raise OscException("Command Execution Error %s"%output["error"])
            elif ("image" in rheaders["content-type"]) or ("video" in rheaders["content-type"]):
                return res.read()
            else:
                return res
        else:
            raise OscException("Command Execution Error:No response")
        
    def CommandStatus(self,id):
        """
        get status information on command execution.
        Input:
          id  command ID returned from Command/Execute request.
        Output: same as output from Commands/Execute
        """
        parms=json.dumps(dict(id="%s"%id))
        return self._sendOscCommand("/osc/commands/status", parms)
        
    def execute(self, command, parms={},
                headers={"Content-type": "application/json;charset=utf-8",
                         "Accept":"application/json"} ):
        """
        Executes a command in a commands category.
        Input
          name: name of the command
          parameters: parametes for the command.
        Output
          Returns one of results, error, or progess objects.
          name: name of executed command
          state: state of command execution. One of "done", "inProgress", "error"
          id: command ID
          result: result of command execution. returned on "done".
          error: error information. returned on "error".
          progress: progress status. returned on "inProgress"
        """
        parms=json.dumps(dict(name=command, parameters=parms))
        return self._sendOscCommand("/osc/commands/execute", parms, headers)

    # TheatOSC commands
    def startSession(self):
        """
        Start session and returns session ID.
        Input:
          None
        Output:
          sessionID  Unique session ID. Hold while power is ON. 
          timeout    seconds until the session expires
        """
        res=self.execute("camera.startSession")
        if res:
            self.sessionId=res["sessionId"]
            self.sessionTimeout=res["timeout"]
            return res
        else:
            raise OscException("Failed to start session")
    
    def updateSession(self):
        """
        Update session. Extend period of the session.
        Input:
          sessionId session ID returned beu startSession
        Output:
          sessionID sesseion ID
          timeout   session expiration time( 180 seconds)
        """
        res=self.execute("camera.updateSession",dict(sessionId=self.sessionId))
        self.sessionId=res["sessionId"]
        return res
        
    def closeSession(self):
        """
        Close session.
        Input:
          sessionID   session ID retured fro startSession.
        Output:
          None
        """
        res=self.execute("camera.closeSession",dict(sessionId=self.sessionId))
        self.sessionId=None
        return res

    def _finishWlan(self):
        """
        Turn off WLAN.
        Input:
          sessionID   session ID retured fro startSession.
        Output:
          None
        """
        res=self.execute("camera._finishWlan",dict(sessionId=self.sessionId))
        return res

    FinishWlan=_finishWlan
    
    def getOptions(self, optionNames=_Options):
        if (type(optionNames) in types.StringTypes):
            optionNames=[optionNames,]
        options=[opt for opt in optionNames if opt in _Options]
        if options:
            return self.execute("camera.getOptions",
                                dict(sessionId=self.sessionId,
                                     optionNames=options))
        else:
            raise OscException("Invalid Option name(s):%s"%optionNames)

    def setOptions(self, options):# type(options) == dict 
        invalid_options=[k for k in options.keys()
                         if unicode(k) not in _Options]
        for k in invalid_options:
            del options[k]
        print (options)
        return self.execute("camera.setOptions",
                            dict(sessionId=self.sessionId,
                                 options=options))
    def GetDateTime(self):
        """
        Current date and time information. Set by setOptions using phone’s date, time, and time zone.
        The format is, YYYY:MM:DD HH:MM:SS+(-)HH:MM.
        Time is in 24-hour format, date and time are separated by a blank space, andt
        ime zone is an offset from UTC time; for example, 2014:05:18 01:04:29+8:00 is China Time Zone (UTC+8:00)
        example:
        dev.setOptions({"dateTimeZone":"2016:04:06 21:06:55+09:00"})
        """
        return self.getOptions("dateTimeZone")

    def SetDateTime(self,datetimeToSet=None):
        if datetimeToSet is None:
            datetimeToSet = datetime.datetime.utcnow()
        if datetimeToSet.tzinfo is not None:
            # %z is replaced by the time zone offset from UTC; a leading plus sign stands for east of
            # UTC, a minus sign for west of UTC, hours and minutes follow with two digits each and
            # no delimiter between them (common form for RFC 822 date headers).
            timestring=datetimeToSet.strftime("%Y:%m:%d %H:%M:%S%z")
            timestring=":".join((timestring[:-2],timestring[-2:]))
        else:
            timestring=datetimeToSet.strftime("%Y:%m:%d %H:%M:%S+00:00")
        self.setOptions(dict(dateTimeZone=timestring))

        
    def InitiateCapture(self, storageId=0, objectFormatId=0):
        return self.takePicture()
                     
    def takePicture(self):
        res=self.execute("camera.takePicture",dict(sessionId=self.sessionId))
        return res
        
    def _startCapture(self):
        res=self.execute("camera._startCapture",dict(sessionId=self.sessionId))
        return res

    def _stopCapture(self):
        res=self.execute("camera._stopCapture",dict(sessionId=self.sessionId))
        return res
    #
    StopCapture=_stopCapture
    StartCapture=_startCapture

    def _stopSelfTimer(self):
        res=self.execute("camera._stopSelfTimer",dict(sessionId=self.sessionId))
        return res
    StopSelfTimer=_stopSelfTimer
    
    def listImages(self,entryCount=8, maxSize=160, includeThumb=True):
        res=self.execute("camera.listImages",
                         dict(
                             entryCount=entryCount,
                             maxSize=maxSize,
                             includeThumb=includeThumb))
        entries=res[u"entries"]
        print (entries[0]["uri"],type(entries),entryCount-len(entries),)
        while res.has_key(u'continuationToken'):
            res=self.execute("camera.listImages",
                             dict(
                                 entryCount=max(entryCount-len(entries),1),
                                 maxSize=maxSize,
                                 continuationToken=res[u'continuationToken'],
                                 includeThumb=includeThumb))
            entries.extend(res[u"entries"])
            print (entries[-1]["uri"])
        return entries
    
    def _listAll(self, entryCount=8, detail=True,sort="newest"):
        res=self.execute("camera._listAll",
                         dict(
                             entryCount=entryCount,
                             detail=detail,
                             sort=sort))
        entries=res[u"entries"]
        print (entries[0]["uri"],type(entries),entryCount-len(entries),)
        while res.has_key(u'continuationToken'):
            res=self.execute("camera._listAll",
                             dict(
                                 entryCount=max(entryCount-len(entries),1),
                                 continuationToken=res[u'continuationToken'],
                                 sort=sort))
            entries.extend(res[u"entries"])
            print (entries[-1]["uri"])
        return entries

    listAll=_listAll
    ListAll=_listAll
    
    def delete(self, fielUri):
        res=self.execute("camera.delete",
                         dict(fileUri=fileUri))
        return res
                         
    def getImage(self, fileUri, _type="thumb"):#_type:"thumb" or "full"
        res=self.execute("camera.getImage",
                         dict(fileUri=fileUri, _type=_type))
        dirs,fname=os.path.split(fileUri)
        if _type=="thumb":
            fn,ext=os.path.splitext(fname)
            fname =fn+"-thumb"+ext
        f=open(fname,"w")
        f.write(res)
        f.close()
        return True
    
    def _getVideo(self, fileUri, _type="full"): # _type:thumb or full
        res=self.execute("camera._getVideo",
                         dict(fileUri=fileUri, type=_type))
        dirs,fname=os.path.split(fileUri)
        if _type=="thumb":
            fn,ext=os.path.splitext(fname)
            fname =fn+"-thumb"+ext
        f=open(fname,"w")
        f.write(res)
        f.close()
        return True
    
    def _getLivePreview(self):
        """
        get live view of camera. Works only in still capture mode.
        operation on the device, starting capture, or change in capture mode
        will terminate transmission.

        Input:
          sessionID  Session ID taken in startSession.

        Output:
          Live view binary data in MotionJPEG format.
          transmitted in "Content-Type:multipart/x-mixed-replace"
          Equirectangular MotionJPEG　format 
        """
        if self.sessionId is None:
            raise OscException("session has not started yet.")
        
        res=self.execute("camera._getLivePreview",
                         dict(sessionId=self.sessionId))
        print (res.getheader("contnt-type"),res.getheaders())
        type=res.msg.type # 'multipart/x-mixed-replace'
        maintype=res.msg.maintype#multipart
        subtype=res.msg.subtype #x-mixed-replace
        plist=res.msg.plist#['boundary=--boundarydonotcross']
        return res

    GetVideo=_getVideo
    GetLivePreview=_getLivePreview
    
    def getMetadata(self, fileUri, ):
        """
        get metadata of a specified image.
        Input
          fileUri: file id of an image
        Output
          exif: Exif information in json format.
          xmp:  Photo Sphere XMP information.
        
        Remark
          Cannot use it while capturing video.
        """
        res=self.execute(
            "camera.getMetadata", dict(fileUri=fileUri) )
        return res
    #
    
    def SetCaptureMode(self,value):
        if (value not in ("image","_video","_liveStreaming")):
            raise OscException("Invaid apture Mode for THETA-S")
        return self.setOptions(dict(captureMode=value))

    def GetCaptureMode(self):
        return self.getOptions("captureMode")

    def SetStillMode(self):
        return self.setOptions(dict(captureMode="image"))

    def SetVideoMode(self):
        return self.setOptions(dict(captureMode="_video"))

    def SetFileFormat(self, filetype, width,height):
        return self.setOptions(
            dict(fileFormat=dict(type=filetype, width=width,height=height))
        )
        
    def SetTimelapseNumber(self, n):
        return self.setOptions(dict(_captureNumber=n))

    def SetTimelapseInterval(self, interval):# sec
        if not ( 5 < interval <3600):
            raise OscException("TimeLaspInterval Out-of-range")
        return self.setOptions(dict(_captureInterval=interval))

    def GetTimelapseNumber(self):
        return self.getOptions(["_captureNumber",])

    def GetTimelapseInterval(self):
        return self.getOptions(["_captureInterval",])

    def GetAndSaveObject(self,entry):
        print (entry)
        if entry.has_key(u"recordTime"):
            self._getVideo(entry["uri"],"thumb")
            self._getVideo(entry["uri"],"full")
        else:
            self.getImage(entry["uri"],"thumb")
            self.getImage(entry["uri"],"full")
                
    def GetAndSaveAllObjects(self):
        objects=self._listAll()
        for entry in objects:
            print (entry)
            self.GetAndSaveObject(entry)

def showLivePreview(dev):
    res=dev._getLivePreview()
    boundary=res.msg.plist[0].split("=")[1]
    f=os.fdopen(res.fileno(),"r")
    while not f.closed:
        nextline=f.readline()
        while (boundary not in nextline):
            nextline=f.readline()
        content_type=f.readline()
        content_size=f.readline()
        #print nextline, content_type,content_size
        f.readline() # skip over null line
        size=int(content_size.split(':')[1])
        size +=4
        raw=f.read(size)
        buf=numpy.array(struct.unpack("%dB"%size,raw),dtype=numpy.uint8)
        img=cv2.imdecode(buf, cv2.IMREAD_COLOR)
        #print size, len(img)
        cv2.imshow("preview", img)
        key=cv2.waitKey(20) & 0xff
        #print key
        if (key > 0) and (key == ord('q')):
            f.close()
        elif (key > 0) and (key == ord('p')):
            f.close()
            res.close()
            res=dev.takePicture()
            cid=res["id"]
            while res["state"] is "inProgress":
                res=dev.Status(id=cid)
                cv2.waitKey(500) # should be replaced with the routine to wait for the service
            res=dev._getLivePreview() 
            boundary=res.msg.plist[0].split("=")[1]
            f=os.fdopen(res.fileno(),"r")
        else:
            cv2.waitKey(20)
            continue
    f.close()
    res.close()
    return

def GettingStarted():
    dev=TheataS()
    dev.startSession()
    print "Session ID:",dev.sessionId

    options=dev.getOptions()
    print "Options:", options

    dev.setOptions(dict(
            fileFormat=dict(type="jpeg",
                            width=2048,
                            height=1024)
        ))

    print dev.getOptions()

    fingerprint=dev.CheckForUpdates("")["stateFingerprint"]
    
    print dev.takePicture()

    res=dev.CheckForUpdates(fingerprint)
    print "response:", res

    st=dev.State()
    print "status:",st

    dev.getImage(st["state"]["_latestFileUri"],"thumb") # get Thumbnail Image to file
    dev.getImage(st["state"]["_latestFileUri"],"full") # get Full Image to file

    dev.closeSession()
    
    

if __name__ == "__main__":
    dev=ThetaS()
    dev.startSession()
    dev.takePicture()
    dev.closeSession()
