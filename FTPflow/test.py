from runwalker import FTPflow

# "Pasteur Insitute", "ftp.pasteur.fr"
walker = FTPflow("Pasteur Insitute", "ftp.pasteur.fr")
# "O-GLYCBASE", "ftp.cbs.dtu.dk"
walker.check_state()
