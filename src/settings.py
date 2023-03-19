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
        self._dirty = False

        try:
            self._settings = self._load_settings()
            self._disabled = False
        except:
            self._settings = DEFAULT_SETTINGS
            self._disabled = True 


    def _load_settings(self):
        # If the file does not exists, create it with the defaults
        # Need to handle loading an older file                
        if self._SETTINGS_FOLDER not in os.listdir():
            self._create_settings(DEFAULT_SETTINGS)

        with open(self._settings_file, 'r') as file:
            stuff = json.load(file)
            # Validate settings.
            stuff = self._clean_settings(stuff)

        return stuff


    def _clean_settings(self, content):
        settings = DEFAULT_SETTINGS
        
        # Same number of settings
        valid = len(settings) == len(content) 
        
        # Settings that are in are valid
        for k,v in content.items():
            if k in settings and type(v) == type(settings[k]):
                settings[k] = v
            else:
                valid = False

        if not valid: # Something wonky, replace the file.
            self._create_settings(settings)
            
        return settings

    def _create_settings(self, content):                
        # Create a new folder and settings file based on the passed in content.
        if self._SETTINGS_FOLDER not in os.listdir():
            os.mkdir(self._SETTINGS_FOLDER)

        # create / replace the file.
        with open(self._settings_file, 'w') as file:
            try:
                json.dump(content, file)
            except Exception as e:
                print('Unable to write file', e)


    def persist_settings(self):
        if not self._disabled and self._dirty: 
            with open(self._settings_file, 'w') as file:                
                try:
                    json.dump(self._settings, file)
                except Exception as e:
                    print('Unable to write file', e)
        
        self._dirty = False
        pass

    #### Settings are accessed via properties.
    @property
    def twelve_hr(self):
        return self._settings['12HR']
    
    @twelve_hr.setter
    def twelve_hr(self, val):
        self._dirty = True
        self._settings['12HR'] = val
    
    @property
    def beep(self):
        return self._settings['BEEP']

    @beep.setter
    def beep(self, val):
        self._dirty = True
        self._settings['BEEP'] = val
    
    @property
    def dst_adjust(self):
        return self._settings['DST_ADJUST']
    
    @dst_adjust.setter
    def dst_adjust(self, val):
        self._dirty = True
        self._settings['DST_ADJUST'] = val
        
    @property    
    def autodim(self):
        return self._settings['AUTODIM']
    
    @autodim.setter
    def autodim(self, val):
        self._dirty = True
        self._settings['AUTODIM'] = val
        
    @property
    def dark_mode(self):
        return self._settings['DARKMODE']
    
    @dark_mode.setter
    def dark_mode(self, val):
        self._dirty = True
        self._settings['DARKMODE'] = val
        
    @property
    def night_level(self):
        return self._settings['NIGHT_LEVEL']
    
    @night_level.setter
    def night_level(self, val):
        self._dirty = True
        self._settings['NIGHT_LEVEL'] = val
        
    @property
    def dim_level(self):
        return self._settings['DIM_LEVEL']

    @dim_level.setter
    def dim_level(self, val):
        self._dirty = True
        self._settings['DIM_LEVEL'] = val