"""
This module contains the gradio Interface which is used to interact with the user.

The interface is themed with a soft color scheme, with primary colors of green and orange, and a neutral color of gray.

A list of languages is also defined in this module, which may be used elsewhere in the application.

Classes:
    Soft: A class from the gradio library used to theme the interface.

Variables:
    theme (gr.themes.Soft): The theme for the gradio interface.
    LANGUAGES (list of str): A list of languages supported by the application.
"""

import gradio as gr
from .utils.interactions import select_task, select_origin, annotate_output \
    , apply_settings, run_scraibe, run_scraibe_async

from .utils.lang import LANGUAGES
from .utils.themes import theme


# TODO: Make a prper interface for the follwing bool values 

async_ui = True

def gradio_Interface(layout : dict, scraibe_params : dict ) -> gr.Blocks:
    """
    Creates a gradio interface for audio transcription.

    The interface includes options for the user to select the task, number of speakers, translation, language, and input type.
    It also provides options for the user to upload or record audio/video, or upload files.
    The output of the transcription is displayed in a textbox, and the JSON output in a JSON viewer.
    The user can also annotate the output by naming the speakers.

    Args:
        layout (dict, optional): A dictionary containing layout information. Defaults to None.

    Returns:
        gr.Blocks: A gradio Blocks object representing the interface.
    """
    
    keep_model_alive = gr.State(scraibe_params.pop('keep_model_alive', False))
    
    scraibe_params = gr.State(scraibe_params)
    
    
    with gr.Blocks(theme=theme,title='ScrAIbe: Automatic Audio Transcription') as demo:
    
            # Define components
            if layout.get('header') is not None:            
                gr.HTML(layout.get('header'), visible= True, show_label=False)
                
            with gr.Row():
                
                with gr.Column():
                    
                    if layout.get('show_settings', True):
                        with gr.Accordion(label="Model Configuration", open= False):
                            #TODO: Add vlaue to whisper_model from config
                            whisper_model = gr.Dropdown(label= "Select Whisper Model",
                                                    choices= ['tiny', 'base', 'small' ,
                                                                'medium', 'large-v3' ],
                                                    value= 'medium')
                            load_model_button = gr.Button("Load Model")
                            
                            checkbox_model_alive = gr.Checkbox(label="Keep model alive?", info = "Keep the model loaded in memory for faster processing.",
                                                                value= keep_model_alive)
                            
                            load_model_button.click(fn = apply_settings, inputs=[whisper_model,checkbox_model_alive], outputs=[whisper_model])
                        
                    task = gr.Radio(["Auto Transcribe", "Transcribe", "Diarisation"], label="Task",
                                    value= 'Auto Transcribe')
                    
                    num_speakers = gr.Number(value=0, label= "Number of speakers (optional)", 
                                    info = "Number of speakers in the audio file. If you don't know,\
                                        leave it at 0.", minimum=0, visible= True)
                    
                    translate = gr.Checkbox(label="Translation", value = False,
                                    info="Select if you want the output to be translated to English.",
                                    visible= True)
                    
                    language = gr.Dropdown(LANGUAGES,
                                    label="Language (optional)", value = "None",
                                    info="Language of the audio file. If you don't know,\
                                        leave it at None.", visible= True)
                    
                    input = gr.Radio(["Audio", "Video" 
                                        ,"File or Files"], label="Input Type", value="Audio")
                    
                    audio = gr.Audio(type = "filepath", label="Upload Audio",
                                        interactive= True, visible= True)

                    video = gr.Video(label="Record or Upload Video", include_audio= True,
                                        interactive= True, visible= False)
                    file_in = gr.Files(label="Upload File or Files", interactive= True, visible= False)
                    
                    # Define behavior of components
                    
                    input.change(fn=select_origin, inputs=[input],
                                outputs=[audio,video, file_in])
                
                    task.change(fn=select_task, inputs=[task],
                            outputs=[num_speakers, translate, language])
                    
                    
                    if async_ui:
                        # creates the async components for the interface which can be used to send you a transcript via email
                        mail = gr.Textbox(type= 'email', label="Email address for transcription delivery", placeholder= "Enter your email",
                            visible= True)
            
                        subject = gr.Textbox(value="My Test Transcript", label="Subject for transcription delivery",
                                        visible= True)
                        
                        output = gr.Textbox(visible= False)
                        
                        submit_async = gr.Button(variant="primary", label="Add files to queue")
                        
                    else:
                        # creates the sync components for the interface which can be used to get the transcript on the interface
                        submit_sync = gr.Button(variant="primary", label="Transcribe")
                    
                if not async_ui:
    
                    with gr.Column():
                        
                        out_txt = gr.Textbox(label="Output",
                                                visible= True, show_copy_button=True)
                        with gr.Accordion(label="JSON Output", open= False, visible= False) as json_accordion:
                            out_json = gr.JSON(label="JSON Output",
                                                visible= False)
                        
                        annoation = gr.Dataframe( label="Name your speaker's",
                                            row_count = 1,
                                            visible= False,
                                            interactive= True)
                        
                        annotate = gr.Button(value="Annotate", visible= False, interactive= True)
                        
                        annotate.click(fn = annotate_output, inputs=[annoation, out_json],
                                outputs=[out_txt, out_json])   
                
                
                if layout.get('footer') is not None:            
                    gr.HTML(layout.get('footer'), visible= True, show_label=False)
                    
                # Define usage of components
                
                # Define interaction for the sync components
                submit_sync.click(fn = run_scraibe, 
                                inputs= [task, num_speakers, translate, language, audio, video, file_in, keep_model_alive, scraibe_params],
                                outputs=[out_txt, out_json, json_accordion, annoation, annotate], concurrency_limit = None)
                
                
                # Define interaction for the async components
                if async_ui:
                    submit_async.click(fn = run_scraibe_async, 
                                    inputs= [task, num_speakers, translate, language, audio, video, file_in,
                                             mail, subject, keep_model_alive, scraibe_params],
                                    outputs=[output], concurrency_limit = None)
                                
    return demo