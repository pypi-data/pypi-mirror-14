# -*- coding: utf-8 -*-
#for documentation about the mqtt lib, check https://pypi.python.org/pypi/paho-mqtt/0.9
import paho.mqtt.client as mqtt                # provides publish-subscribe messaging support
import calendar                                # for getting the epoch time
from datetime import datetime                  # for json date time
import time                                    # gets the current time
import httplib                                 # for http comm
from socket import error as SocketError         # for http error handling
import errno                                    # for http error handling
import logging
import socket                                  # for checking if there is support for https
import types as types                          # to check on type info
import json                                    # in case the data we need to send is complex
import unicodedata                              # for converting unicode to regular strings

logger = logging.getLogger('att_iot_gateway')

def on_connect(client, userdata, rc):
    'The callback for when the client receives a CONNACK response from the server.'

    if rc == 0:
        msg = "Connected to mqtt broker with result code "+str(rc)
        logger.info(msg)
    else:
        logger.error("Failed to connect to mqtt broker, error: " + mqtt.connack_string(rc))
        return
    
    topic = 'client/' + ClientId + "/in/gateway/" + GatewayId + "/#/command"                                           #subscribe to the topics for the device
    #topic = '#'
    logger.info("subscribing to: " + topic)
    result = _mqttClient.subscribe(topic)                                                    #Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    logger.info(result)


def on_MQTTmessage(client, userdata, msg):
    'The callback for when a PUBLISH message is received from the server.'

    payload = str(msg.payload)
    logger.info("Incoming message - topic: " + msg.topic + ", payload: " + payload)
    topicParts = msg.topic.split("/")
    if on_message is not None:
        try:
            if len(topicParts) >= 7:
                if topicParts[5] == 'device':   # 3
                    devId = topicParts[6]       # 4
                    assetId = topicParts[8]
                else:
                    devId = None
                    assetId = topicParts[6]
                on_message(devId, assetId, msg.payload)                                 #we want the second last value in the array, the last one is 'command'
            else:
                logger.error("unknown topic format: " + msg.topic)
        except:
            logger.exception("failed to process actuator command: " + msg.topic + ", payload: " + msg.payload)

def on_MQTTSubscribed(client, userdata, mid, granted_qos):
    logger.info("Subscribed to topic, receiving data from the cloud: qos=" + str(granted_qos))


#private reference to the mqtt client object for which we reserve a mem loc from the start
_mqttClient = None
_httpServerName = None
_httpClient = None

# gateway specific stuff
_RegisteredGateway = False                                              # when true: gateway is created in cloud, when false, gateway is not created in cloud, only 'loose' devices are managed. User specified all credentials manually (not adviced)


#has to be provided by the module consumer:

on_message = None
'callback for receiving values from the IOT platform: expects 3 params: deviceId, assetId, payload'
ClientId = None
'the id of the client on the ATT platform, used to connect to the http & mqtt servers'
ClientKey = None
'the key that the ATT platform generated for the specified client'
GatewayId = None
'the id of the gateway that we are using.'

def connect(httpServer="api.smartliving.io", secure = False):
    """connect with the http server
    :param secure: When true, an SSL connection will be used, if available.
    :type httpServer: basestring
                      The dns name of the server to use for HTTP communication
    """
    global _httpClient, _httpServerName                                         # we assign to these vars first, so we need to make certain that they are declared as global, otherwise we create new local vars
    if secure and socket.ssl:
        _httpClient = httplib.HTTPSConnection(httpServer)
    else:
        _httpClient = httplib.HTTPConnection(httpServer)
    _httpServerName = httpServer
    logger.info("connected with http server")

