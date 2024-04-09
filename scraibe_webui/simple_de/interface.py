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

from .interactions import run_scraibe, select_origin, select_task
from ..utils.interactions import annotate_output
from ..utils.lang import LANGUAGES
from ..utils.themes import theme

js_enforce_light = """
function refresh() {
    const url = new URL(window.location);

    if (url.searchParams.get('__theme') !== 'light') {
        url.searchParams.set('__theme', 'light');
        window.location.href = url.href;
    }
}
"""


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
    with gr.Blocks(theme=theme,title='ScrAIbe: Automatic Audio Transcription', js= js_enforce_light) as demo:
            
            # Define components
            if layout.get('header') is not None:            
                gr.HTML(layout.get('header'), visible= True, show_label=False)
            
            with gr.Row():
                
                with gr.Column():
                
                    task = gr.Radio(["Automatische Transkription mit Sprecher*innen-Erkennung", 
                                     "Transkription ohne Sprecher*innen-Erkennung", 
                                     "Sprecher*innen-Erkennung ohne Transkription"], label="Aufgabe",
                                    value= 'Automatische Transkription mit Sprecher*innen-Erkennung')
                    
                    num_speakers = gr.Number(value=0, label= "Anzahl der Sprecher*innen", 
                                    info = "Anzahl der Sprecher*innen in der Audiodatei. Wenn Sie es nicht wissen oder sich unsicher sind,\
                                        lassen Sie es bei 0.", visible= True)
                    
                    translate = gr.Checkbox(label="Übersetzung in die Englische Sprache", value = False,
                                    info="Setzen Sie hier den Haken, wenn Sie eine Übersetzung in die Englische Sprache wünschen.",
                                    visible= True)
                    
                    language = gr.Dropdown(LANGUAGES,
                                    label="Sprache", value = "None",
                                    info="Lautsprache, die in der Audiodatei gesprochen wird.", visible= True)
                    
                    input = gr.Radio(["Audio Datei (.mp3, .wav, etc.)", "Video Datei (.mp4, .mov, etc.)", "Datei oder Dateien"], label="Art der Eingabe", value= "Audio Datei (.mp3, .wav, etc.)")
                    
                    audio = gr.Audio(type = "filepath", label="Audio Datei (.mp3, .wav, etc.)",
                                        interactive= True, visible= True)

                    video = gr.Video(label="Video Datei (.mp4, .mov, etc.)",include_audio= True,
                                        interactive= True, visible= False)
                    file_in = gr.Files(label="Datei oder Dateien", interactive= True, visible= False)
                    
                    submit = gr.Button(value="Transkription starten",variant="primary")
                
                with gr.Column():
                    
                    out_txt = gr.Textbox(label="Resultat",
                                            visible= True, show_copy_button=True)
                    
                    out_json = gr.JSON(label="Resultat im JSON Format für Entwickler*innen",
                                        visible= False)
                    
                    annotation = gr.Textbox(label="Namensgebung der Sprecher*innen",
                                        info= "Bitte geben Sie eine Liste der Sprecher*innen an,"\
                                            " die in exakt dieser Reihenfolge beginnen zu sprechen."\
                                            " Verwenden Sie ein Komma ( , ) als Trennzeichen."\
                                            "  Beachten Sie, dass der erste Name SPEAKER_00,"\
                                            " der zweite SPEAKER_01 usw. zugeordnet wird.",
                                        visible= False, interactive= True)
                    
                    annotate = gr.Button(value="Annotieren der Sprecher*innen", visible= False, interactive= True, )
            
            if layout.get('footer') is not None:            
                gr.HTML(layout.get('footer'), visible= True, show_label=False)
                 
            # Define usage of components
            input.change(fn=select_origin, inputs=[input],
                            outputs=[audio,video, file_in])
            
            task.change(fn=select_task, inputs=[task],
                        outputs=[num_speakers, translate, language])
            
            submit.click(fn = run_scraibe, 
                            inputs= [task, num_speakers, translate, language, audio, video, file_in],
                            outputs=[out_txt, out_json, annotation, annotate], concurrency_limit = None)
            
            annotate.click(fn = annotate_output, inputs=[annotation, out_json],
                            outputs=[out_txt, out_json])
            
    return demo