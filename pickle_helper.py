import pickle
import os

#Étienne Lepage-Lepitre

def save_obj(obj, name):
    #print(obj)
    with open("./" + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    if os.path.isfile("./" + name + '.pkl'):
        with open("./" + name + '.pkl', 'rb') as f:
            return pickle.load(f)
    return None