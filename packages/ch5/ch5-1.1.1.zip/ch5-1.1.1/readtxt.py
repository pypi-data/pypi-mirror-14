import os
def filedir(filename,filepath):
	os.chdir(filepath)
	with open (filename) as temp_list:
		data = temp_list.readline()
		fileobj=data.strip().split(',')
	return fileobj