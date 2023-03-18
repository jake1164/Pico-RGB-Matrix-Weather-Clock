import os
import json

DEFAULT_SETTINGS = {
    "12HR": True,
    "BEEP": True,
    "AUTODIM": True,
    "DARKMODE": True,
    "DST_ADJUST": True,
    "NIGHT_LEVEL": 1000,
    "DIM_LEVEL": 2000 
    }


class Settings:
    def __init__(self) -> None:
        self._SETTINGS_FOLDER = '.settings'
        SETTINGS_FILE = 'settings.json'
        self._settings_file = f'{self._SETTINGS_FOLDER}/{SETTINGS_FILE}'

        try:
            self._settings = self._load_settings()
        except:
            self._settings = DEFAULT_SETTINGS
            self._disabled = True 


    def _load_settings(self):
        # If the file does not exists, create it with the defaults
        # Need to handle loading an older file                
        if self._SETTINGS_FOLDER not in os.listdir():
            print('creating default settings')
            self._create_settings(DEFAULT_SETTINGS)

        print('loading content')
        with open(self._settings_file, 'r') as file:
            stuff = json.load(file)
            # Validate settings.
            stuff = self._clean_settings(stuff)

        return stuff


    def _clean_settings(self, content):
        settings = DEFAULT_SETTINGS
        
        # Same number of settings
        valid = len(settings) == len(content) 
        
        print('before', settings)
        # Settings that are in are valid
        for k,v in content.items():
            #print('content', k, v)
            if k in settings and type(v) == type(settings[k]):
                settings[k] = v
            else:
                valid = False

        print(f'after valid: {valid}', settings)

        if not valid: # Something wonky, replace the file.
            self._create_settings(settings)
            
        return settings

    def _create_settings(self, content):                
        # File was found corrupt, remove folder if it exists and start over.
        #if self._SETTINGS_FOLDER in os.listdir():
        #    print('removing .settings')
        #    try:
        #        os.rmdir(self._SETTINGS_FOLDER)
        #    except Exception as e:
        #        print('Error removing directory?', e)

        print('creating .settings')
        # Create a new folder and settings file based on the passed in content.
        if self._SETTINGS_FOLDER not in os.listdir():
            os.mkdir(self._SETTINGS_FOLDER)

        # create / replace the file.
        with open(self._settings_file, 'w') as file:
            print('creating file with content', content)
            try:
                json.dump(content, file)
            except Exception as e:
                print('Unable to write file', e)


    def persist_settings(self):
        pass


    def get_12hr(self):
        return self._settings['12HR']
    
    def get_beep(self):
        return self._settings['BEEP']

    def get_dst_adjust(self):
        return self._settings['DST_ADJUST']
        
    def get_autodim(self):
        return self._settings['AUTODIM']
    
    def get_dark_mode(self):
        return self._settings['DARKMODE']
        
    def get_night_level(self):
        return self._settings['NIGHT_LEVEL']
    
    def get_dim_level(self):
        return self._settings['DIM_LEVEL']