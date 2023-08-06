import os
import os.path as osp
import shutil
import re
import shelve

def _zslidirh(subdir):
    """(Hilfsfunktion für ls) Set aller Einträge zurückgeben"""

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

def ls(subdir):
    """Liste aller Einträge sortiert zurückgeben"""
    return sorted(_zslidirh(subdir))

class entry:
    __slots__ = [ '__ename', '__datf', '__data' ]

    def __init__(self, ename):
        self.__ename = ename
        self.__datf = osp.join(ename, 'D')
        self.reload_data()

    def __getName(self):
        return self.__ename

    def __repr__(self):
        return "zdbc.entry('" + self.name + "')"

    def __str__(self):
        return self.name + ": " + str(self.__data)

    def litems(self):
        return list(self.__data)

    def reload_data(self):
        if not osp.isfile(self.__datf):
            self.__data = dict()
            return False

        with shelve.open(self.__datf) as s:
            self.__data = dict(s)

        return True

    def save_data(self):
        """Speichert die Eigenschaften im shelve"""
        with shelve.open(self.__datf) as s:
            s.clear()
            for prop,val in self.__data.items():
                s[prop] = val

    def cleanup(self):
        """Löscht alle leeren Eigenschaften"""
        ler = list()

        for prop,val in self.__data.items():
            if val == None:
                ler.append(prop)

        for i in ler:
            del self.__data[i]

        self.save_data()

    def __contains__(self, prop):
        if not prop:
            return False

        if (prop not in self.__data) or (self.__data[prop] == None):
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

            if val == None:
                return False
            else:
                self.set(prop, val)
        else:
            if self.__data[prop] == None:
                return False

        return (prop in self.__data)

    def __getitem__(self, prop):
        if prop in self:
            return self.__data[prop]

    def __setitem__(self, prop, content):
        os.makedirs(self.name, exist_ok=True)

        with shelve.open(self.__datf, writeback=True) as s:
            s[prop] = content
            self.__data = dict(s)

    def append_to(self, prop, content):
        os.makedirs(self.name, exist_ok=True)

        with shelve.open(self.__datf, writeback=True) as s:
            s[prop].append(content)
            self.__data = dict(s)

    def __delitem__(self, prop):
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

            try:
                with shelve.open(self.__datf, writeback=True) as s:
                    del s[prop]
            except:
                pass

    name = property(__getName)

def search(workset, prop, matchtype, value):
    """Suche Einträge
       Rückgabewert: Liste der gesuchten Einträge
    """
    if matchtype == "LIKE":
        value = re.compile(str(value))
    elif not matchtype == "=":
        raise ValueError("search: incorrect matchtype: " + matchtype)

    nwset = set()

    if prop == "name":
        if matchtype == "LIKE":
            for i in workset:
                if value.search(i):
                    nwset.add(i)

        elif matchtype == "=":
            if value in workset:
                nwset.add(value)

    else:
        if matchtype == "LIKE":
            for i in workset:
                enti = entry(i)
                if value.search(str(enti[prop])):
                    nwset.add(i)

        elif matchtype == "=":
            for i in workset:
                enti = entry(i)
                dat = enti[prop]
                if dat == value:
                    nwset.add(i)
                else:
                    iparts = None
                    try:
                        iparts = dat.splitlines()
                    except:
                        pass

                    if iparts:
                        for line in iparts:
                            if line == value:
                                nwset.add(i)
                                break

    return sorted(nwset)

def lients(l):
    """Liste von Einträgen als Liste von Instanzen der Klasse 'entry' zurückgeben"""
    ret = list()
    for i in l:
        ret.append(entry(i))
    return ret
