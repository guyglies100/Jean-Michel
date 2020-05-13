import json_encoder_helper as enc

#Guillaume Dumont, 2020

#I know this is not that safe, it's trust based on the server.

def get_token():
	return enc.decodeJsonPickle("creds.json")['token']

def get_username():
	return enc.decodeJsonPickle("creds.json")['username']

def get_password():
	return enc.decodeJsonPickle("creds.json")['password']

def get_bot_control_id():
	return enc.decodeJsonPickle("creds.json")['bot-control']

def get_new_notes_id():
	return enc.decodeJsonPickle("creds.json")['new-note']

def get_timer_channel_id():
	return enc.decodeJsonPickle("creds.json")['timer-channel']