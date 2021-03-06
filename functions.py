from os import listdir
from os.path import isfile, join
from os import path
import random
import subprocess
from datetime import datetime
from datetime import timedelta
import credentials_helper as cred
#Guillaume Dumont, 2020

def GetFilesFromFolder(path):
	onlyfiles = [f.replace(".mp3", "") for f in listdir(path) if isfile(join(path, f))]
	return sorted(onlyfiles)

def CreateListMessage(messageList):
	msg = ">>> "
	for str in messageList:
		msg += str + "\n"
	return msg

def WeirdGIFpourPhil():
	gifs = []
	gifs.append("https://tenor.com/view/kid-what-awkward-uh-no-gif-11504117")
	gifs.append("https://tenor.com/view/sausage-fest-hot-dog-gif-14785205")
	gifs.append("https://tenor.com/view/baby-infant-toddler-sour-are-you-kidding-me-gif-5490119")
	gifs.append("https://tenor.com/view/uncomfortable-drinking-thirsty-gif-13676825")
	gifs.append("https://tenor.com/view/suck-funny-gif-8541269")
	gifs.append("https://tenor.com/view/confused-what-huh-gif-13526427")
	gifs.append("https://tenor.com/view/morgan-freeman-im-done-oh-lord-oh-no-gif-12461195")
	gifs.append("https://tenor.com/view/disgusted-appalled-colin-farrell-gif-14505530")
	gifs.append("https://tenor.com/view/mad-cats-cat-kitten-kitty-gif-16783314")
	gifs.append("https://tenor.com/view/michael-scott-the-office-angry-unimpressed-not-in-the-mood-gif-3579004")
	gifs.append("https://tenor.com/view/hopeless-disappointed-ryan-reynolds-facepalm-embarrassed-gif-5436796")
	gifs.append("https://tenor.com/view/shook-shocked-gif-10048986")
	gifs.append("https://tenor.com/view/peasant-joke-rich-understand-funny-horrible-histories-gif-15537482")
	gifs.append("https://tenor.com/view/baby-vomitando-bebe-puke-vomit-gif-14250810")
	gifs.append("https://tenor.com/view/disgust-clint-eastwood-gif-5045246")
	gifs.append("https://tenor.com/view/oh-fuck-off-go-away-just-go-leave-me-alone-spicy-wings-gif-14523970")
	gifs.append("https://tenor.com/view/sausage-party-dinner-sauce-angry-gif-13271811")
	gifs.append("https://tenor.com/view/too-much-sauce-gif-7649820")
	gifs.append("https://tenor.com/view/extra-extra-sauce-oprah-sauce-crazy-gif-7296069")
	gifs.append("https://tenor.com/view/szechuan-sauce-rick-and-morty-gif-8476237")
	gifs.append("https://tenor.com/view/vldl-viva-la-dirt-league-bro-brother-pal-gif-16079539")
	r = random.randint(0, len(gifs)-1)
	return gifs[r]

def log(msg):
	f= open("bot.log","a")
	f.write(str(msg) + "\n")
	f.close()

def init_log():
	f= open("bot.log","w")
	f.close()

def print_to_csv(work_tuple):
	if(not path.exists("./Persistence/Work.csv")):
		f= open("./Persistence/Work.csv","w")
		f.write("member, start, finish, desc\n")
		f.close()
	f= open("./Persistence/Work.csv","a")
	len_tupple = len(work_tuple)
	for x in range(len_tupple):
		f.write(str(work_tuple[x]))
		if(x != len_tupple-1):
			f.write(", ")
	f.write('\n')
	f.close()
	
def get_version():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()


#Expected XXHXXMin
def handle_time_message(msg):
	lower_msg = msg.lower()
	index_hours = lower_msg.find('h')
	hours = 0
	minutes = 0
	if(index_hours != -1):
		hours = int(lower_msg[:index_hours])
	

	index_mins = lower_msg.find('m')
	if(index_mins != -1):
		minutes= int(msg[index_hours + 1:index_mins])
	
	print(hours)
	print(minutes)
	date = datetime.now()
	date_with_delta = datetime.now()

	if (hours > 0 or minutes > 0 ):
		delta = timedelta(
			minutes=minutes,
			hours=hours
		)
		date_with_delta = date - delta
	return date, date_with_delta

def get_time_to_add_and_desc(msg):
	msg_array = msg.split(' ', 1)
	if(len(msg_array) != 2):
		raise ValueError("Format non valide, devrait être !commande XXHXXM description")
	try:
		date, date_with_delta = handle_time_message(msg_array[0])
	except:
		raise ValueError("Format non valide, devrait être !commande XXHXXM description")		
	desc = msg_array[1]
	if(date == date_with_delta):
		raise ValueError("Format non valide, devrait être !commande XXHXXM description")
	return date, date_with_delta, desc
