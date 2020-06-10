from datetime import datetime
from datetime import timedelta

def getTimeObj(string):
	return datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f')

def time_delta_format(timedelta):
    return "Day: "+ str(timedelta.days)+ ", Heures: "+ str(timedelta.seconds//3600) +", Minutes: " + str((timedelta.seconds//60)%60)

def print_dict(dictionary):
	print_str = []
	for key in dictionary:
		print_str.append(str(key)+' -> '+time_delta_format(dictionary[key]))

def dashboard():
	work_time_dictionary  = dict()
	f= open("./Persistence/Work.csv","r")
	Lines = f.readlines()[1:]
	for line in Lines:
		array = line.split(", ")
		if array[0] in work_time_dictionary:
			work_time_dictionary[array[0]] += getTimeObj(array[2]) - getTimeObj(array[1])
		else:
			work_time_dictionary[array[0]] = getTimeObj(array[2]) - getTimeObj(array[1])

	return print_dict(work_time_dictionary)
