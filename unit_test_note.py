import pickle_helper as pkl
import json

#Guillaume Dumont, 2020

#works if at least one note is already entered
def main():
	grille_ancienne = pkl.load_obj("grille")
	for index_cours, cours in enumerate(grille_ancienne):
		for index_evaluation, evaluation in enumerate(cours["evaluations"]):
			if(evaluation["avg"] != None):
				evaluation["avg"] = None
	with open('data.json', 'w') as outfile:
		json.dump(grille_ancienne, outfile)			
	pkl.save_obj(grille_ancienne, "grille")
	
main()