# Work with Python 3.6
import discord
import os.path
from os import path
import functions as func
import pickle_helper as pkl
import get_nouvelle_note as note
import time
import threading
import asyncio
import signal
import credentials_helper as creds

#Guillaume Dumont, 2020

TOKEN = creds.get_token()
client = discord.Client()
bot_control_channel_id = creds.get_bot_control_id()
new_note_channel_id = creds.get_new_notes_id() 

async def sendMessage(id_channel, msg):
	channel = client.get_channel(id_channel)
	await channel.send(msg)


def aviser_les_boys_sur_discord(nouvelles_notes, loop):
	if(nouvelles_notes != []):
		msg = "On a une ou des notes de sorties pour les cours suivant \n"
		msg += func.CreateListMessage(nouvelles_notes)  
		print("New note found")
		try:
			loop.run_until_complete(sendMessage(new_note_channel_id, msg))
			loop.close()   
			pass
		except:
			pass

class NoteThread(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.loop = asyncio.get_event_loop()
		self.threadID = threadID
		self.name = name
		self.exit = False
		self.grille_ancienne = None
		signal.signal(signal.SIGINT, self.exit)

	def close(self):
		self.exit = True

	def run(self):
		try:
			self.grille_ancienne = pkl.load_obj("grille")
		except:
			pass
		while(not self.exit):
			grille_actuelle = note.get_grille_de_note(creds.get_username(), creds.get_password())
			if(self.grille_ancienne == None):
				self.grille_ancienne = grille_actuelle
				pkl.save_obj(self.grille_ancienne, "grille" )
			else:
				nouvelles_notes = note.check_for_nouvelles_notes(
					grille_actuelle, self.grille_ancienne)
				aviser_les_boys_sur_discord(nouvelles_notes, self.loop)
				self.grille_ancienne = grille_actuelle
				if (nouvelles_notes != []):
					pkl.save_obj(self.grille_ancienne, "grille" )
			#dirty, but works well. Used to not wait the thread on Ctrl+C (SIGINT)
			i = 0
			while(not self.exit and i < note.refresh_time_in_sec): 
				time.sleep(1)
				i += 1


thread_for_notes = NoteThread(1, "Thread-1")


@client.event
async def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return
	channel = message.channel
	if message.content.startswith('!hello'):
		msg = 'Hello {0.author.mention}'.format(message)
		print(channel)
		print(channel.id)
		await channel.send(msg)
	#elif message.content.startswith('!disconnect'):
	#    if(message.author.id is admin):
	#        try:
	#            thread_for_notes.close()
	#        except:
	#            pass
	#        await channel.send("Alright! Je m'en vais!")
	#        await client.close()
	#    else:
	#        await channel.send("Nice try!")
	elif message.content.startswith('!play'):
		if(message.author.voice == None):
			await channel.send("T'es même pas connecté... Git Gud!")
		else:
			message_content = message.content.lower()
			audio_track = "E:/Bot/Jean-Michel/Audio/" + \
				message_content.replace('!play ', '')+".mp3"
			if(path.exists(audio_track)):
				voice_channel = client.get_channel(
					message.author.voice.channel.id)
				voice_client = await voice_channel.connect(reconnect=False)
				if voice_client != None:
					audio = discord.FFmpegPCMAudio(audio_track)
					voice_client.play(audio)
					while(voice_client.is_playing()):
						time.sleep(0.25)
						continue
					await voice_client.disconnect()
			else:
				if(message.content == '!play'):
					await channel.send("U Stupid!? Quel fichier tu veux que je joue?")
				else:
					await channel.send("Bro... ça existe ton fichier " + message.content.replace('!play ', '')+"!")
	elif message.content.startswith('!list'):
		await channel.send("Voici la liste des fichiers audios disponibles:")
		await channel.send(func.CreateListMessage(func.GetFilesFromFolder("./Audio")))
	elif message.content.startswith('!help'):
		await channel.send("You must be desperate to come to me for help...")
		actionList = ['!hello si tu te cherches un ami',
					'!play _nom de piste voulu_', '!list pour voir les pistes disponibles']
		await channel.send(func.CreateListMessage(actionList))
	elif message.content.startswith('!saucemepls'):
		await channel.send(func.WeirdGIFpourPhil())

def signal_handler(sig, frame):
	loop = asyncio.get_event_loop()
	try:
		print("Peace!")
		thread_for_notes.close()
		loop.run_until_complete(client.close())
		loop.close()
	except:
		pass   
		

@client.event
async def on_ready():
	print('Logged in as ' + client.user.name)
	channel = client.get_channel(bot_control_channel_id)
	try:
		if(os.name == 'nt'):
			print("Try load Windows Opus")
			discord.opus.load_opus('./Opus/libopus-0.dll')
		else:
			print("Try load Unix Opus")
			discord.opus.load_opus('libopus.so.1')
		print("discord.opus.is_loaded() = ", discord.opus.is_loaded())
		#await channel.send("Jean-Michel is back Fuckers!")
		thread_for_notes.start()
		signal.signal(signal.SIGINT, signal_handler)
		print("Jean-Michel is back online")
	except:
		print("discord.opus.is_loaded() = ", discord.opus.is_loaded())
		await client.close()

client.run(TOKEN)
