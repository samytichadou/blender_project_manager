################## recuperer les arguments de la ligne de commande
# ta commande doit ressembler a ça :

blender fichier.blend -P script.py -- foo bar 7

# dans script.py tu fais ça :
import sys

def get_args() :
	""" recupere tout les arguments de la ligne de commande apres -- """
	ag  = [] ; add = False
	for a in sys.argv :
		if add : ag.append(a)
		if a == '--' : add = True
	return(ag)

print(get_args())


############# La methode avec les variables d'environement

la commande doit ressembler a ça :
"name='salut'" blender fichier.blend -P script.py

# dans script.py
import os
print(os.getenv("name"))



############# La duplication de plans

def custom_duplicate() :
	scn    = bpy.context.scene
	snew   = []
	# offset = scn.bs_props.shot_offset
	sqs    = bpy.context.selected_sequences
	for s in sqs :
		for st in sqs : st.select = False
		s.select = True ; scn.sequence_editor.active_strip = s

		# si s (un strip selectionné) est un plan on fait un custom duplicate, sinon on duplique de maniere reguliere
		if Utils.check(s) :
			snew.append(shot_duplicator(s))
		else :
			bpy.ops.sequencer.duplicate()

		for st in bpy.context.selected_sequences : snew.append(st)

	# scn.bs_props.shot_offset   = offset
	for st in snew : st.select = True
	bpy.ops.transform.transform("INVOKE_DEFAULT")
