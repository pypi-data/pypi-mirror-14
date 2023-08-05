# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 22:21:58 2016

@author: lpzjwp
"""


from pyosf import project, sync
import time
import os
from os.path import join
import json
import shutil

this_dir, filename = os.path.split(__file__)
tmp_folder = join(this_dir, "tests/tmp")
proj_file = join(this_dir, "tests/tmp", "test.proj")
proj_root = join(this_dir, "tmp", "files")


proj = project.Project(project_file=proj_file)
local_files= proj.local.create_index()
#print(json.dumps(local_files, indent=1))
dict_local = sync.dict_from_list(local_files, 'path')
print "********* local ********"
for entry in dict_local.keys():
    print entry

osf_files= proj.osf.create_index()
#print(json.dumps(osf_files, indent=1))
dict_osf = sync.dict_from_list(osf_files, 'path')
print "********* osf ********"
for entry in dict_osf.keys():
    print entry
