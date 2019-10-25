# coding=utf-8

APPLY = 1
NOAPPLY = 0
class ResMsg(object):
    """
    success return code = 0
    fail return code != 0 and detail in msg
    """
    def __init__(self, code=0, data=None, msg=""):
        self.code = code
        self.data = data
        self.msg = msg

    def __repr__(self):
        return {"code": self.code, "msg": self.msg, "data": self.data}

    def to_dict(self):
        return {"code": self.code, "msg": self.msg, "data": self.data}