# Customize your WebUI

You can completly custom ize your `ScrAIbe-WebUI` instancer using a YAML File.`ScrAIbe-WebUI` interanlly uses a default `config.yaml` file, which is located under `scraibe_webui/misc`. But no worries you do not have to touch this file by your own but rather use our interface for it. If you do not want to use a YAML file you can also input your settings as keyword argumentes using the python interface or the commandline interface. 

## How to use custom e settings.

Let's use a simple example realying on some WebUI knowlage.
We want to change the **port** to 8080 and the **whipser model** to the latest `large-v3`.
First of all we consider you allread sucessuly managed ScrAIbe-WebUI otherwise I would suggest you to follow our [Installtion Guide](GETTING_STARTED.md). 
Now you have to option the first one would be to use our `command line interface` or our `python` interface. Further more you have to choose wheter you want to use a stuctured dictionary, a YAML or just keword arguments to be the inpur of your choice. 

Let's start whit the `cli` using the `scraibe-webui` command using your file called `custom.yaml` :

```yaml
launch:
    server_port: 8080
scraibe_params:
  whisper_model : 'large-v3'
```

Now you can run the WebUI using: 

costume
