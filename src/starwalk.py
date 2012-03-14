#!/usr/bin/env python
import os
import pymongo
from pymongo import Connection

conn = Connection(host='coltrane.lbl.gov')
c = conn.stardb.walk
# Note: Clear old data!
c.remove()

start = "/eliza3/starprod/picodsts/Run11/AuAu/19GeV/all"
base_meta = { 'run_year' : 2011, "atoms":"AuAu", "energy_GeV": 19,
          'magnetic_field_setups' : 'all' }
counter = 0
for dirpath, dirnames, filenames in os.walk(start, topdown=False):
    if not dirnames and filenames: # leaf
        meta = base_meta.copy()
        path = dirpath
        path, ts = os.path.split(path)
        meta["ts"] = int(ts)
        path , meta["foo"] = os.path.split(path)
        path, meta["bar"] = os.path.split(path)
        for f in filenames:
            words = f[:f.find(".")].split('_')
            meta["num"] = int(words[-1])
            meta["is_raw"] = words[-2]
            meta["ts"] = int(words[-3])
            meta["exp"] = '-'.join(words[:-4])
            meta["fullpath"] = os.path.join(dirpath, f)
            #print(meta)
            doc_id = c.insert(meta, manipulate=False)
            counter += 1
            if not(counter % 1000):
                print("Inserted {0:d} files".format(counter))
