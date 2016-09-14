This module is used to fork the current process into a daemon.
Almost none of this is necessary (or advisable) if your daemon
is being started by inetd. In that case, stdin, stdout and stderr are
all set up for you to refer to the network connection, and the `fork()`s
and session manipulation should not be done (to avoid confusing inetd).
Only the `chdir()` and `umask()` steps remain as useful.
References:
       - UNIX Programming FAQ
           - 1.7 How do I get my program to act like a daemon?
               - http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
       - Advanced Programming in the Unix Environment
           - W. Richard Stevens, 1992, Addison-Wesley, ISBN 0-201-56317-7.

History:
      2001/07/10 by Jürgen Hermann
      2002/08/28 by Noah Spurrier
      2003/02/24 by Clark Evans
      2016/09/14 by Kasra A. Vand

## New feautures:

  - Support Python3.X
  - Run withn code
  - Use classes for more flexibility
