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






############## l'update de plan


###### PSEUDO CODE ##########
strip  = le plan du montage qu'on veut updater
st_scn = strip.scene

# pour recuperer le timing original
st = st_scn.frame_start
ed = st_scn.frame_end

# on calcule le nouveau timing a partir des handles du strip
nst, ned = get_new_timing(strip)

# on update le .blend du plan (en background)

# pour update le plan du montage, on commence par changer le timing de la scene linkée
st_scn.frame_end   = ned
st_scn.frame_start = nst

# ensuite methode triste , on rajoute la scene dans le montage pour avoir un strip avec la bonne durée
# puis on efface l'ancien et on fait genre rien n'a changé
new_strip = update_strip(strip)



############# MIX PSEUDO CODE AVEC SNIPPETS ####################

def update_strip(strip) :
	name        = strip.name
	strip.name += "_TMP"
	# instanciation de la scene
	seq = bpy.context.scene.sequence_editor.sequences.new_scene(
		scene   = strip.scene,
		name    = name ,
		channel = strip.channel , # pas sur que ça marche mais on y crois...
		frame_start = strip.frame_start,
		)

	# copie des custom props ....

	# on efface l'ancien plan ....
	bpy.context.scene.sequence_editor.sequences.remove(strip)
	return(seq)


def get_new_timing(strip) :
	# on calcule le nouveau timing a partir des handles du strip
	st_scn    = strip.scene
	offset    = shot.frame_offset_start - shot.frame_still_start
	start     = st_scn.frame_start      + offset
	end       = st_scn.frame_end        + shot.frame_still_end - shot.frame_offset_end
	return(start, end)

### MAIN
strip  = le plan du montage qu'on veut updater
st_scn = strip.scene
nst, ned = get_new_timing(strip)

if nst != st_scn.frame_start or ned != st_scn.frame_end :
	print("on update le timing !")
	# on update le .blend du plan (en background)

	# pour update le plan du montage, on commence par changer le timing de la scene linkée dans le .blend du montage
	st_scn.frame_end   = ned
	st_scn.frame_start = nst

	# ensuite methode triste , on rajoute la scene dans le montage pour avoir un strip avec la bonne durée
	# puis on efface l'ancien et on fait genre rien n'a changé
	new_strip = update_strip(strip)