import os
import json

class Version:
    def __init__(self) -> None:
        VERSION_FILE = '.version'
        try:
            with open(VERSION_FILE, 'r') as file:
                stuff = json.load(file)
                # Validate settings.
                self._version = stuff['version']
        except:
            self._version = 'dev'


    def get_version_string(self) -> str:
        return self._version

    
    def get_version(self) -> str:
        return self._version.replace('v', '')
