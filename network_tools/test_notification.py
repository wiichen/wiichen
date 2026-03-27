# test_notification.py
import sys
import logging
from ncclient import manager
from ncclient import operations
log = logging.getLogger(__name__) 

CREATE_SUBSCRIPTION = '''<?xml version="1.0" encoding="UTF-8"?>
  <rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="{}">
    <create-subscription xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0">
      <stream>NETCONF</stream>
    </create-subscription>
  </rpc>'''

#Fill the device information and establish a NETCONF session
def huawei_connect(host, port, user, password):
    return manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           hostkey_verify = False,
                           device_params={'name': "huaweiyang"},
                           allow_agent = False,
                           look_for_keys = False)

def test_notification(host, port, user, password):
    #1.Create a NETCONF session
    with huawei_connect(host, port=port, user=user, password=password) as m:

        #2.Set the message-id for the rpc
        msgId = 1001
        rpc = CREATE_SUBSCRIPTION.format(msgId)

        #3.Send rpc
        result = m._session.send(rpc)
        
        #4.Attempt to retrieve one notification
        ntf = m.take_notification(block=True, timeout=None) 
        print("The notification message is %s." % (ntf))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_notification(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])