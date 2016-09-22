"""
===== 
walker.py 
===== 



Documentation created using SimpleRST. Source: https://github.com/Kasramvd/SimpleRST

============================

"""

from os import path as ospath


class ftp_walker(object):
    """
    ==============

    ``ftp_walker``
    ----------

    .. py:class:: ftp_walker()



       :rtype: UNKNOWN

    .. note::

    Example

    .. code-block:: python
	

    .. todo::
    """
    def __init__(self, connection):
        """
        .. py:attribute:: __init__()


           :param connection:
           :type connection:
           :rtype: UNKNOWN

        .. note::

        Example

        .. code-block:: python
	

        .. todo::
        """
        self.connection = connection

    def listdir(self, _path):
        """
        .. py:attribute:: listdir()


           :param _path:
           :type _path:
           :rtype: UNKNOWN

        .. note::

        Example

        .. code-block:: python
	

        .. todo::
        """
        file_list, dirs, nondirs = [], [], []
        try:
            self.connection.cwd(_path)
        except Exception as exp:
            print ("the current path is : ", self.connection.pwd(), exp.__str__(), _path)
            return [], []
        else:
            self.connection.retrlines('LIST', lambda x: file_list.append(x.split()))
            for info in file_list:
                ls_type, name = info[0], info[-1]
                if ls_type.startswith('d'):
                    dirs.append(name)
                else:
                    nondirs.append(name)
            return dirs, nondirs

    def Walk(self, path='/'):
        """
        .. py:attribute:: Walk()


           :param path:
           :type path:
           :rtype: UNKNOWN

        .. note::

        Example

        .. code-block:: python
	

        .. todo::
        """
        dirs, nondirs = self.listdir(path)
        yield path, dirs, nondirs
        print ((path, dirs))
        for name in dirs:
            path = ospath.join(path, name)
            for x in self.Walk(path):
                yield x
            self.connection.cwd('..')
            path = ospath.dirname(path)
