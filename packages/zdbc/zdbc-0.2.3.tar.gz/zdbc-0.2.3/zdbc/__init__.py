import os
import os.path as osp
import sys
import shutil
import re
import shelve

def _zslidirh(subdir):
    """(Hilfsfunktion für lidir) Set aller Einträge zurückgeben"""

    ret = set()

    for i in os.listdir(subdir):
        ptd = osp.relpath(osp.realpath(osp.join(subdir, i)))

        if (ptd == subdir) or osp.ismount(ptd):
            continue

        try:
            ret |= _zslidirh(ptd)
        except:
            continue

        if osp.isfile(osp.join(ptd, 'D')):
            ret.add(ptd)

    return ret

def lidir(subdir):
    """Liste aller Einträge sortiert zurückgeben"""
    return sorted(_zslidirh(subdir))

ls = lidir

class entry:
    __slots__ = [ '__ename', '__datf', '__data' ]

    def __init__(self, ename):
        self.__ename = ename
        self.__datf = osp.join(ename, 'D')
        self.reload_data()

    def __getName(self):
        return self.__ename

    def reload_data(self):
        if not osp.isfile(self.__datf):
            self.__data = dict()
            return False

        with shelve.open(self.__datf) as s:
            self.__data = dict(s)

        return True

    def getraw(self, prop = 'D'):
        """Gib den Inhalt der Eigenschaft zurück"""

        if (prop not in self.__data) or (self.__data[prop] == None):
            # check for new data
            self.reload_data()

        if prop not in self.__data:
            # try prop-file
            val = None
            try:
                fname = osp.join(self.name, prop)
                with open(fname) as f:
                    val = f.read()
                os.remove(fname)
            except:
                pass

            self.set(prop, val)

        return self.__data[prop]

    def set(self, prop = 'D', content = "", append = False):
        """Setze die Eintragseigenschaft 'prop' auf 'content' bzw. hänge an"""
        os.makedirs(self.name, exist_ok=True)

        with shelve.open(self.__datf, writeback=True) as s:
            if append:
                s[prop].append(content)
            else:
                s[prop] = content
            self.__data = dict(s)

    def rm(self, prop = 'D'):
        """Eintrag oder Eigenschaft löschen"""

        if prop == 'D':
            shutil.rmtree(self.name)
        else:
            entsf = osp.join(self.name, prop)
            if osp.isdir(entsf):
                shutil.rmtree(entsf)
            elif osp.isfile(entsf):
                os.remove(entsf)

            if prop in self.__data:
                del self.__data[prop]

            with shelve.open(self.__datf, writeback=True) as s:
                if prop in s:
                    del s[prop]

    name = property(__getName)

def search(*args):
    """Suche Einträge
       Argumente: Typ tuple (linktype, prop, matchtype, value)
       Rückgabewert: Liste der gesuchten Einträge
    """
    wholeset = frozenset(ls('.'))
    curset = set(wholeset)
    for i in args:
        if not isinstance(i, tuple):
            raise TypeError("i is an instance of class " + i.__class__ + ", but it should be a tuple")

        if len(i) != 4:
            raise ValueError("i has a length of " + len(i) + ", but it should have the length of 4")

        workset = set()
        if i[0] == "AND":
            workset = frozenset(curset)
        elif i[0] == "OR":
            workset = wholeset
        else:
            raise ValueError("search: incorrect linktype: " + i[0])

        matchtype = i[2]
        if matchtype == "LIKE":
            value = re.compile(str(i[3]))
        elif matchtype == "=":
            value = i[3]
        else:
            raise ValueError("search: incorrect matchtype: " + matchtype)

        nwset = set()

        if i[1] == "name":
            if matchtype == "LIKE":
                for j in workset:
                    if value.search(j):
                        nwset.add(j)

            elif matchtype == "=":
                if value in workset:
                    nwset.add(value)

        else:
            if matchtype == "LIKE":
                for j in workset:
                    enti = entry(j)
                    if value.search(str(enti.getraw(i[1]))):
                        nwset.add(j)

            elif matchtype == "=":
                for j in workset:
                    enti = entry(j)
                    dat = enti.getraw(i[1])
                    if dat == value:
                        nwset.add(j)
                    else:
                        iparts = None
                        try:
                            iparts = dat.splitlines()
                        except:
                            pass

                        if iparts:
                            for line in iparts:
                                if line == value:
                                    nwset.add(j)
                                    break

        if i[0] == "AND":
            curset = nwset
        elif i[0] == "OR":
            curset |= nwset

    return sorted(curset)

def lients(l):
    """Liste von Einträgen als Liste von Instanzen der Klasse 'entry' zurückgeben"""
    ret = list()
    for i in l:
        ret.append(entry(i))
    return ret
