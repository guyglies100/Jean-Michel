from os import listdir
from os.path import isfile, join
import random

#Guillaume Dumont, 2020

def GetFilesFromFolder(path):
	onlyfiles = [f.replace(".mp3", "") for f in listdir(path) if isfile(join(path, f))]
	return onlyfiles

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