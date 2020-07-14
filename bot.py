# Work with Python 3.6
import discord
import os.path
from os import path
import functions as func
import pickle_helper as pkl
import get_nouvelle_note as note
import dashboard
import time
import threading
import asyncio
import signal
import credentials_helper as creds
from datetime import datetime
import text_to_speech
#Guillaume Dumont, 2020

TOKEN = creds.get_token()
client = discord.Client()
bot_control_channel_id = creds.get_bot_control_id()
new_note_channel_id = creds.get_new_notes_id() 
work_time_dictionary  = dict()

async def sendMessage(id_channel, msg):
	channel = client.get_channel(id_channel)
	await channel.send(msg)


def aviser_les_boys_sur_discord(nouvelles_notes, loop):
	if(nouvelles_notes != []):
		msg = "On a une ou des notes de sorties pour les cours suivant \n"
		msg += func.CreateListMessage(nouvelles_notes)  
		func.log("New note found")
		try:
			send_fut = asyncio.run_coroutine_threadsafe(sendMessage(new_note_channel_id, msg), loop)
			send_fut.result()		
		except Exception as ex:
			print("Aviser les boys exception: " + ex.args[0])
			pass

class NoteThread(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		func.log("Starting NoteThread "+ name)
		self.loop = asyncio.get_event_loop()
		self.threadID = threadID
		self.name = name
		self.exit = False
		self.grille_ancienne = None
		signal.signal(signal.SIGINT, self.exit)

	def close(self):
		func.log("Closing NoteThread "+ self.name)
		self.exit = True

	def run(self):
		func.log("Running NoteThread "+ self.name)
		try:
			self.grille_ancienne = pkl.load_obj("grille")
		except:
			func.log("except while loading old grille")
			pass
		func.log("Running NoteThread suite "+ self.name)
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
	author = str(message.author)
	if message.content.startswith('!hello'):
		msg = 'Hello {0.author.mention}'.format(message)	
		await channel.send(msg)
	elif message.content.startswith('!work') and func.is_work_member(author):
		if message.author in work_time_dictionary:
			old_tuple = work_time_dictionary[message.author]
			work = message.content.replace('!work ', '')
			work_time_dictionary[message.author] = (old_tuple[0], old_tuple[1], old_tuple[2], work)
			await channel.send("C'est noté")
		else:
			await channel.send("T'es pas en session de travail présentement")
	elif message.content.startswith('!csv') and func.is_work_member(author):
		if(path.exists("./Persistence/Work.csv")):
			file_to_send = discord.File(open("./Persistence/Work.csv","rb"))
			await channel.send("Keep up the good work", file=file_to_send)
			file_to_send.close()
		else:
			await channel.send("Aucun csv n'a été créé pour le moment")
	elif message.content.startswith('!dashboard') and func.is_work_member(author):
		if(path.exists("./Persistence/Work.csv")):
			await channel.send("Voici les statistiques calculées par JM")
			await channel.send(func.CreateListMessage(dashboard.dashboard()))
		else:
			await channel.send("Aucun csv n'a été créé pour le moment")
	elif message.content.startswith('!version'):
		try:
			await channel.send("JM est présentement au commit: " + func.get_version())
		except:
			await channel.send("Git n'est pas disponible...")
	elif message.content.startswith('!member'):
		func.log(message.author)
		if func.is_work_member(author):
			await channel.send("Tu as accès aux fonctions de travail.")
		else: 
			await channel.send("Tu n'as pas accès aux fonctions de travail.")
	elif message.content.startswith('!what is my purpose'):
		msg = 'https://www.youtube.com/watch?v=wqzLoXjFT34'.format(message)	
		await channel.send(msg)
	elif message.content.startswith('!time') and func.is_work_member(author):
		work = message.content.replace('!time ', '')
		try:
			date, date_delta, desc = func.get_time_to_add_and_desc(work)
			tuple_time = (message.author, date_delta, date, "MANUAL_TIME["+desc+"]")
			func.print_to_csv(tuple_time)
			await channel.send("Temps ajouté!")			
		except ValueError as err:
			await channel.send("Format non valide, devrait être !commande XXHXXM description")
	elif message.content.startswith('!quote'):
		if(message.author.voice == None):
			await channel.send("T'es même pas connecté... Git Gud!")
		else:
			text = message.content.replace('!quote ', '')
			audiofile = text_to_speech(text)
			voice_channel = client.get_channel(message.author.voice.channel.id)
			voice_client = await voice_channel.connect(reconnect=False)
			if voice_client != None:
				audio = discord.FFmpegPCMAudio(audiofile)
				voice_client.play(audio)
				while(voice_client.is_playing()):
					time.sleep(0.25)
					continue
				await voice_client.disconnect()
		
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
			audio_track = "./Audio/" + \
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
					'!play _nom de piste voulu_', 
					'!list pour voir les pistes disponibles',
					'!work pour décrire ta session de travail, si elle existe',
					'!csv envoye le csv de travail',
					'!version pour voir la version déployée',
					'!dashboard pour avoir le nombre d\'heure des membres de UNC-I',
					'!time pour ajouter manuellement du temps de travail, devrait être !time XXHXXM description',
					'!member dit si tu es un membre de l\'équipe de travail'
					]
		await channel.send(func.CreateListMessage(actionList))
	elif message.content.startswith('!saucemepls'):
		await channel.send(func.WeirdGIFpourPhil())

def signal_handler(sig, frame):
	loop = asyncio.get_event_loop()
	try:
		func.log("Peace!")
		thread_for_notes.close()
		loop.run_until_complete(client.close())
		loop.close()
	except:
		pass   
		

@client.event
async def on_ready():
	func.log('Logged in as ' + client.user.name)
	channel = client.get_channel(bot_control_channel_id)
	try:
		if(os.name == 'nt'):
			func.log("Try load Windows Opus")
			discord.opus.load_opus('./Opus/libopus-0.dll')
		else:
			func.log("Try load Unix Opus")
			discord.opus.load_opus('libopus.so')
		func.log("discord.opus.is_loaded() = " + str(discord.opus.is_loaded()))
		#await channel.send("Jean-Michel is back!")
		thread_for_notes.start()
		signal.signal(signal.SIGINT, signal_handler)
		func.log("Jean-Michel is back online")
	except:
		func.log("discord.opus.is_loaded() = " + str(discord.opus.is_loaded()))
		await client.close()

@client.event
async def on_voice_state_update(member, before, after):
	if member == client.user or before.channel == after.channel:
		return

	timer_channel_id = creds.get_timer_channel_id()
	before_id = 0 if before.channel == None else before.channel.id
	after_id = 0 if after.channel == None else after.channel.id
	
	if(after_id == timer_channel_id):
		#user connected
		work_time_dictionary[member] = (member, datetime.now(), None, "")
	if(before_id == timer_channel_id):
		if member in work_time_dictionary:
			old_tuple = work_time_dictionary[member]
			work_time_dictionary[member] = (member, old_tuple[1], datetime.now(), old_tuple[3])
			func.print_to_csv(work_time_dictionary[member])
			work_time_dictionary.pop(member)

		func.log(member);
		func.log(before);
		func.log(after);

func.init_log()
client.run(TOKEN)