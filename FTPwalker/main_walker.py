from multiprocessing import Pool
from . import traverse
from datetime import datetime
import json
from collections import OrderedDict
from os import path as ospath, listdir, mkdir
import csv


class main_walker:
    """
    ==============

    ``main_walker``
    ----------
    Main walker class.
    .. py:class:: main_walker()

    """
    def __init__(self, *args, **kwargs):
        """
        .. py:attribute:: __init__()

           :rtype: None
        """
        self.server_name = kwargs['server_name']
        self.url = kwargs['url']
        self.root = kwargs['root']
        self.server_path = kwargs['server_path']
        self.json_path = kwargs.get('json_path')
        self.meta_path = ospath.join(self.server_path, 'metadata.json')

    def Process_dispatcher(self, resume):
        """
        .. py:attribute:: Process_dispatcher()


           :param resume:
           :type resume:
           :rtype: None

        """
        run = traverse.Run(self.server_name,
                           self.url,
                           self.root,
                           self.server_path,
                           self.meta_path
                           resume)
        base, leadings = run.find_leading(self.root, thread_flag=False)
        path, _ = base[0]
        leadings = [ospath.join(path, i.strip('/')) for i in leadings]
        print ("Root's leadings are: ", leadings)

        all_leadings = run.find_all_leadings(leadings)
        lenght_of_subdirectories = sum(len(dirs) for _, (_, dirs) in all_leadings.items())
        print("{} subdirectories founded".format(lenght_of_subdirectories))
        with open(self.meta_path, 'w') as f:
            json.dump({'subdirectory_number': lenght_of_subdirectories}, f)
        try:
            pool = Pool()
            pool.map(run.main_run, all_leadings.items())
        except Exception as exp:
            print(exp)
        else:
            print ('***' * 5, datetime.now(), '***' * 5)
            with open(self.meta_path) as f:
                meta = json.load(f)
                traversed_subs = meta['traversed_subs']
                lenght_of_subdirectories = meta['subdirectory_number']
            if lenght_of_subdirectories == len(traversed_subs):
                main_dict = OrderedDict()
                for name in file_names:
                    with open(ospath.join(self.server_path, name)) as f:
                        csvreader = csv.reader(f)
                        for path_, *files in csvreader:
                            main_dict[path_] = files
                self.create_json(main_dict, self.server_name)
            else:
                print("Traversing isn't complete. Start resuming the {} server...".format(self.server_name))
                self.Process_dispatcher(resume)

    def create_json(self, dictionary, name):
        """
        .. py:attribute:: create_json()


           :param dictionary: dictionary of paths and files
           :type dictionary: dict
           :param name: server name
           :type name: str
           :rtype: None

        """
        try:
            with open("{}/{}.json".format(self.json_path, name), 'w') as fp:
                json.dump(dictionary, fp, indent=4)
        except:
            mkdir(self.json_path)
            with open("{}/{}.json".format(self.json_path, name), 'w') as fp:
                json.dump(dictionary, fp, indent=4)