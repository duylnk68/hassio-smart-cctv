from onvif import ONVIFCamera, ONVIFService
from zeep import transports
import zeep
import threading
import requests
import xmltodict
import time
import datetime

class Camera(transports.Transport, threading.Thread):
    IsMotion = False
    _SnapshotUri = None
    _Host = None
    _Port = None
    _User = None
    _Pwd = None
    _KeepRunning = True
    _PullMsgLimit = 1
    _PullMsgTimeout = datetime.timedelta(seconds=1)
    _TransportTimeout = 10
    
    def __init__(self, host, port, user, pwd):
        threading.Thread.__init__(self)
        transports.Transport.__init__(self, timeout=self._TransportTimeout, operation_timeout=self._TransportTimeout)
        self._Host = host
        self._Port = port
        self._User = user
        self._Pwd = pwd

        # Patch zeep.xsd.AnySimpleType.pythonvalue 
        zeep.xsd.AnySimpleType.pythonvalue = self._patched_zeep_pythonvalue

    # Work arround: NotImplementedError: AnySimpleType.pytonvalue() not implemented
    def _patched_zeep_pythonvalue(self, xmlvalue):
        return xmlvalue

    def post(self, address, message, headers):
        self.xml_request = message.decode('utf-8')
        response = super().post(address, message, headers)
        self.response = response
        return response

    def getSnapshotUri(self, cam: ONVIFCamera):
        media = cam.create_media_service()
        profiles = media.GetProfiles()
        mainProfile = media.GetProfile({'ProfileToken' : profiles[0].token})
        return media.GetSnapshotUri({'ProfileToken' : mainProfile.token})

    def _log(self, prefix, msg):
        print("[%c][%s:%d] - %s" % (prefix, self._Host, self._Port, msg))

    def CaptureImage(self):
        if self._SnapshotUri is None:
            return None
        else:
            return requests.get(self._SnapshotUri, auth=(self._User, self._Pwd)).content

    def _Loop(self):
        self._log('i', "Initializing...")
        cam = ONVIFCamera(self._Host, self._Port, self._User, self._Pwd, transport=self)
        self._log('i', "Getting Snapshot Uri...")
        self._SnapshotUri = self.getSnapshotUri(cam).Uri
        self._log('i', "Creating PullPoint Service...")
        pullpoint = cam.create_pullpoint_service()
        self._log('i', "The operation completed successfully!")
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
            self.IsMotion = "true" == simpleItemValue

    def run(self):
        while(self._KeepRunning):
            try:
                self._Loop()
            except:
                self._log('e', "Something wrong, please check log!")
                time.sleep(60)