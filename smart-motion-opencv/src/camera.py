from onvif import ONVIFCamera, ONVIFService
from zeep import transports
from requests.auth import HTTPDigestAuth
import zeep
import threading
import requests
import xmltodict
import time
import datetime

class Camera(transports.Transport, threading.Thread):
    _IsMotion = False
    _LastChanged = datetime.datetime.now()
    _IsReady = False
    _SnapshotUri = None
    _SnapshotUsr = None
    _SnapshotPwd = None
    _Host = None
    _Port = None
    _User = None
    _Pwd = None
    _KeepRunning = True
    _PullMsgLimit = 1
    _PullMsgTimeout = datetime.timedelta(seconds=1)
    _TransportTimeout = 10
    _Tag = None
    
    def __init__(self, host, port, user, pwd, snap_uri, snap_usr, snap_pwd, tag):
        threading.Thread.__init__(self)
        transports.Transport.__init__(self, timeout=self._TransportTimeout, operation_timeout=self._TransportTimeout)
        self._Host = host
        self._Port = port
        self._User = user
        self._Pwd = pwd
        self._Tag = tag
        if snap_uri is not None:
            self._SnapshotUri = "http://%s:%u/%s" % (host, port, snap_uri.lstrip('/'))
        if snap_usr is not None:
            self._SnapshotUsr = snap_usr
        else:
            self._SnapshotUsr = self._User
        if snap_pwd is not None:
            self._SnapshotPwd = snap_pwd
        else:
            self._SnapshotPwd = self._Pwd

    def post(self, address, message, headers):
        self.xml_request = message.decode('utf-8')
        response = super().post(address, message, headers)
        self.response = response
        return response

    @property
    def Hostname(self):
        return self._Host

    @property
    def IsReady(self):
        return self._IsReady

    @property
    def Tag(self):
        return self._Tag

    @property
    def IsMotion(self):
        return self._IsMotion

    @property
    def LastChanged(self):
        return self._LastChanged

    def getSnapshotUri(self, cam: ONVIFCamera):
        media = cam.create_media_service()
        profiles = media.GetProfiles()
        mainProfile = media.GetProfile({'ProfileToken' : profiles[0].token})
        return media.GetSnapshotUri({'ProfileToken' : mainProfile.token})

    def _log(self, prefix, msg):
        print("[%c][%s:%d] - %s" % (prefix, self._Host, self._Port, msg))

    def CaptureImage(self):
        try:
            if self._SnapshotUri is None:
                return None
            else:
                request_result = requests.get(self._SnapshotUri, auth=HTTPDigestAuth(self._SnapshotUsr, self._SnapshotPwd))
                if request_result.status_code is 200:
                    return request_result.content
                return None
        except:
            return None

    def _Loop(self):
        self._IsReady = False
        self._log('i', "Initializing...")
        cam = ONVIFCamera(self._Host, self._Port, self._User, self._Pwd, './wsdl/', transport=self)
        if self._SnapshotUri is None:
            self._log('i', "Getting Snapshot Uri...")
            self._SnapshotUri = self.getSnapshotUri(cam).Uri
        self._log('i', "Creating PullPoint Service...")
        pullpoint = cam.create_pullpoint_service()
        self._log('i', "The operation completed successfully!")
        self._IsReady = True
        while(True):
            # Pull message!
            pullpoint.PullMessages({"Timeout":self._PullMsgTimeout, "MessageLimit":self._PullMsgLimit})
            
            # Convert response message into a dictionary!
            msg = xmltodict.parse(cam.transport.response.text)
            
            # Get Envelope node!
            nodeEnvelope = msg.get("env:Envelope")
            if nodeEnvelope is None:
                self._log('e', "ONVIF service response invalid data!")
                raise Exception('env:Envelope not found!')
            
            # Get Body node!
            nodeBody = nodeEnvelope.get("env:Body")
            if nodeBody is None:
                continue
            
            # Get PullMessagesResponse node!
            nodePullMessagesResponse = nodeBody.get("tev:PullMessagesResponse")
            if nodePullMessagesResponse is None:
                continue
            
            # Get NotificationMessage node!
            nodeNotificationMessage = nodePullMessagesResponse.get("wsnt:NotificationMessage")
            if nodeNotificationMessage is None:
                continue
            
            # Get Message node!
            nodeMessage = nodeNotificationMessage.get("wsnt:Message")
            if nodeMessage is None:
                continue
            nodeMessage = nodeMessage.get("tt:Message")
            if nodeMessage is None:
                continue
            
            # Get Data node!
            nodeData = nodeMessage.get("tt:Data")
            if nodeData is None:
                continue
            
            # Get SimpleItem node!
            nodeSimpleItem = nodeData.get("tt:SimpleItem")
            if nodeSimpleItem is None:
                continue
            
            # Get SimpleItem's name!
            simpleItemName = nodeSimpleItem.get("@Name")
            if simpleItemName != "IsMotion":
                continue
            
            # Get SimpleItems's value!
            simpleItemValue = nodeSimpleItem.get("@Value")
            if simpleItemValue is None:
                continue

            # Update self.IsMotion
            motionStatus = "true" == simpleItemValue
            if motionStatus != self._IsMotion:
                self._IsMotion = motionStatus
                self._LastChanged = datetime.datetime.now()

    def run(self):
        while(self._KeepRunning):
            try:
                self._Loop()
            except:
                self._log('e', "Something wrong, please check log!")
                time.sleep(60)