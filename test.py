from runwalker import ftpwalker

walker = ftpwalker("PairsDB", "nic.funet.fi", daemon=True)
walker.chek_state()
