"""
=====
traverse.py
=====

This module is responsible for dispatching the threads between subdirectories.

============================

"""

from . import walker
import ftplib
from multiprocessing import Manager
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
import socket
from os import path as ospath, listdir
from collections import deque
import csv


class Run(object):
    """
    ==============

    ``Run``
    ----------

    .. py:class:: Run()

    Main class for threads dispatcher.

    """
    def __init__(self, name, server_url, root, server_path, resume):
        """
        .. py:attribute:: __init__()


           :param server_name: name of server
           :type server_name: str
           :param url: server's url
           :type url: str
           :param root: traversing start root
           :type root: str
           :param server_path: corresponding path for saving temporary files
           :type server_path: str
           :param resume: resume flag for resuming the traversing
           :type resume: bool
           :rtype: None

        """
        m = Manager()
        self.all_path = m.Queue()
        self.server_url = server_url
        self.root = root
        self.name = name
        self.server_path = server_path
        self.resume = resume

    def find_leading(self, top, thread_flag=True):
        """
        .. py:attribute:: find_leading()


           :param top: The top root for starting the traversing
           :type top: str
           :param thread_flag: shows if leadings are for threads or not
           :type thread_flag: boolean
           :rtype: tuple

        """
        print ("Find leading...")
        length = 2
        conn = ftplib.FTP(self.server_url)
        conn.login()
        fw = walker.ftp_walker(conn)
        for p, dirs, files in fw.walk(top):
            length = len(dirs)
            base = [(p, files)]
            if length > 1:
                p = '/'.join(p.split('/')[1:])
                length = length
                return base, dirs
            elif thread_flag:
                return base, []
        return base, []
        conn.quit()

    def traverse_branch(self, args):
        """
        .. py:attribute:: traverse_branch()


           :param root: The root path for start traversing
           :type root: str
           :rtype: None

        """
        root, all_path = args
        try:
            connection = ftplib.FTP(self.server_url)
            connection.login()
            # connection.cwd(root)
        except Exception as exp:
            print ("Couldn't create the connections for thread {}".format(exp))
        else:
            # file_names = listdir(self.server_path)
            fw = walker.ftp_walker(connection, self.resume)
            if self.resume:
                walker_obj = fw.walk_resume(all_path, root)
                next(walker_obj)
            else:
                walker_obj = fw.walk(root)
            root_name = root.replace('/', '_')

            with open('{}/{}.csv'.format(self.server_path, root_name), 'a') as f:
                csv_writer = csv.writer(f)
                for _path, _, files in walker_obj:
                    # self.all_path.put((_path, files))
                    csv_writer.writerow([_path] + files)

                # csv_writer.writerow(("TRAVERSING_FINISHED",))
            connection.quit()

    def find_all_leadings(self, leadings):
        """
        .. py:attribute:: find_all_leadings()


           :param leadings: find all the leadings for all the subdirectories
           :type leadings: list
           :rtype: dict

        """
        return {path: self.find_leading(path) for path in leadings}

    def main_run(self, args):
        """
        .. py:attribute:: main_run()
        Run threads by passing a leading directory to `traverse_branch` function.

           :param args: a tuple contain root and another tuple contains base and
           leadings. The root is the path of parent directory (assigned to a process)
           base is a tuple contain the path of sub-directory and file names that are
           associated with.
           :type args: iterable
           :rtype: None

        """
        root, (base, leadings) = args
        print ('---' * 5, datetime.now(), '{}'.format(root), '---' * 5)
        try:
            # base, leadings = self.find_leading(root)
            # print("base and leadings for {} --> {}, {}".format(root, base, leadings))
            leadings = [ospath.join('/', root, i.strip('/')) for i in leadings]
            if leadings:
                if self.resume:
                    print("Resuming...")
                    leadings = self.find_latest_leadings(leadings)
                else:
                    leadings = [(i, None) for i in leadings]

                pool = ThreadPool()
                pool.map(self.traverse_branch, leadings)
                pool.close()
                pool.join()
            else:
                self.all_path.put(base[0])
        except (ftplib.error_temp, ftplib.error_perm, socket.gaierror) as exp:
            print(exp)

    def find_latest_leadings(self, leadings):
        for root in leadings:
            f_name = ospath.join(self.server_path, "{}.csv".format(root).replace('/', '_'))
            try:
                with open(f_name) as f:
                    csv_reader = csv.reader(f)
                    all_path = next(zip(*csv_reader))
            except FileNotFoundError:
                # file is empty or doesn't exist
                all_path = [root]
            finally:
                yield root, all_path