def addAsset(id, deviceId, name, description, isActuator, assetType, style = "Undefined"):
    '''add an asset to the device. Use the specified name and description.
    The asset type can be: string, int, bool, double, dateTime, timeSpan or a json schema to declare the content of data represented as json objects.
    :param id: The local id of the asset (it's name)
    :param deviceId: The local id of the device that owns the asset (the name of the device)
    :param name: A label for the asset.
    :param description: A desccription.
    :param isActuator: When true, an actuator will be created, otherwise an asset.
    :param assetType: The data type of the asset: integer, string, number, boolean, json schema definition
    :type style: string
    :param style: how is the asset displayed in the system. Supported values: 'Undefined', 'Primary', 'Config', 'Battery', 'Secondary'
    :return: True when succesful (200 ok was returned), otherwise False
    Can raise exceptions when there were network issues.
    '''
    
    if _RegisteredGateway == False:
        raise Exception('gateway must be registered')

    body = '{"title":"' + name + '","description":"' + description + '", "style": "' + style + '","is":"'
    if isActuator:
        body = body + 'actuator'
    else:
        body = body + 'sensor'

    if assetType[0] == '{':                 # if the asset type is complex (starts with {', then render the body a little different
        body = body + '","profile":' + assetType + '}'
    else:
        body = body + '","profile": {"type":"' + assetType + '" }}'
    headers = _buildHeaders()
    url = "/device/" + deviceId + "/asset/" + str(id)
    
    logger.info("HTTP PUT: " + url)
    logger.info("HTTP HEADER: " + str(headers))
    logger.info("HTTP BODY:" + body)

    return _sendData(url, body, headers, 'PUT')

def addGatewayAsset(id, name, description, isActuator, assetType, style = "Undefined"):
    '''add an asset to the gateway'''
    if _RegisteredGateway == False:
        raise Exception('gateway must be registered')

    body = '{"title":"' + name + '","description":"' + description + '", "style": "' + style + '","is":"'
    if isActuator:
        body = body + 'actuator'
    else:
        body = body + 'sensor'

    if assetType[0] == '{':                 # if the asset type is complex (starts with {', then render the body a little different
        body = body + '","profile":' + assetType + '}'
    else:
        body = body + '","profile": {"type":"' + assetType + '" }}'
    headers = _buildHeaders()
    url = "/asset/" + str(id)
    
    logger.info("HTTP PUT: " + url)
    logger.info("HTTP HEADER: " + str(headers))
    logger.info("HTTP BODY:" + body)

    return _sendData(url, body, headers, 'PUT') 

def deleteAsset(device, id):    
    if not device:
        raise Exception("DeviceId not specified")
    headers = _buildHeaders()
    url = "/device/" + device  + "/" + str(id)

    print("HTTP DELETE: " + url)
    print("HTTP HEADER: " + str(headers))
    print("HTTP BODY: None")
    return _sendData(url, "", headers, "DELETE", 204)
    
def addDevice(deviceId, name, description, activateActivity = False):
    '''creates a new device in the IOT platform. The deviceId gets appended with the value  <GatewayId>_
    if the device already exists, the function will fail
    :rtype : None
    returns True if the operation was succesful, otherwise False
    :param deviceId:
    :param name:
    :param description:
    :param activateActivity:When true, historical data will be recorded for this device.
    :type activateActivity: bool
    '''
    
    if _RegisteredGateway == False:
        raise Exception('gateway must be registered')
    body = '{"title":"' + name + '","description":"' + description + '", "type": "custom", "activityEnabled": ' + str(activateActivity).lower() + '}'
    headers = _buildHeaders()
    url = "/device/" + deviceId
    
    logger.info("HTTP PUT: " + url)
    logger.info("HTTP HEADER: " + str(headers))
    logger.info("HTTP BODY:" + body)

    return _sendData(url, body, headers, 'PUT')

def deviceExists(deviceId):
    '''checks if the device already exists in the IOT platform.
    returns True when it already exists, otherwise False'''
    
    if _RegisteredGateway == False:
        raise Exception('gateway must be registered')
    
    headers = _buildHeaders()
    url = "/device/" + deviceId
    
    logger.info("HTTP GET: " + url)
    logger.info("HTTP HEADER: " + str(headers))

    return _sendData(url, "", headers, 'GET')


def deleteDevice(deviceId):
    '''
        Deletes the specified device from the cloud.
        returns true when successful.
    '''
    headers = _buildHeaders()
    url = "/Device/" + deviceId

    logger.info("HTTP DELETE: " + url)
    logger.info("HTTP HEADER: " + str(headers))
    logger.info("HTTP BODY: None")
    return _sendData(url, "", headers, "DELETE", 204)

