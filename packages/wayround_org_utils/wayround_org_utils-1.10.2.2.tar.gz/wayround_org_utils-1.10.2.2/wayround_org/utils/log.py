
import threading
import logging
import os
import io
import sys


import wayround_org.utils.path
import wayround_org.utils.stream
import wayround_org.utils.time
import wayround_org.utils.error
import wayround_org.utils.osutils


class LoggingFileLikeObject:

    def __init__(self, log_instance, typ='info'):

        if not type(log_instance) == Log:
            raise TypeError("only Log instance allowed here")

        if not typ in ['info', 'error']:
            raise ValueError("invalid typ value")

        self._log = log_instance
        self._typ = typ
        self._pipe = os.pipe()
        self._pipe_read_file = os.fdopen(self._pipe[0])
        self._stop_flag = False

        self._close_lock = threading.Lock()

        self._thread = threading.Thread(
            name="Thread of {}".format(self),
            target=self._thread_run
            )

        self._thread.start()

        return

    def fileno(self):
        return self._pipe[1]

    def close(self):
        with self._close_lock:
            ret = os.close(self._pipe[1])
            self._stop_flag = True
        return ret

    def _thread_run(self):
        for line in iter(self._pipe_read_file.readline, ''):

            with self._close_lock:

                if self._stop_flag:
                    break

                line = line.rstrip(' \n\r\0')

                if self._typ == 'info':
                    self._log.info(line)

                if self._typ == 'error':
                    self._log.error(line)

        self._pipe_read_file.close()

        return


def process_output_logger(process, log):

    raise Exception(
        "this is depricated. use .stdout and/or .stderr objects"
        )

    t = wayround_org.utils.stream.lbl_write(
        process.stdout,
        log,
        True
        )
    t.start()

    t2 = wayround_org.utils.stream.lbl_write(
        process.stderr,
        log,
        threaded=True,
        typ='error'
        )
    t2.start()

    t.join()
    t2.join()

    return


class Log:

    def __init__(
            self,
            log_dir,
            logname,
            echo=True,
            timestamp=None,
            longest_logname=None,
            group=None,
            user=None
            ):

        ret = 0
        self.code = 0
        self.fileobj = None
        self.logname = logname
        self.log_filename = None
        self.longest_logname = longest_logname
        self._write_lock = threading.Lock()

        # TODO: group and user parameter's behavior need to be improved
        self._group, self._user = wayround_org.utils.osutils.convert_gid_uid(
            group,
            user
            )

        self.stdout = LoggingFileLikeObject(self, 'info')
        self.stderr = LoggingFileLikeObject(self, 'error')

        os.makedirs(log_dir, exist_ok=True)

        if (not os.path.isdir(log_dir)
                or os.path.islink(log_dir)
            ):
            logging.error(
                "Current file type is not acceptable: {}".format(
                    log_dir
                    )
                )
            ret = 2

        if ret == 0:
            if self._user is not None and self._group is not None:
                os.chown(
                    log_dir,
                    self._user,
                    self._group
                    )

        if ret == 0:

            if timestamp is None:
                timestamp = wayround_org.utils.time.currenttime_stamp_iso8601()

            filename = wayround_org.utils.path.abspath(
                os.path.join(
                    log_dir,
                    "{ts:26} {name}.txt".format(
                        name=logname,
                        ts=timestamp
                        )
                    )
                )

            self.log_filename = filename

            try:
                self.fileobj = open(filename, 'w')
            except:
                logging.exception("Error opening log file")
                ret = 3
            else:
                self.info(
                    "[{}] log started" .format(
                        self.logname
                        ),
                    echo=echo,
                    timestamp=timestamp
                    )

        if ret == 0:
            if self._user is not None and self._group is not None:
                os.chown(
                    self.log_filename,
                    self._user,
                    self._group
                    )

        if ret != 0:
            raise Exception("Exception during Log creation. read above.")

        return

    def __del__(self):
        if self:
            if self.fileobj:
                if not self.fileobj.closed:
                    try:
                        self.stop()
                    except:
                        pass
        return

    def stop(self, echo=True):
        if self.fileobj is None:
            raise Exception("Programming error")

        timestamp = wayround_org.utils.time.currenttime_stamp_iso8601()
        self.info(
            "[{}] log ended" .format(
                self.logname
                ),
            echo=echo,
            timestamp=timestamp
            )

        self.stdout.close()
        self.stderr.close()

        self.fileobj.flush()
        self.fileobj.close()

        return

    close = stop

    def write(self, text, echo=False, typ='info', timestamp=None):

        if not typ in ['info', 'error', 'exception', 'warning']:
            raise ValueError("Wrong `typ' parameter")

        if self.fileobj is None:
            raise Exception("Log output file object is None")

        if timestamp is not None:
            pass
        else:
            timestamp = wayround_org.utils.time.currenttime_stamp_iso8601()

        log_name = self.logname
        if self.longest_logname is not None:
            log_name += ' ' * (self.longest_logname - len(self.logname) - 1)

        icon = 'i'
        if typ == 'info':
            icon = 'i'
        elif typ == 'error':
            icon = 'e'
        elif typ == 'exception':
            icon = 'E'
        elif typ == 'warning':
            icon = 'w'
        else:
            icon = '?'

        msg2 = "[{}] [{:26}] [{}] {}".format(
            icon,
            timestamp,
            log_name,
            text
            )

        msg2_scn = "\033[0;1m[{}] [{:26}] [{}]\033[0m {}".format(
            icon,
            timestamp,
            log_name,
            text
            )

        if icon != 'i':
            msg2_scn = "\033[0;1m[\033[0m\033[0;4m\033[0;5m{}\033[0m\033[0;1m] [{:26}] [{}]\033[0m {}".format(
                icon,
                timestamp,
                log_name,
                text
                )

        with self._write_lock:
            self.fileobj.write(msg2 + '\n')
            self.fileobj.flush()
            if echo:
                sys.stderr.write(msg2_scn + '\n')
                sys.stderr.flush()
        return

    def error(self, text, echo=True, timestamp=None):
        self.write(text, echo=echo, typ='error', timestamp=timestamp)
        return

    def exception(self, text, echo=True, timestamp=None, tb=True):
        # EXCEPTION TEXT:
        ei = wayround_org.utils.error.return_instant_exception_info(
            tb=tb
            )
        ttt = """\
{text}
{ei}
""".format(text=text, ei=ei)

        self.write(ttt, echo=echo, typ='exception', timestamp=timestamp)
        return

    def info(self, text, echo=True, timestamp=None):
        self.write(text, echo=echo, typ='info', timestamp=timestamp)
        return

    def warning(self, text, echo=True, timestamp=None):
        self.write(text, echo=echo, typ='warning', timestamp=timestamp)
        return
