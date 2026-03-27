# test_export_config.py
import sys
from ncclient import manager

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

def test_export_config(host, port, user, password):

    with huawei_connect(host, port=port, user=user, password=password) as m:

        with m.locked("running"):
            m.copy_config(source="running", target="file:///output.xml")

if __name__ == '__main__':   
    test_export_config(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])