"""
This module initializes the package by importing all necessary submodules.

Submodules:
    - multi: Contains functionality related to multi-threading or multi-processing.
    - interface: Defines the user interface for the application.
    - interactions: Handles user interactions.
    - global_var: Defines global variables used across the package.
    - app: Contains the main application logic.
    - mail: Provides functionality for sending emails.

Each submodule is imported in its entirety (i.e., using the * wildcard).
"""
from .multi import *
from .interface import *
from .multi import *
from .interactions import *
from .global_var import *
from .app import *
from .mail import *
