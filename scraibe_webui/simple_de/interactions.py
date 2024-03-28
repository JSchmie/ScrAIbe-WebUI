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
               audio1,
               audio2,
               video1,
               video2,
               file_in,
               progress = Progress(track_tqdm= True)):
    
        # get *args which are not None
        progress(0, desc='Starting task...')
        source = audio1 or audio2 or video1 or video2 or file_in
        
        print(gv.PIPE)
        
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
            
        elif task == 'Sprecher*innen-Erkennung':
            
            out = gv.PIPE.diarisation(source = source,
                                num_speakers = num_speakers)
            
            return (update(value = None, visible = False),
                    update(value = out, visible = True),
                    update(visible = False),
                    update(visible = False))