""" This file contains the interactions for the web app. Here we define the functions that will be called when the user interacts with the UI like pressing a button or uploading a file.
These functions will be used by all interfaces that use the web app.
"""


import gradio as gr
from scraibe import Transcript

def select_task(choice):
        # tell the app that it is still in use
    if choice == 'Auto Transcribe':
        
        return (gr.update(visible = True),
                gr.update(visible = True),
                gr.update(visible = True))
                
        
    elif choice == 'Transcribe':
        
        return (gr.update(visible = False),
                gr.update(visible = True),
                gr.update(visible = True))

        
    elif choice == 'Diarisation':
        
        return (gr.update(visible = True),
                gr.update(visible = False),
                gr.update(visible = False))
        
def select_origin(choice):
        
    # tell the app that it is still in use
    if choice == "Audio":
        
        return (gr.update(visible = True),
                gr.update(visible = False, value = None),
                gr.update(visible = False, value = None))
    
    elif choice == "Video":
        
        return (gr.update(visible = False, value = None),
                gr.update(visible = True),
                gr.update(visible = False, value = None))
    
        
    elif choice == "File or Files":
        
        return (gr.update(visible = False, value = None),
                gr.update(visible = False, value = None),
                gr.update(visible = True))
        
def annotate_output(annoation : str, out_json : dict):
    # get *args which are not None
    
    trans = Transcript.from_json(out_json)
    trans = trans.annotate(*annoation.split(","))

    return gr.update(value = str(trans)),gr.update(value = trans.get_json())