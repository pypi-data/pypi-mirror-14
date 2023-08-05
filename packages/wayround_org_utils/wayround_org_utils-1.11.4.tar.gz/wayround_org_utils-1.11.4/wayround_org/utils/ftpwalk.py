
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
        return

    def __del__(self):
        self.clean()
        return

    def _init(self, verbose=False):
        self._verbose = verbose

        self.re_ex = re.compile(
            r'(.*?)([ \t]+)(.*?)([ \t]+)(.*?)([ \t]+)(.*?)'
            r'([ \t]+)(.*?)([ \t]+)(.*?)([ \t]+)(.*?)([ \t]+)'
            r'(.*?)([ \t]+)(.*)'
            )

        self.clean()
        return

    def setverbose(self, value):
        self._verbose = value
        return

    def clean(self):

        if self._verbose:
            v("Cleaning instance")

        self._file_lists = {}

        self._fstats_cb_dir = ''
        self._fstats_cb_errors = False
        return

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

        return

    def fstats(self, dirname, force=False):

        ret = None

        if self._verbose:
            v("Getting directory stats: {}".format(dirname))

        if self._ftpc is None:
            ret = 'not connected'

        if ret is None:

            if not isinstance(dirname, str):
                raise TypeError

            if dirname == '':
                raise ValueError

            if dirname in self._file_lists and not force:
                ret = 'ok'

        if ret is None:
            r = self.is_dir(dirname)

            if r == 'not connected':
                ret = 'not connected'

            elif r == 'errors':
                ret = 'errors'

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
                    ret = 'errors'
                else:
                    ret = 'ok'

            elif r == False:
                ret = 'not dir'

            else:
                ret = 'errors'

        return ret

    def fstat_d_n(self, dirname, name):

        ret = None

        if self._ftpc is None:
            ret = 'not connected'

        if ret is None:

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
                    ret = self._file_lists[dirname][name]
                else:
                    ret = 'file not found'

        if ret is None:
            r = self.fstats(dirname)

            if r == 'not connected':
                ret = 'not connected'

            elif r == 'ok':
                ret = self.fstat_d_n(dirname, name)

            elif r == 'not dir':
                ret = 'not dir'

            elif r == 'errors':
                ret = 'errors'

            else:
                ret = 'errors'

        return ret

    def fstat(self, name):

        ret = None

        if self._ftpc is None:
            ret = 'not connected'

        if ret is None:

            if not isinstance(name, str):
                raise TypeError

            if name == '':
                raise ValueError

            name = wayround_org.utils.path.normpath(name)
            fdir = os.path.dirname(name)
            name = os.path.basename(name)

            ret = self.fstat_d_n(fdir, name)

        return ret

    def _is(self, name, c='-', no=False):

        ret = None

        if self._ftpc is None:
            ret = 'not connected'

        if ret is None:

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
                ret = 'not connected'

            elif r == 'file not found':
                ret = False

            elif r == 'error getting file stat':
                ret = 'errors'

            elif r == 'not dir':
                ret = False

            elif r == 'errors':
                ret = 'errors'

            if not no:
                if r['mode'][0] == c:
                    ret = True
                else:
                    ret = False
            else:
                if r['mode'][0] != c:
                    ret = True
                else:
                    ret = False

        return ret

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
            ret = 'not connected'

        if ret is None:

            if not isinstance(name, str):
                raise TypeError

            if name == '':
                raise ValueError

            if name == '/':
                ret = True

        if ret is None:

            r = self.fstat_d_n(
                os.path.dirname(name),
                os.path.basename(name)
                )

            if r == 'not connected':
                ret = 'not connected'

            elif r == 'file not found':
                ret = False

            elif r == 'error getting file stat':
                ret = 'errors'

            elif r == 'not dir':
                ret = False

            elif r == 'errors':
                ret = 'errors'

            else:
                ret = True

        return ret

    def get_all_files(self, dirname):

        ret = None

        if self._ftpc is None:
            ret = 'not connected'

        if ret is None:

            r = self.fstats(dirname)

            if r == 'ok':
                ret = self._file_lists[dirname]

            else:
                ret = r

        return ret

    def get(self, dirname, c='d', no=False):

        ret = None

        l = []

        r = self.get_all_files(dirname)

        if not isinstance(r, dict):
            ret = r

        else:
            for i in r.keys():
                if no:
                    if r[i]['mode'][0] != c:
                        l.append(i)
                else:
                    if r[i]['mode'][0] == c:
                        l.append(i)
            ret = l

        return ret

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
            raise TypeError("`server' must be str")

        if server == '':
            raise ValueError("invalid `server' value")

        self._server = server

        self._init()

        return

    def connect(self):
        ret = True

        if self._verbose:
            v("Connecting to {}".format(self._server))

        if self._ftpc is not None:
            ret = True

        else:

            try:
                self._ftpc = ftplib.FTP(self._server)
            except:
                ret = False

        if ret:
            try:
                self._ftpc.login()
            except:
                # TODO: invalid exception handling
                ret = False

        if not ret:
            self.disconnect()

        if self._verbose:
            if not ret:
                v("Connection failed")

        return ret

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

        return

    def reconnect(self):
        self.disconnect()
        return self.connect()

    def clean(self):

        FTPWalk.clean(self)

        self.disconnect()
        return

    # __del__ not required as it is present in parent Class
