"""
This module contains the async gradio Interface which is used to interact with the user.

The interface is themed with a soft color scheme, with primary colors of green and orange, and a neutral color of gray.

A list of languages is also defined in this module, which may be used elsewhere in the application.

Classes:
    Soft: A class from the gradio library used to theme the interface.

Variables:
    theme (gr.themes.Soft): The theme for the gradio interface.
    LANGUAGES (list of str): A list of languages supported by the application.
"""

import gradio as gr

from .interactions import run_scraibe
from ..utils.interactions import select_origin, select_task
from ..utils.lang import LANGUAGES
from ..utils.themes import theme


def gradio_Interface(layout : dict) -> gr.Blocks:
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
    with gr.Blocks(theme=theme,title='ScrAIbe: Automatic Audio Transcription') as demo:
            
            # Define components
            

            if layout.get('header') is not None:            
                gr.HTML(layout.get('header'), visible= True, show_label=False)
            
                
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

            video = gr.Video(label="Record or Upload Video",include_audio= True,
                                interactive= True, visible= False)
            
            file_in = gr.Files(label="Upload File or Files", interactive= True, visible= False)
            
            mail = gr.Textbox(type= 'email', label="Email address for transcription delivery", placeholder= "Enter your email",
                            visible= True)
            
            subject = gr.Textbox(value="My Test Transcript", label="Subject for transcription delivery",
                            visible= True)
            
            output = gr.Textbox(visible= False)
            
            submit = gr.Button()
            
            if layout.get('footer') is not None:            
                gr.HTML(layout.get('footer'), visible= True, show_label=False)
                 
            # Define usage of components
            input.change(fn=select_origin, inputs=[input],
                            outputs=[audio,video, file_in])
            
            task.change(fn=select_task, inputs=[task],
                        outputs=[num_speakers, translate, language])
            
            submit.click(fn = run_scraibe, 
                            inputs=[task, num_speakers, translate, language, audio, video, file_in, mail, subject],
                            outputs=[output], concurrency_limit = None)
            
    return demo