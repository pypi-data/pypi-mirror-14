
import ftplib
import logging
import os.path
import re

import wayround_org.utils.path


def v(s):
    logging.debug(s)


class FTPWalk:

    def __init__(self, ftp_connection, verbose=False):

        if not isinstance(ftp_connection, ftplib.FTP):
            raise TypeError

        self._ftpc = ftp_connection

        self._init(verbose)

    def __del__(self):
        self.clean()

    def _init(self, verbose=False):
        self._verbose = verbose

        self.re_ex = re.compile(
            r'(.*?)([ \t]+)(.*?)([ \t]+)(.*?)([ \t]+)(.*?)([ \t]+)(.*?)([ \t]+)(.*?)([ \t]+)(.*?)([ \t]+)(.*?)([ \t]+)(.*)')

        self.clean()

    def setverbose(self, value):
        self._verbose = value

    def clean(self):

        if self._verbose:
            v("Cleaning instance")

        self._file_lists = {}

        self._fstats_cb_dir = ''
        self._fstats_cb_errors = False

    def _fstats_cb(self, string):

        if not isinstance(string, str):
            raise TypeError

        if string == '':
            raise ValueError

        m = self.re_ex.match(string)

        if m is not None:

            self._file_lists[self._fstats_cb_dir][m.group(17)] = {
                'mode': m.group(1),
                'blocks': m.group(3),
                'uid': m.group(5),
                'gid': m.group(7),
                'size': m.group(9),
                'date1': m.group(11),
                'date2': m.group(13),
                'date3': m.group(15)
                }
        else:
            self._fstats_cb_errors = True

        del m

    def fstats(self, dirname, force=False):

        if self._verbose:
            v("Getting directory stats: {}".format(dirname))

        if self._ftpc is None:
            return 'not connected'

        if not isinstance(dirname, str):
            raise TypeError

        if dirname == '':
            raise ValueError

        if dirname in self._file_lists and not force:
            return 'ok'
        else:
            r = self.is_dir(dirname)

            if r == 'not connected':
                return 'not connected'

            elif r == 'errors':
                return 'errors'

            elif r == True:

                if dirname in self._file_lists:
                    del(self._file_lists[dirname])

                self._fstats_cb_dir = dirname
                self._file_lists[dirname] = {}
                self._fstats_cb_errors = False
                try:
                    self._ftpc.dir(dirname, self._fstats_cb)
                except:
                    self._fstats_cb_errors = True

                if self._fstats_cb_errors:
                    if dirname in self._file_lists:
                        del(self._file_lists[dirname])
                    return 'errors'
                else:
                    return 'ok'

            elif r == False:
                return 'not dir'

            else:
                return 'errors'

    def fstat_d_n(self, dirname, name):

        if self._ftpc is None:
            return 'not connected'

        if not isinstance(dirname, str):
            raise TypeError

        if dirname == '':
            raise ValueError

        if not isinstance(name, str):
            raise TypeError

        if name == '':
            raise ValueError

        if dirname in self._file_lists:
            if name in self._file_lists[dirname]:
                return self._file_lists[dirname][name]
            else:
                return 'file not found'
        else:
            r = self.fstats(dirname)

            if r == 'not connected':
                return 'not connected'

            elif r == 'ok':
                return self.fstat_d_n(dirname, name)

            elif r == 'not dir':
                return 'not dir'

            elif r == 'errors':
                return 'errors'

            else:
                return 'errors'

    def fstat(self, name):

        if self._ftpc is None:
            return 'not connected'

        if not isinstance(name, str):
            raise TypeError

        if name == '':
            raise ValueError

        name = wayround_org.utils.path.normpath(name)
        fdir = os.path.dirname(name)
        name = os.path.basename(name)
        return self.fstat_d_n(fdir, name)

    def _is(self, name, c='-', no=False):
        if self._ftpc is None:
            return 'not connected'

        if not isinstance(name, str):
            raise TypeError

        if name == '':
            raise ValueError

        if name == '/':
            return True

        r = self.fstat_d_n(
            os.path.dirname(name),
            os.path.basename(name)
            )

        if r == 'not connected':
            return 'not connected'

        elif r == 'file not found':
            return False

        elif r == 'error getting file stat':
            return 'errors'

        elif r == 'not dir':
            return False

        elif r == 'errors':
            return 'errors'

        if not no:
            if r['mode'][0] == c:
                return True
            else:
                return False
        else:
            if r['mode'][0] != c:
                return True
            else:
                return False

    def is_dir(self, name):
        return self._is(name, c='d')

    def is_not_dir(self, name):
        return self._is(name, c='d', no=True)

    def is_file(self, name):
        return self._is(name, c='-')

    def is_link(self, name):
        return self._is(name, c='l')

    def exists(self, name):

        if self._ftpc is None:
            return 'not connected'

        if not isinstance(name, str):
            raise TypeError

        if name == '':
            raise ValueError

        if name == '/':
            return True

        r = self.fstat_d_n(
            os.path.dirname(name),
            os.path.basename(name)
            )

        if r == 'not connected':
            return 'not connected'

        elif r == 'file not found':
            return False

        elif r == 'error getting file stat':
            return 'errors'

        elif r == 'not dir':
            return False

        elif r == 'errors':
            return 'errors'

        else:
            return True

    def get_all_files(self, dirname):

        if self._ftpc is None:
            return 'not connected'

        r = self.fstats(dirname)

        if r == 'ok':
            return self._file_lists[dirname]

        else:
            return r

    def get(self, dirname, c='d', no=False):
        l = []

        r = self.get_all_files(dirname)

        if not isinstance(r, dict):
            return r

        else:
            for i in r.keys():
                if no:
                    if r[i]['mode'][0] != c:
                        l.append(i)
                else:
                    if r[i]['mode'][0] == c:
                        l.append(i)
            return l

    def get_normal_files(self, dirname):
        return self.get(dirname, '-')

    def get_dirs(self, dirname):
        return self.get(dirname, 'd')

    def get_links(self, dirname):
        return self.get(dirname, 'l')

    def get_not_dirs(self, ftpc, dirname):
        return self.get(dirname, 'd', True)


class FTPWalkSole(FTPWalk):

    def __init__(self, server, verbose=False):

        if not isinstance(server, str):
            raise TypeError

        if server == '':
            raise ValueError

        self._server = server

        self._init()

    def connect(self):
        isok = True

        if self._verbose:
            v("Connecting to {}".format(self._server))

        if self._ftpc is not None:
            return True

        try:
            self._ftpc = ftplib.FTP(self._server)
        except:
            isok = False

        if isok:
            try:
                self._ftpc.login()
            except:
                isok = False

        if not isok:
            self.disconnect()

        if self._verbose:
            if not isok:
                v("Connection failed")

        return isok

    def disconnect(self):
        try:
            self._ftpc.quit()
        except:
            pass

        try:
            self._ftpc.close()
        except:
            pass

        self._ftpc = None

    def reconnect(self):
        self.disconnect()
        return self.connect()

    def clean(self):

        FTPWalk.clean(self)

        self.disconnect()

    # __del__ not required as it is present in parent Class
