import main_walker
from os import path, makedirs, listdir
import shutil
import re
import argparse


class ftpwalker:
    def __init__(self, server_name, url, root='/'):
        self.name = re.sub(r'\W', '_', server_name)
        self.url = url
        try:
            server_path = path.join(path.dirname(__file__), self.name)
        except Exception as exc:
            raise Exception("Please enter a valid name. {}".format(exc))
        else:
            self.server_path = server_path
        self.m_walker = main_walker.main_walker(server_name=self.name,
                                                url=self.url,
                                                server_path=self.server_path,
                                                root=root)

    def chek_state(self):
        if path.isdir(self.server_path):
            if len(listdir(self.server_path)) > 0:
                self.path_exit()
            else:
                self.path_not_exit(False)
        else:
            self.path_not_exit(True)

    def path_exit(self):
        while True:
            answer = input("""It seems that you've already
                started traversing a server with this name.
                Do you want to continue with current one(Y/N)?: """)
            if answer.strip().lower() in {'y', 'yes'}:
                print("Start resuming the {} server...".format(self.name))
                self.m_walker.Process_dispatcher(True)
                break
            elif answer.strip().lower() in {'n', 'no'}:
                # deleting the directory
                shutil.rmtree(self.server_path)
                self.m_walker.Process_dispatcher(False)
                break
            else:
                print("Answer with (Y/N).")

    def path_not_exit(self, create_dir):
        # create the directory
        if create_dir:
            makedirs(self.server_path)
        self.m_walker.Process_dispatcher(False)


if __name__ == "__main__":
    description = "walk through FTP server's directory tree. Use -h or --help for help menu."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-N", "-name", help="The name of server.")
    parser.add_argument("-U", "-url", help="The server url.")
    parser.add_argument("-R",
                        "-root",
                        help="The root path for start the traversing.",
                        default='/')
    args = parser.parse_args()
    name = args.N
    url = args.U
    root = args.R
    fw = ftpwalker(name, url, root)
    fw.chek_state()
