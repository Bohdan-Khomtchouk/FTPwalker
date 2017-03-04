from multiprocessing import Pool
import traverse
from datetime import datetime
import json
from collections import OrderedDict, deque
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
        if not self.json_path:
            self.json_path = self.server_path
        self.meta_path = ospath.join(ospath.dirname(self.server_path), 'metadata.json')
        self.run_object = None

    def find_leading_dirs(self, top):
        base, leadings = self.run_object.find_leading(top, thread_flag=False)
        _path, files = base[0]
        # Preserve the current directory path and files before deviding them between
        # threads and processors.
        with open('{}/{}.csv'.format(self.server_path, "leading_ftpwalker"), 'a+') as f:
            csv_writer = csv.writer(f)
            try:
                # self.all_path.put((_path, files))
                csv_writer.writerow([_path] + files)
            except:
                pass

        leadings = [ospath.join(_path, i.strip('/')) for i in leadings]
        return leadings

    def Process_dispatcher(self, resume):
        """
        .. py:attribute:: Process_dispatcher()


           :param resume:
           :type resume:
           :rtype: None

        """
        self.run_object = traverse.Run(self.server_name,
                                       self.url,
                                       self.root,
                                       self.server_path,
                                       self.meta_path,
                                       resume)
        if resume:
            # If resume is valid, this means that there is a file within server_path
            # directory which can be any of leading directories or the leading_ftpwalker
            leadings = self.find_latest_leadings()
            all_leadings = self.run_object.find_all_leadings(leadings)
        else:

            while True:
                leadings = self.find_leading_dirs(self.root)
                if len(leadings) == 0:
                    print("Empty directory!")
                    return
                if len(leadings) == 1:
                    top = leadings[0]
                    leadings = self.find_leading_dirs(top)
                elif len(leadings) > 1:
                    break

            print ("Root's leadings are: ", leadings)

            all_leadings = self.run_object.find_all_leadings(leadings)
            lenght_of_subdirectories = sum(len(dirs) for _, (_, dirs) in all_leadings.items())
            print("{} subdirectories founded".format(lenght_of_subdirectories))
            all_file_names = [i.replace('/', '_')for _, (_, leads) in all_leadings.items() for i in leads]
            with open(self.meta_path, 'w') as f:
                json.dump({'subdirectory_number': lenght_of_subdirectories,
                           'traversed_subs': [],
                           'all_file_names': all_file_names}, f)
        try:
            pool = Pool()
            pool.map(self.run_object.main_run, all_leadings.items())
        except Exception as exp:
            raise
        else:
            print ('***' * 5, "finish traversing", '***' * 5)
            with open(self.meta_path) as f:
                meta = json.load(f)
                traversed_subs = meta['traversed_subs']
                lenght_of_subdirectories = meta['subdirectory_number']
            if lenght_of_subdirectories == len(traversed_subs) and lenght_of_subdirectories:
                main_dict = OrderedDict()
                file_names = listdir(self.server_path)
                for name in file_names:
                    with open(ospath.join(self.server_path, name)) as f:
                        csvreader = csv.reader(f)
                        for path_, *files in csvreader:
                            main_dict[path_] = files
                self.create_json(main_dict, self.server_name)
            elif lenght_of_subdirectories:
                print("Traversing isn't complete. Start resuming the {} server...".format(self.server_name))
                self.Process_dispatcher(resume)

    def find_latest_leadings(self):
        with open(self.meta_path) as f:
            meta = json.load(f)
            traversed_subs = meta['traversed_subs']
            all_file_names = meta['all_file_names']
            exist_files = listdir(self.server_path)
        for file_name in exist_files:
            # check if the directory is not traversed already
            if file_name not in traversed_subs:
                f_name = ospath.join(self.server_path, file_name)
                try:
                    with open(f_name) as f:
                        csv_reader = csv.reader(f)
                        lates_path = deque(csv_reader, maxlen=1).pop()[0].replace('_', '/')
                except IndexError:
                    # file is empty
                    lates_path = file_name.replace('_', '/')
                finally:
                    yield lates_path
        # yield non-traversed directories
        for f_name in set(all_file_names).difference(traversed_subs):
            yield file_name.replace('_', '/')

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