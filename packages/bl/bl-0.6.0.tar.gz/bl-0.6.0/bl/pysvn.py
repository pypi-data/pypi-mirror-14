
from bl.dict import Dict
import pysvn                # http://pysvn.stage.tigris.org

class PySVN(Dict):

    def __init__(self, **SVN):
        Dict.__init__(self, **SVN)
        self.pysvn = pysvn.Client()
        if SVN.username is not None and SVN.password is not None:
            self.pysvn.callback_get_login = \
                lambda realm, username, may_save: True, SVN.username, SVN.password, True