from os import path
import pickle_helper as pkl
import json

#Guillaume Dumont, 2020

#outputs a name.enc file
def encodeJsonPickle(name):
	if(path.exists(name)):
		data = open(name, "r").read()
		file_obj = json.loads(data)
		pkl.save_obj(file_obj, name)
	else:
		raise FileNotFoundError() 

#decode and return de values
def decodeJsonPickle(name):
	if(path.exists(name + ".pkl")):
		data = pkl.load_obj(name)
		return data	
	else:
		raise FileNotFoundError("file "+name+".pkl not found")

def replace_value(field, value):
	t = decodeJsonPickle("creds.json")
	t[field] = value
	pkl.save_obj(t, "creds.json")