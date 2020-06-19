from datetime import datetime
from datetime import timedelta
from math import ceil

def getTimeObj(string):
	return datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f')

def time_delta_format(timedelta):
	hours_in_a_week = 168 * 60 * 60
	e20_semester_start = datetime(2020, 4, 27)

	weeks_since_semester_start = ceil((datetime.today().timestamp() - e20_semester_start.timestamp()) / hours_in_a_week)
	hours = timedelta.days * 24 + timedelta.seconds//3600

	return "Heures: " + str(hours) + ", Minutes: " + str((timedelta.seconds//60)%60) + ", Moyenne par semaine: " + str(round(hours/weeks_since_semester_start, 2))

def print_dict(dictionary):
	print_str = []
	for key in dictionary:
		print_str.append(str(key)+' -> '+time_delta_format(dictionary[key]))
	return print_str

def dashboard():
	work_time_dictionary  = dict()
	f = open("./Persistence/Work.csv","r")
	lines = f.readlines()[1:]
	for line in lines:
		array = line.split(", ")
		if array[0] in work_time_dictionary:
			work_time_dictionary[array[0]] += getTimeObj(array[2]) - getTimeObj(array[1])
		else:
			work_time_dictionary[array[0]] = getTimeObj(array[2]) - getTimeObj(array[1])

	return print_dict(work_time_dictionary)