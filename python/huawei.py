def get_capabilities(self):
        # Just need to replace a single value in the default capabilities
        c = super(HuaweiDeviceHandler, self).get_capabilities()
        c.append('http://www.huawei.com/netconf/capability/execute-cli/1.0')
        c.append('http://www.huawei.com/netconf/capability/action/1.0')
        c.append('http://www.huawei.com/netconf/capability/active/1.0')
        c.append('http://www.huawei.com/netconf/capability/discard-commit/1.0')
        c.append('http://www.huawei.com/netconf/capability/exchange/1.0')

        return c