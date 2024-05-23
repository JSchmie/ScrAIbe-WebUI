"""
This file contains ervery function that will be called when the user interacts with the 
UI like pressing a button or uploading a file.
"""

import gradio as gr 
import scraibe_webui.sync.global_var as gv
from .multi import start_model_worker

def run_scraibe(task,
                num_speakers,
                translate,
                language,
                audio,
                video,
                file_in):
    
    if gv.MODELS_PROCESS.is_alive():
        #progress(0.0, desc='Loading model...')
        gv.MODELS_PROCESS = start_model_worker(gv.MODELS_PARAMS,
                                      gv.REQUEST_QUEUE,
                                      gv.LAST_ACTIVE_TIME,
                                      gv.RESPONSE_QUEUE,
                                      gv.LOADED_EVENT,
                                      gv.RUNNING_EVENT)
    
    # progress(0.1, desc='Starting task...')
    source = audio or video or file_in
    
    if isinstance(source, list):
        source = [s.name for s in source]
        if len(source) == 1:
            source = source[0]
    
    config = dict(source = source,
                  task = task,
                  num_speakers = num_speakers,
                  translate = translate,
                  language = language)
    
    gv.REQUEST_QUEUE.put(config)
    
    if task == 'Auto Transcribe':
        
        out_str , out_json = gv.RESPONSE_QUEUE.get()
        
        if isinstance(source, str):
            return (gr.update(value = out_str, visible = True),
                    gr.update(value = out_json, visible = True),
                    gr.update(visible = True),
                    gr.update(visible = True))      
        else:
            return (gr.update(value = out_str, visible = True),
                    gr.update(value = out_json, visible = True),
                    gr.update(visible = False),
                    gr.update(visible = False))  
        
    elif task == 'Transcribe':
        
        out = gv.RESPONSE_QUEUE.get()
        
        return (gr.update(value = out, visible = True),
                gr.update(value = None, visible = False),
                gr.update(visible = False),
                gr.update(visible = False))
        
    elif task == 'Diarisation':
        
        out = gv.RESPONSE_QUEUE.get()
        
        return (gr.update(value = None, visible = False),
                gr.update(value = out, visible = True),
                gr.update(visible = False),
                gr.update(visible = False))
    