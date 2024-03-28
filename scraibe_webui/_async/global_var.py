"""
global_var.py

This module stores global variables for the app.

Global variables:
    REQUEST_QUEUE (multiprocessing.Queue): A queue to store audio file paths as strings.
    RESPONSE_QUEUE (multiprocessing.Queue): A queue to store transcriptions as strings.
    LAST_ACTIVE_TIME (multiprocessing.Value): A value to store the time of the last activity.
    LOADED_EVENT (multiprocessing.Event): An event to indicate when the model is loaded.
    RUNNING_EVENT (multiprocessing.Event): An event to indicate when the model is running.
    MODELS_PARAMS (Optional[dict]): A dictionary to store the model parameters.
    MODELS_PROCESS (Optional[multiprocessing.Process]): A process to handle the model globally.
    LAST_USED (float): A float to track the time of the last user activity.
    TIMEOUT (Optional[int]): An integer to store the timeout in seconds.
    DEFAULT_APP_CONIFG_PATH (str): A string to store the default path to the app configuration file.
"""
import os
import time
import multiprocessing
from queue import Queue
from typing import Optional
from threading import Thread, Event

REQUEST_QUEUE: multiprocessing.Queue = multiprocessing.Queue()  # audio file path as string 
RESPONSE_QUEUE: multiprocessing.Queue = multiprocessing.Queue()  # transcription as string
LAST_ACTIVE_TIME: multiprocessing.Value = multiprocessing.Value('d', time.time())  # time of last activity
LOADED_EVENT: multiprocessing.Event = multiprocessing.Event()  # model loaded event
RUNNING_EVENT: multiprocessing.Event = multiprocessing.Event()  # model running event

MODELS_PARAMS: Optional[dict] = None  # model parameters
MODELS_PROCESS: Optional[multiprocessing.Process] = None  # model process to handle globally

# Global variable to track user activity
LAST_USED: float = time.time()
TIMEOUT: Optional[int] = None  # seconds

DEFAULT_APP_CONIFG_PATH: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.yaml")

MAIL_THREAD : Thread = None
MAIL_SETTINGS : dict = {}
MAIL_STOP_EVENT : Event = Event()
MAIL_TRANSCRIPT_QUEUE: Queue = multiprocessing.Queue()   # mail transcript queue stores the transcript to be sent
MAIL_MISC_QUEUE : Queue = Queue()  # stores the misc information like mail subject, recipient, etc.