def createGateway(name, uid, assets = None):
    'create a new orphan gateway in the cloud'
    
    if assets == None:
        body = '{"uid":"' + uid + '","name":"' + name + '", "assets":[] }'
    else:
        body = '{"uid":"' + uid + '","name":"' + name + '", "assets":' + json.dumps(assets) + ' }'
    headers = {"Content-type": "application/json"}
    url = "/gateway"
    
    logger.info("HTTP POST: " + url)
    logger.info("HTTP HEADER: " + str(headers))
    logger.info("HTTP BODY:" + body)

    return _sendData(url, body, headers)

def getGateway(includeDevices = True):
    try:
        headers = _buildHeaders()
        url = '/gateway/' + GatewayId + '?includeDevices=' + str(includeDevices)

        logger.info("HTTP GET: " + url)
        logger.info("HTTP HEADER: " + str(headers))
        _httpClient.request("GET", url, "", headers)
        response = _httpClient.getresponse()
        logger.info((response.status, response.reason))
        if response.status == 200:
            return json.loads(response.read())
        else:
            response.read()                                                     #need to clear the buffers.
    except:
        logger.exception("get gateway failed")
        _httpClient.close()
        connect(_httpServerName)                                                # recreate the connection when something went wrong. if we don't do this and an error occured, consecutive requests will also fail.
    return None

def finishclaim(name, uid):
    '''finish the claiming process for a previously created gateway.  When done, the system will store the credentials
    return true if succesful, otherwise false'''
    body = '{"uid":"' + uid + '","name":"' + name + '" , "assets":[]}'
    headers = {"Content-type": "application/json"}
    url = "/gateway"

    logger.info("HTTP POST: " + url)
    logger.info("HTTP HEADER: " + str(headers))
    logger.info("HTTP BODY:" + body)

    try:
        _httpClient.request('POST', url, body, headers)
        response = _httpClient.getresponse()
    except:
        logger.exception("finishClaim")
        _httpClient.close()
        connect(_httpServerName)                                                # recreate the connection when something went wrong. if we don't do this and an error occured, consecutive requests will also fail.
        return False
    status = response.status
    logger.info((status, response.reason))
    response = response.read()
    logger.info(response)
    if status == 200:
        _storeCredentials(json.loads(response))
        return True
    else:
        return False

def getAssetState(assetId, deviceId):
    '''look up the current state value for the asset with the specified local id, on the specified device (local id)  
    if not found, returns None'''
    
    try:
        if _RegisteredGateway == False:
            raise Exception('gateway must be registered')
        headers = _buildHeaders()
        url = "/device/" + deviceId + "/asset/" + str(assetId) + "/state"
    
        logger.info("HTTP GET: " + url)
        logger.info("HTTP HEADER: " + str(headers))

        _httpClient.request("GET", url, "", headers)
        response = _httpClient.getresponse()
        logger.info((response.status, response.reason))
        if response.status == 200:
            responseObj = json.loads(response.read())
            if responseObj:
                return responseObj
        else:
            response.read()                                                     #need to clear the buffers.
    except Exception as e:
        logger.exception("get asset state failed")
        _httpClient.close()
        connect(_httpServerName)                                                # recreate the connection when something went wrong. if we don't do this and an error occured, consecutive requests will also fail.
    return None                                                                 # if we couldn't find a proper result, return null

def _buildPayLoadHTTP(value):
    data = {"value": value, "at": datetime.utcnow().isoformat()}
    return json.dumps(data)


def _storeCredentials(gateway):
    'extracts all the relevant info from the gateway response object'
    global GatewayId
    global ClientKey
    global ClientId
    global _RegisteredGateway
    GatewayId = unicodedata.normalize('NFKD', gateway["id"]).encode('ascii','ignore')       #convert to regular strings (from unicode), if we don't do this, the mqtt subscribe fails (can't handle unicode as it's uid for the session)
    ClientKey = unicodedata.normalize('NFKD', gateway["key"]).encode('ascii','ignore')
    ClientId = unicodedata.normalize('NFKD', gateway["client"]["clientId"]).encode('ascii','ignore')
    _RegisteredGateway = True                                   # so we know that we are using a registered gateway.

def authenticate():
    '''validate that the currently stored credentials are ok.
    return true if succesful, otherwise false'''
   
    headers = _buildHeaders()
    url = "/gateway"

    logger.info("HTTP GET: " + url)
    logger.info("HTTP HEADER: " + str(headers))

    global _RegisteredGateway
    if _sendData(url, "", headers, 'GET'):
        _RegisteredGateway = True
        return True
    else:
        _RegisteredGateway = False
        return False

