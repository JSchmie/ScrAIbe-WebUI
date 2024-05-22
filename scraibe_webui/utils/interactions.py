""" This file contains the interactions for the web app. Here we define the functions that will be called when the user interacts with the UI like pressing a button or uploading a file.
These functions will be used by all interfaces that use the web app.
"""

from typing import Union
from pandas import DataFrame
from gradio import Progress, update, Info, Warning
from scraibe import Transcript
from .wrapper import ScraibeWrapper
import scraibe_webui.global_var as gv

def select_task(choice):
        # tell the app that it is still in use
    if choice == 'Auto Transcribe':
        
        return (update(visible = True),
                update(visible = True),
                update(visible = True))
                
        
    elif choice == 'Transcribe':
        
        return (update(visible = False),
                update(visible = True),
                update(visible = True))

        
    elif choice == 'Diarisation':
        
        return (update(visible = True),
                update(visible = False),
                update(visible = False))
        
def select_origin(choice):
        
    # tell the app that it is still in use
    if choice == "Audio":
        
        return (update(visible = True),
                update(visible = False, value = None),
                update(visible = False, value = None))
    
    elif choice == "Video":
        
        return (update(visible = False, value = None),
                update(visible = True),
                update(visible = False, value = None))
    
        
    elif choice == "File or Files":
        
        return (update(visible = False, value = None),
                update(visible = False, value = None),
                update(visible = True))
        
def annotate_output(annoation : DataFrame, out_json : dict):
    # get *args which are not None
    
    trans = Transcript.from_json(out_json)
    
    _ann = annoation.loc[0].to_dict()
     
    trans = trans.annotate(**_ann)

    return update(value = str(trans)),update(value = trans.get_json())


def get_pipe(keep_model_alive : bool, scraibe_params : dict) -> ScraibeWrapper:
    """
    This function loads the model into memory only when it's needed, which is beneficial for occasional use. 
    By doing so, it efficiently manages resource usage by ensuring that the resources required by the model 
    are only utilized when the model is actually running. This approach helps to free up resources when the 
    model is not in use, thereby improving the overall performance and efficiency of the system.
    
    Args:
        timer_interval (int): The interval (in seconds) at which the model should be kept alive in memory.
        audio (str): The path to the audio file for which the prediction should be made.

    Returns:
        model (Scraibe): The loaded Scraibe model.
    """
    _loader =  ScraibeWrapper.load_from_dict
    
    if keep_model_alive:
        pipe = _loader(**scraibe_params)
    else:
        pipe = gv.PIPE

        if pipe is None:
            Warning("Loading the model for the first time. This may take a few seconds.")
            pipe = _loader(**scraibe_params)
            gv.PIPE = pipe

    return pipe

def run_scraibe(task : str,
               num_speakers : int,
               translate : bool,
               language : str,
               audio : str,
               video : str,
               file_in : Union[str, list],
               keep_model_alive : bool,
               scraibe_params : dict,
               progress = Progress(track_tqdm= True)):
        
        # load model or use the existing one

        _pipe = get_pipe(keep_model_alive, scraibe_params)
    
        # get *args which are not None
        progress(0, desc='Starting task...')
        source = audio or video or file_in
        
        if isinstance(source, list):
            source = [s.name for s in source]
            if len(source) == 1:
                source = source[0]
 
        if task == 'Auto Transcribe':
    
            res, out_str , out_json = _pipe.autotranscribe(source = source,
                                num_speakers = num_speakers,
                                translate = translate,
                                language = language)
            
            _df = DataFrame(columns= res.speakers)
            
            _df.loc[0] = res.speakers
            
            return (update(value = out_str, visible = True), # out_txt
                    update(value = out_json, visible = True), # out_json
                    update(visible = True), # accordion for json
                    update(value = _df,
                           row_count = (1, "fixed"),
                           col_count = (len(res.speakers), "fixed"),
                           visible = True), # annotation
                    update(visible = True)) # annotate button     
            
        elif task == 'Transcribe':
            
            out = _pipe.transcribe(source = source,
                                translate = translate,
                                language = language)
            
            return (update(value = out, visible = True), # out_txt
                    update(value = None, visible = False), # out_json
                    update(visible = False), # accordion for json
                    update(visible = False), # annotation
                    update(visible = False)) # annotate button 
            
        elif task == 'Diarisation':
            
            out = _pipe.diarisation(source = source,
                                num_speakers = num_speakers)
            
            return (update(value = None, visible = False), # out_txt
                    update(value = out, visible = True), # out_json
                    update(visible = True), # accordion for json
                    update(visible = False), # annotation
                    update(visible = False)) # annotate button


def show_notification(mail : str, subject : str) -> str:
    # This function returns HTML for the notification with email and subject details if provided.
    email_message = f" They will be processed and sent to your email ({mail}) with the subject '{subject}' soon."
    return f"""
    <div style="background-color: #4CAF50; color: white; padding: 20px; border-radius: 5px; margin-top: 20px;">
        Your files have been successfully added to the queue.{email_message}
    </div>
    """


def run_scraibe_async(task : str,
                num_speakers : int,
                translate : bool,
                language : str,
                audio : str,
                video : str,
                file_in : Union[str, list],
                mail : str,
                subject : str,
                keep_model_alive : bool,
                scraibe_params : dict,):
    
    source = audio or video or file_in
    
    
    
    
    #TODO: Implement the function to send the transcript via email
    return update(value = show_notification(mail, subject),visible = True)


def apply_settings(model: str,
                   keep_model_alive : bool,
                   scraibe_params : dict) -> None:
    """
    Load the selected model into memory.
    
    Args:
        model (str): The name of the model to load.
    
    Returns:
        None
    """
    Info(f"Loading model {model}...\n" \
         "Depending on the model size, this may take a few seconds.")
    gv.PIPE.update_transcriber_model(model)
    
    Info(f"Model {model} loaded successfully.")
    
    return update(value = model)
