"""This file contains interactions which are unique to the async version of the web app.
"""

import scraibe_webui._async.global_var as gv
from .multi import start_model_worker, start_mail_thread
from gradio  import update 

def run_scraibe(task,
                num_speakers,
                translate,
                language,
                audio,
                video,
                file_in,
                mail,
                subject):
    
    source = audio or video or file_in
    
    if not gv.MODELS_PROCESS.is_alive():
        #progress(0.0, desc='Loading model...')
        
        gv.MODELS_PROCESS = start_model_worker(model_params = gv.MODELS_PARAMS,
                                            request_queue = gv.REQUEST_QUEUE,
                                            last_active_time = gv.LAST_ACTIVE_TIME,
                                            mail_transcript_queue = gv.MAIL_TRANSCRIPT_QUEUE,
                                            loaded_event = gv.LOADED_EVENT,
                                            running_event = gv.RUNNING_EVENT)
    
    if not gv.MAIL_THREAD.is_alive():
        gv.MAIL_THREAD = start_mail_thread(gv.MAIL_SETTINGS, gv.MAIL_TRANSCRIPT_QUEUE, gv.MAIL_MISC_QUEUE)
        
    
    if isinstance(source, list):
        source = [s.name for s in source]
        if len(source) == 1:
            source = source[0]
    
    config = dict(source = source,
                  task = task,
                  num_speakers = num_speakers,
                  translate = translate,
                  language = language)
    
    gv.MAIL_MISC_QUEUE.put(dict(receiver_email = mail, subject = subject))
    gv.REQUEST_QUEUE.put(config)
    
    return update(value = f'Your transcription is submitted will be sent to the following Email: {mail}',visible = True)
