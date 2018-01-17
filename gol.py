""" GAME OBJECT LIST"""
class GOL():
    golist = []

    @classmethod
    def add_go(cls,object):
        cls.golist.append(object)

    @classmethod
    def get_go(cls,type):
        for go in cls.golist:
            if isinstance(go, type):
                return go

    @classmethod
    def get_golist(cls,type=""):
        type_list = []
        if type:
            for go in cls.golist:
                if isinstance(go, type):
                    type_list.append(go)
            return type_list
        else:
            return cls.golist

    @classmethod
    def del_go(cls,object):
        if object in cls.golist:
            cls.golist.remove(object)

    @classmethod
    def del_golist(cls):
        del cls.golist[:]