""" This file contains the interactions for the web app. Here we define the functions that will be called when the user interacts with the UI like pressing a button or uploading a file.
These functions will be used by all interfaces that use the web app.
"""
from time import sleep
from typing import Union
from pandas import DataFrame
from gradio import Progress, update, Info, Warning, Error
from scraibe import Transcript
from .wrapper import ScraibeWrapper
from .mail import MailService
from .background import BackgroundThread
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
        keep_model_alive (bool): A boolean value that determines whether the model should be kept alive.
        scraibe_params (dict): A dictionary containing the parameters required to load the model.

    Returns:
        model (Scraibe): The loaded Scraibe model.
    """
    _loader =  ScraibeWrapper.load_from_dict(scraibe_params)
    
    if not keep_model_alive:
        
        pipe = _loader
    else:
        pipe = gv.PIPE

        if pipe is None:
            Warning("Loading the model for the first time. This may take a few seconds.")
            pipe = _loader
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

        
        if not progress.track_tqdm: # TODO [FixProgressBarIssue]
            Warning("You are using Faster-Whipser Models progress will not be tracked!")
            
        # load model or use the existing one

        _pipe = get_pipe(keep_model_alive, scraibe_params)
    
        # get *args which are not None
        
        
        if progress.track_tqdm: # TODO [FixProgressBarIssue]
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
                    update(visible = True, open = True), # accordion for json
                    update(visible = False), # annotation
                    update(visible = False)) # annotate button


def show_notification(mail : str) -> str:
    # This function returns HTML for the notification with email and subject details if provided.
    email_message = f" They will be processed and sent to your email {mail} soon."
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
                mail_service_params : dict,
                scraibe_kwargs : dict,
                threads_per_model : int,
                error_format_options = {},
                transcript_format_options = {},
                upload_format_options = {}):
    
    source = audio or video or file_in
    
    if not mail:
        raise Error("Please provide an email address.")
    if not source:
        raise Error("Please provide a valid source file.")
    
    job = BackgroundThread(mail_service_params, scraibe_kwargs, threads_per_model)
    
    job.run(audio = source,
            reciever = mail,
            task = task,
            num_speakers = num_speakers,
            translate = translate,
            language = language,
            error_format_options = error_format_options,
            transcript_format_options = transcript_format_options)
    
    if "queue_position" in upload_format_options.keys():
        gv.NUMBER_OF_QUEUE += 1
        upload_format_options["queue_position"] = gv.NUMBER_OF_QUEUE
    
    MailService.from_config(mail_service_params).send_upload_notification(mail, **upload_format_options)

    yield update(value = show_notification(mail),visible = True)
    sleep(5)
    yield update(visible = False)
    
def apply_settings(model: str,
                   scraibe_params : dict,
                   keep_model_alive_checkbox : bool,
                   keep_model_alive : bool,) -> None:
    """
    Load the selected model into memory.
    
    Args:
        model (str): The name of the model to load.
    
    Returns:
        None
    """
    scraibe_params["whisper_model"] = model
    
    keep_model_alive = keep_model_alive_checkbox
    print(f"Model is set to {scraibe_params['whisper_model']} will be kept alive: {keep_model_alive}. ") 
    
    Info(f"Model is set to {scraibe_params['whisper_model']} will be kept alive: {keep_model_alive}. " \
         "If you change the model, the new model will be loaded on the next task.")
    return  scraibe_params, keep_model_alive