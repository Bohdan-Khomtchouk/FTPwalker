# -*- coding: utf-8 -*-

"""
    This module is used to fork the current process into a daemon.
    Almost none of this is necessary (or advisable) if your daemon
    is being started by inetd. In that case, stdin, stdout and stderr are
    all set up for you to refer to the network connection, and the fork()s
    and session manipulation should not be done (to avoid confusing inetd).
    Only the chdir() and umask() steps remain as useful.
    References:
        UNIX Programming FAQ
            1.7 How do I get my program to act like a daemon?
                http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        Advanced Programming in the Unix Environment
            W. Richard Stevens, 1992, Addison-Wesley, ISBN 0-201-56317-7.

    History:
      2001/07/10 by Jürgen Hermann
      2002/08/28 by Noah Spurrier
      2003/02/24 by Clark Evans
      2016/09/14 by Kasra A. Vand

Also see: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012
"""


import sys
import os
import time
from signal import SIGTERM


def deamonize(stdout='/dev/null', stderr=None, stdin='/dev/null',
              pidfile=None, startmsg='started with pid {}'):
    """
        This forks the current process into a daemon.
        The stdin, stdout, and stderr arguments are file names that
        will be opened and be used to replace the standard file descriptors
        in sys.stdin, sys.stdout, and sys.stderr.
        These arguments are optional and default to /dev/null.
        Note that stderr is opened unbuffered, so
        if it shares a file with stdout then interleaved output
        may not appear in the order that you expect.
    """
    # Do first fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit first parent.
    except OSError as exc:
        sys.stderr.write("fork #1 failed: ({}) {}\n".format(exc.errno, exc.strerror))
        sys.exit(1)

    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid()

    # Do second fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit second parent.
    except OSError as exc:
        print(exc)
        sys.stderr.write("fork #2 failed: ({}) {}\n".format(exc.errno, exc.strerror))
        sys.exit(1)

    # Open file descriptors and print start message
    if not stderr:
        stderr = stdout
    # with open(stdin, 'rb') as si, open(stdout, 'ab+') as so, open(stderr, 'ab+', 0) as se:
    pid = str(os.getpid())
    sys.stderr.write("\n{}\n".format(startmsg.format(pid)))
    sys.stderr.flush()
    if pidfile:
        with open(pidfile, 'w+') as f:
            f.write("{}\n".format(pid))
        # Redirect standard file descriptors.
        # sys.stdout.flush()
        # sys.stderr.flush()
        # os.dup2(si.fileno(), sys.stdin.fileno())
        # os.dup2(so.fileno(), sys.stdout.fileno())
        # os.dup2(se.fileno(), sys.stderr.fileno())

def startstop(stdout='/dev/null', stderr=None, stdin='/dev/null',
              pidfile='pid.txt', startmsg='started with pid {}'):
    if len(sys.argv) > 1:
        action = sys.argv[1]
        try:
            with open(pidfile) as pf:
                pid = int(pf.read().strip())
        except (IOError, ValueError):
            pid = None
        if 'stop' == action or 'restart' == action:
            if not pid:
                mess = "Could not stop, pid file '{}' missing.\n"
                sys.stderr.write(mess.format(pidfile))
                sys.exit(1)
            try:
                while 1:
                    os.kill(pid, SIGTERM)
                    time.sleep(1)
            except OSError as exc:
                exc = str(exc)
                if exc.find("No such process") > 0:
                    os.remove(pidfile)
                    if 'stop' == action:
                        sys.exit(0)
                    action = 'start'
                    pid = None
                else:
                    print(str(exc))
                    sys.exit(1)
        elif 'start' == action:
            if pid:
                mess = "Start aborded since pid file '{}' exists.\n"
                sys.stderr.write(mess.format(pidfile))
                sys.exit(1)
            deamonize(stdout, stderr, stdin, pidfile, startmsg)
            return
    print("usage: {} start|stop|restart".format(sys.argv[0]))
    sys.exit(2)

def test():
    """
        This is an example main function run by the daemon.
        This prints a count and timestamp once per second.
    """
    sys.stdout.write('Message to stdout...')
    sys.stderr.write('Message to stderr...')
    c = 0
    while True:
        sys.stdout.write('{}: {}\n'.format(c, time.ctime(time.time())))
        sys.stdout.flush()
        c = c + 1
        time.sleep(1)

if __name__ == "__main__":
    startstop(stdout='/tmp/deamonize.log',
              pidfile='/tmp/deamonize.pid')
    test()
