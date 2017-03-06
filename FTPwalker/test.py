from runwalker import ftpwalker

# "Pasteur Insitute", "ftp.pasteur.fr"
walker = ftpwalker("Pasteur Insitute", "ftp.pasteur.fr")
# "O-GLYCBASE", "ftp.cbs.dtu.dk"
walker.check_state()
