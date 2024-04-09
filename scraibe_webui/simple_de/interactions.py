"""
This file contains ervery function that will be called when the user interacts with the 
UI like pressing a button or uploading a file.
"""
from gradio import Progress, update
import scraibe_webui.simple.global_var as gv

def run_scraibe(task,
               num_speakers,
               translate,
               language,
               audio,
               video,
               file_in,
               progress = Progress(track_tqdm= True)):
    
        # get *args which are not None
        progress(0, desc='Starte die Transkription...')
        source = audio or video or file_in
        
        if isinstance(source, list):
            source = [s.name for s in source]
            if len(source) == 1:
                source = source[0]
 
        if task == 'Automatische Transkription mit Sprecher*innen-Erkennung':
    
            out_str , out_json = gv.PIPE.autotranscribe(source = source,
                                num_speakers = num_speakers,
                                translate = translate,
                                language = language)
            
            if isinstance(source, str):
                return (update(value = out_str, visible = True),
                        update(value = out_json, visible = True),
                        update(visible = True),
                        update(visible = True))      
            else:
                return (update(value = out_str, visible = True),
                        update(value = out_json, visible = True),
                        update(visible = False),
                        update(visible = False))  
            
        elif task == 'Transkription ohne Sprecher*innen-Erkennung':
            
            out = gv.PIPE.transcribe(source = source,
                                translate = translate,
                                language = language)
            
            return (update(value = out, visible = True),
                    update(value = None, visible = False),
                    update(visible = False),
                    update(visible = False))
            
        elif task == 'Sprecher*innen-Erkennung ohne Transkription':
            
            out = gv.PIPE.diarisation(source = source,
                                num_speakers = num_speakers)
            
            return (update(value = None, visible = False),
                    update(value = out, visible = True),
                    update(visible = False),
                    update(visible = False))

def select_task(choice):
        # tell the app that it is still in use

    if choice == 'Automatische Transkription mit Sprecher*innen-Erkennung':
        
        return (update(visible = True),
                update(visible = True),
                update(visible = True))
                
        
    elif choice == 'Transkription ohne Sprecher*innen-Erkennung':
        
        return (update(visible = False),
                update(visible = True),
                update(visible = True))

        
    elif choice == 'Sprecher*innen-Erkennung ohne Transkription':
        
        return (update(visible = True),
                update(visible = False),
                update(visible = False))
        
def select_origin(choice):
        
    # tell the app that it is still in use
    if choice == "Audio Datei (.mp3, .wav, etc.)":
        
        return (update(visible = True),
                update(visible = False, value = None),
                update(visible = False, value = None))
    
    elif choice == "Video Datei (.mp4, .mov, etc.)":
        
        return (update(visible = False, value = None),
                update(visible = True),
                update(visible = False, value = None))
    
        
    elif choice == "Datei oder Dateien":
        
        return (update(visible = False, value = None),
                update(visible = False, value = None),
                update(visible = True))
        