import os
from setuptools import setup, find_packages

module_name = "scraibe-webui"
github_url = "https://github.com/JSchmie/ScrAIbe-WebUI"

file_dir = os.path.dirname(os.path.realpath(__file__))
absdir = lambda p: os.path.join(file_dir, p)

############### versioning ###############
verfile = os.path.abspath(os.path.join(module_name.replace("-","_"), "version.py"))
version = {"__file__": verfile}

with open(verfile, "r") as fp:
    exec(fp.read(), version)


############### setup ###############

build_version = "SCRAIBE_WEBUI_BUILD" in os.environ

version["ISRELEASED"] = True if "ISRELEASED" in os.environ else False

###############  load requirements ############### 

with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

if __name__ == "__main__":

    print(version["ISRELEASED"])
    
    setup(
        name=module_name,
        version=version["get_version"](build_version),
        packages=find_packages(),
        python_requires=">=3.8",
        readme="README.md",
        install_requires = requirements,
        url= github_url,

        license='GPL-3',
        author='Jacob Schmieder',
        author_email='Jacob.Schmieder@dbfz.de',
        description='WebUI for the fully automated transcription Toolkit ScrAIbe.',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: GPU :: NVIDIA CUDA :: 11.2',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11'
            'Programming Language :: Python :: 3.12'],
        keywords = ['webui','transcription', 'speech recognition', 'whisper', 'pyannote', 'audio', 'ScrAIbe', 'scraibe',
                    'speech-to-text', 'speech-to-text transcription', 'speech-to-text recognition',
                    'voice-to-speech'],
        package_data={'scraibe-webui' : ["*.html", "*.svg","*.yml"]},     
    )
