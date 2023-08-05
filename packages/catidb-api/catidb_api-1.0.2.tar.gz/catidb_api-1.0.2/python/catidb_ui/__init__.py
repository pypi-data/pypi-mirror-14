# -*- coding: utf-8 -*-


class GlobalVars(object):
    _catidb = None

    @property
    def catidb(self):
        return self._catidb

    @catidb.setter
    def catidb(self, catidb):
        if self._catidb is not None:
            del self._catidb  # TODO : disconnect catidb properly
        self._catidb = catidb

global_vars = GlobalVars()
