### PROCESS FUNCTIONS ###

# split string on spaces
def split_string_on_spaces(string, char_limit):
    lines = []
    words = string.split()

    line = ""
    for w in words:
        if len(line) < char_limit:
            line += w + " "
        else:
            line = line[:-1]
            lines.append(line)
            line = w + " "

    if line not in lines:    
        lines.append(line)
        
    return lines


### DRAWING FUNCTIONS ###

# help function
def draw_wiki_help(container, wikipage):
    container.operator('bpm.open_wiki_page', text="", icon='QUESTION').wiki_page = wikipage

# draw operator and help function
def draw_operator_and_help(container, operator_bl_idname, icon, wikipage):
    row = container.row(align=True)
    if icon != '':
        row.operator(operator_bl_idname, icon = icon)
    else:
        row.operator(operator_bl_idname)
    row.operator('bpm.open_wiki_page', text="", icon='QUESTION').wiki_page = wikipage

# draw all props for debug
def draw_debug(container, dataset):

    box = container.box()
    box.label(text = str(dataset.bl_rna.identifier) + ' - Be careful', icon='ERROR')

    for p in dataset.bl_rna.properties:
        if not p.is_readonly and p.identifier != 'name':
            row = container.row()
            row.prop(dataset, '%s' % p.identifier)

# draw next previous comment panel
def draw_next_previous_comment(container):

    row = container.row(align = True)

    op = row.operator("bpm.goto_next_previous_comment", text = "", icon = "TRIA_LEFT")
    op.next = False
    
    op = row.operator("bpm.goto_next_previous_comment", text = "", icon = "TRIA_RIGHT")
    op.next = True

    row.label(text = "Comments")

# comment function 
def draw_comment(container, comments, c_type, context):

    row = container.row(align=True)
    op = row.operator("bpm.add_comment", text="Add")
    op.comment_type = c_type
    op2 = row.operator("bpm.reload_comments", text = "", icon = "FILE_REFRESH")
    op2.comment_type = c_type
    #row.separator()
    draw_wiki_help(row, "Comments")

    bigcol = container.column(align=True)

    for c in comments:
        box = bigcol.box()
        col = box.column(align=True)   

        row = col.row(align=True)
        if c.hide:
            icon = "DISCLOSURE_TRI_RIGHT"
        else:
            icon = "DISCLOSURE_TRI_DOWN"
        row.prop(c, "hide", text="", icon=icon, emboss=False)

        row.label(text=c.author + " - " + c.time)

        if c.frame_comment:
            if c_type == "edit_shot":
                target_frame = c.timeline_frame
            else:
                target_frame = c.frame
            if context.scene.frame_current == target_frame:
                icon = "MARKER_HLT"
            else:
                icon = "MARKER"
            
            op = row.operator("bpm.goto_comment", text = "", icon = icon, emboss = False)
            op.frame = target_frame

        if c.edit_time:
            icon = "OUTLINER_DATA_GP_LAYER"
        else:
            icon = "GREASEPENCIL"
        idx = comments.find(c.name)
        op = row.operator("bpm.modify_comment", text="", icon=icon, emboss = False)
        op.index = idx
        op.comment_type = c_type
        op = row.operator("bpm.remove_comment", text="", icon="X", emboss = False)
        op.index = idx
        op.comment_type = c_type

        if not c.hide:
            for line in split_string_on_spaces(c.comment, 25):
                col.label(text=line)
            if c.frame_comment or c.edit_time:
                if c.frame_comment:
                    col.label(text="Frame : " + str(c.frame))
                    if c_type == "edit_shot":
                        col.label(text="Timeline Frame : " + str(c.timeline_frame))
                if c.edit_time:
                    col.label(text="Edited on " + c.edit_time)

# draw shot comments ui
def draw_shot_comments_ui(container, scene_settings):

    container.prop(scene_settings, 'color_shot_comments', text="Color")

    row = container.row()
    row.label(text = "Names")
    row.prop(scene_settings, 'display_shot_comments_names', text = "")

    row = container.row()
    row.prop(scene_settings, 'display_shot_comments_boxes', text = "Name Boxes")
    row.prop(scene_settings, 'color_shot_comments_boxes', text="")

    container.prop(scene_settings, 'display_shot_comments_text_limit')

    #container.prop(scene_settings, "test_prop")

# draw custom folder ui list
def draw_custom_folder_template_list(container, winman, filebrowser):

    general_settings = winman.bpm_generalsettings
    idx = general_settings.custom_folders_index
    custom_folders_coll = winman.bpm_customfolders

    box = container.box()

    row = box.row(align=True)
    row.label(text = "Custom Folders")
    row.operator("bpm.refresh_custom_folders", text = "", icon = "FILE_REFRESH")
    draw_wiki_help(row, "Project-Custom-Folders")

    if len(custom_folders_coll) == 0 and not filebrowser:
        box.label(text = "No custom folders", icon = "INFO")
        return

    col1 = box.column(align=True)

    row = col1.row(align=True)
    row.template_list("BPM_UL_Folders_Uilist", "", winman, "bpm_customfolders", general_settings, "custom_folders_index", rows=4)

    col2 = row.column(align=True)

    if filebrowser:
        op = col2.operator("bpm.custom_folder_actions", text = "", icon = "ADD")
        op.action = "ADD"

    op = col2.operator("bpm.custom_folder_actions", text = "", icon = "REMOVE")
    op.action = "REMOVE"

    col2.separator()

    op = col2.operator("bpm.custom_folder_actions", text = "", icon = "TRIA_UP")
    op.action = "UP"

    op = col2.operator("bpm.custom_folder_actions", text = "", icon = "TRIA_DOWN")
    op.action = "DOWN"

    if idx in range(0, len(custom_folders_coll)):
        col1.label(text = custom_folders_coll[idx].filepath)

    col1.separator()

    col1.operator("bpm.open_custom_folder", text = "Open in explorer")
