import time_split
def for_list_sqlit(list_temp,list_append):
	for temp in list_temp:
		list_append.append(time_split.sannitize(temp))
	return list_append