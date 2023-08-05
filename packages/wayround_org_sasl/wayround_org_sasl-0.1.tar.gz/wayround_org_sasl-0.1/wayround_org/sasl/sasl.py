

import base64

import wayround_org.sasl.mechs.plain


MECHANISMS = {
    'PLAIN': {
        'server': wayround_org.sasl.mechs.plain.Server,
        'client': wayround_org.sasl.mechs.plain.Client,
        }
    }


class SASLSession:

    def __init__(self, mech_obj):
        self.mech_obj = mech_obj
        return

    def step(self, data):
        return self.mech_obj.step(data)

    def step64(self, text):

        data = base64.b64decode(text)
        code, data = self.step(data)
        text = base64.b64encode(data)

        return code, text

    @property
    def properties(self):
        return self.mech_obj.properties

    def __getitem__(self, obj):
        return self.mech_obj.properties[obj]


def init_mech(mech_name, mode, callback=None):

    if not mech_name in MECHANISMS:
        raise Exception("mechanism is not supported")

    if not mode in MECHANISMS[mech_name]:
        raise Exception(
            "mechanism `{}' does not supports named mode".format(mech_name)
            )

    return SASLSession(MECHANISMS[mech_name][mode](callback))
