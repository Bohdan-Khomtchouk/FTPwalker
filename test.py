from FTPwalker.runwalker import ftpwalker


walker = ftpwalker("Uniprot", "ftp.uniprot.org")

walker.check_state()
