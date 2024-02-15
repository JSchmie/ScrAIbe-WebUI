# ScrAIbe-WebUI


The Gradio App is a user-friendly interface for ScrAIbe. It enables you to run the model without any coding knowledge. Therefore, you can run the app in your browser and upload your audio file, or you can make the Framework avail on your network and run it on your local machine.

#### Running the Gradio App on your local machine

To run the Gradio App on your local machine, just use the following command:

```
scraibe --start-server --port 7860 --hf-token hf_yourhftoken
```

- `--start-server`: Command to start the Gradio App.
- `--port`: Flag for connecting the container internal port to the port on your local machine.
- `--hf-token`: Flag for entering your personal HuggingFace token in the container.

When the app is running, it will show you at which address you can access it.
The default address is: http://127.0.0.1:7860 or http://0.0.0.0:7860

After the app is running, you can upload your audio file and select the desired options.
An example is shown below:

![Gradio App](./img/gradio_app.png)
