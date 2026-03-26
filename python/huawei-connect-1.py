# -*- coding: utf-8 -*- 
import sys 
import socket
from ncclient import manager 
from ncclient import operations 
 
def huawei_connect(host, port, user, password): 
    return manager.connect(host=host, 
                           port=port, 
                           username=user, 
                           password=password, 
                           hostkey_verify = False, 
                           device_params={'name': "huaweiyang"}, 
                           allow_agent = False, 
                           look_for_keys = False) 
 
def test_connect(host, port, user, password): 
    with huawei_connect(host, port=port, user=user, password=password) as m: 
 
        n = m._session.id         
        print("The session id is %s." % (n)) 
 
print(sys.version)
 
if __name__ == '__main__':
    test_connect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])