def _reconnectAfterSendData():
    try:
        _httpClient.close()
        connect(_httpServerName)                # recreate the connection when something went wrong. if we don't do this and an error occured, consecutive requests will also fail.
    except:
        logger.exception("reconnect failed after _sendData produced an error")

def _sendData(url, body, headers, method = 'POST', status = 200):
    """send the data and check the result
        Some multi threading applications can have issues with the server closing the connection, if this happens
        we try again
    """
    success = False
    while not success:
        try:
            _httpClient.request(method, url, body, headers)
            response = _httpClient.getresponse()
            logger.info((response.status, response.reason))
            logger.info(response.read())
            return response.status == status
        except SocketError as e:
            _reconnectAfterSendData()
            if e.errno != errno.ECONNRESET:             # if it's error 104 (connection reset), then we try to resend it, cause we just reconnected
                raise
        except:
            _reconnectAfterSendData()
            raise

def _buildHeaders():
    return {"Content-type": "application/json", "Auth-GatewayKey": ClientKey, "Auth-GatewayId": GatewayId}


def subscribe(mqttServer = "broker.smartliving.io", port = 1883, secure = False):
    '''start the mqtt client and make certain that it can receive data from the IOT platform
	   :param mqttServer:  the address of the mqtt server. Only supply this value if you want to a none standard server. Default = broker.smartliving.io
	   :param port: the port number to communicate on with the mqtt server. Default = 1883
	   :param secure: When true, an SSL connection is used. Default = False.  When True, use port 8883 on broker.smartliving.io
	   Note: SSL will can only be used when the mqtt lib has been compiled with support for ssl
    '''
    if _RegisteredGateway == False:
        raise Exception('gateway must be registered')

    global _mqttClient                                             # we assign to this var first, so we need to make certain that they are declared as global, otherwise we create new local vars
    if len(GatewayId) > 23:
        mqttId = GatewayId[:23]
    else:
        mqttId = GatewayId
    _mqttClient = mqtt.Client(mqttId)
    _mqttClient.on_connect = on_connect
    _mqttClient.on_message = on_MQTTmessage
    _mqttClient.on_subscribe = on_MQTTSubscribed
    if ClientId is None:
        logger.error("ClientId not specified, can't connect to broker")
        raise Exception("ClientId not specified, can't connect to broker")
    brokerId = ClientId + ":" + ClientId
    _mqttClient.username_pw_set(brokerId, ClientKey);
    if secure and socket.ssl:
        _mqttClient.tls_set("cacert.pem")
    _mqttClient.connect(mqttServer, port, 60)
    _mqttClient.loop_start()

def _buildPayLoad(value):
    typeOfVal = type(value)
    if typeOfVal in [types.IntType, types.BooleanType, types.FloatType, types.LongType, types.StringType]:      # if it's a basic type: send as csv, otherwise as json.
        timestamp = calendar.timegm(time.gmtime())                                # we need the current epoch time so we can provide the correct time stamp.
        return str(timestamp) + "|" + str(value)                                            # build the string that contains the data that we want to send
    else:
        data = {  "value": value, "at": datetime.utcnow().isoformat() + 'Z' }       # the +Z is a small hack cause utcnow doesn't include timezone info. Since we want utc time, we can add the value 'z' to indicate this.
        return json.dumps(data)



def send(value, deviceId, assetId):
    'send the data to the cloud. Data can be a single value or object'
    if ClientId is None:
        logger.error("ClientId not specifie")
        raise Exception("ClientId not specified")
    if assetId is None:
        logger.error("sensor id not specified")
        raise Exception("sensorId not specified")
    if _RegisteredGateway == False:
        raise Exception('gateway must be registered')

    toSend = _buildPayLoad(value)
    topic = "client/" + ClientId + "/out/gateway/" + GatewayId
    if deviceId != None:
        topic += "/device/" + deviceId + "/asset/" + str(assetId) + "/state"             # also need a topic to publish to
    else:
        topic += "/asset/" + str(assetId) + "/state"
    logger.info("Publishing message - topic: " + topic + ", payload: " + toSend)
    _mqttClient.publish(topic, toSend, 0, False)
