def sannitize(time_stirng):
	if '-' in time_stirng:
		splitter='-'
	elif ':' in time_stirng:
		splitter=':'
	else:
		return time_stirng
	(mins,secs)=time_stirng.split(splitter)
	return mins+'.'+secs