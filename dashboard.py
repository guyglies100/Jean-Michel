from datetime import datetime
from datetime import timedelta
from math import ceil

semester_start = datetime(2021, 1, 11)

def getTimeObj(string):
    return datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f')

def time_delta_format(timedelta):
    hours_in_a_week = 168 * 60 * 60
    global semester_start

    weeks_since_semester_start = ceil((datetime.today().timestamp() - semester_start.timestamp()) / hours_in_a_week)
    hours = timedelta.days * 24 + timedelta.seconds//3600

    return "Heures: " + str(hours) + ", Minutes: " + str((timedelta.seconds//60)%60) + ", Moyenne par semaine: " + str(round(hours/weeks_since_semester_start, 2))

def print_dict(dictionary, weekly):
    print_str = []
    for key in dictionary:
        string = str(key)+' -> '+time_delta_format(dictionary[key])
        if(key in weekly):
            timedelta = weekly[key]
            hours = timedelta.days * 24 + timedelta.seconds//3600
            minutes = (timedelta.seconds//60)%60
            string += ", Depuis lundi: " + str(hours) + "h" + str(minutes) + "min"
        print_str.append(string)
    return print_str

def get_most_recent_sprint_start_weekday():
    return get_last_monday()

def get_last_wednesday():
    return get_last_weekday(2)

def get_last_monday():
    return get_last_weekday(0)

def get_last_weekday(weekdayOffset):
    today = datetime.today()
    offset = (today.weekday() - weekdayOffset) % 7
    last_weekday = today - timedelta(days=offset)
    last_weekday = datetime(year = last_weekday.year, month = last_weekday.month, day = last_weekday.day)
    return last_weekday

def dashboard():
    work_time_dictionary  = dict()
    work_time_weekly_dictionary  = dict()
    f = open("./Persistence/Work.csv","r")
    lines = f.readlines()[1:]

    global semester_start

    for line in lines:
        array = line.split(", ")

        if getTimeObj(array[1]) < semester_start or getTimeObj(array[2]) < semester_start:
            continue

        if array[0] in work_time_dictionary:
            work_time_dictionary[array[0]] += getTimeObj(array[2]) - getTimeObj(array[1])
        else:
            work_time_dictionary[array[0]] = getTimeObj(array[2]) - getTimeObj(array[1])

        if(getTimeObj(array[1]) > get_most_recent_sprint_start_weekday()):
            if array[0] in work_time_weekly_dictionary:
                work_time_weekly_dictionary[array[0]] += getTimeObj(array[2]) - getTimeObj(array[1])
            else:
                work_time_weekly_dictionary[array[0]] = getTimeObj(array[2]) - getTimeObj(array[1])
        elif(getTimeObj(array[1]) < get_most_recent_sprint_start_weekday() and getTimeObj(array[2]) > get_most_recent_sprint_start_weekday()):
            if array[0] in work_time_weekly_dictionary:
                work_time_weekly_dictionary[array[0]] += getTimeObj(array[2]) - get_most_recent_sprint_start_weekday()
            else:
                work_time_weekly_dictionary[array[0]] = getTimeObj(array[2]) - get_most_recent_sprint_start_weekday()
    return print_dict(work_time_dictionary, work_time_weekly_dictionary)