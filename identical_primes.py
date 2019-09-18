import json
from os import listdir
from os.path import isfile, join
import os


base_dir = os.path.dirname(os.path.realpath(__file__))
tmp_dir = "%s/tmp/" % base_dir
id_group_dir = "%s/id_groups/" % tmp_dir
file_map = {}

for filename in listdir(tmp_dir):
	if not isfile(join(tmp_dir, filename)):
		continue

	f = open(join(tmp_dir, filename), "r")
	identifier = f.read()
	f.close()

	if identifier not in file_map:
		prime_sum = sum(json.loads(identifier))
		folder_name = "%d_%s" % (prime_sum, "".join([str(x) for x in json.loads(identifier)]))
		file_map[identifier] = {"id": folder_name, "files": []}
		os.mkdir("%s%s"%(id_group_dir, folder_name))
	else:
		print(filename, identifier)

	file_map[identifier]['files'].append(filename)


for identifier in file_map.keys():
	folder_name = file_map[identifier]['id']
	for filename in file_map[identifier]['files']:
		os.symlink("%s%s" % (tmp_dir, filename), "%s%s/%s"%(id_group_dir, folder_name, filename))
