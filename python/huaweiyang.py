def get_capabilities(self):
        # Just need to replace a single value in the default capabilities
        c = []
        c.append('urn:ietf:params:netconf:base:1.0')
        c.append('urn:ietf:params:netconf:base:1.1')

        return c