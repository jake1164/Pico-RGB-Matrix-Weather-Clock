## Class for handling networking. 
import os
import gc
import ssl
import wifi
import socketpool
import adafruit_ntp
import adafruit_requests

class WifiNetwork:
    def __init__(self) -> None:
        self.RETRY_WIFI = 5 # Number of times to attempt to connect to wifi
        self.SSID = os.getenv('WIFI_SSID')
        self.PASS = os.getenv('WIFI_PASSWORD')

        if self.SSID is None or self.PASS is None or len(self.SSID) == 0 or len(self.PASS) == 0:
            raise Exception("WIFI_SSID & WIFI_PASSWORD are stored in settings.toml, please add them")

        # NTP specific constants
        self.TZ = os.getenv('TZ_OFFSET')
        # Offer up to 3 ntp api's.
        self.NTP_HOST = os.getenv('NTP_HOST').split('|', 2)
        self.INTERVAL = os.getenv('NTP_INTERVAL')

        if self.TZ is None or self.NTP_HOST is None or self.INTERVAL is None:
            raise Exception("NTP_HOST, NTP_INTERVAL & TZ_OFFSET are stored in settings.toml, please add them")
        
        self._last_ntp_sync = None
        self.connect()


    def connect(self) -> bool:
        """ If not connected connect to the network."""
        print("connecting to: {}".format(self.SSID))
        # TODO: async methods?
        attempt = 1
        while(attempt <= self.RETRY_WIFI):
            try:
                # TODO: async methods?
                wifi.radio.connect(self.SSID, self.PASS)                        
                return True
            except Exception as e:
                print(e)
            attempt += 1
        
        raise Exception('Unable to connect')



    def get_time(self):
        pool = socketpool.SocketPool(wifi.radio)
        ntp_try = 0
        while ntp_try < len(self.NTP_HOST):
            try:
                ntp = adafruit_ntp.NTP(pool, tz_offset=self.TZ, server=self.NTP_HOST[ntp_try])
                self._last_ntp_sync = ntp.datetime
                return ntp.datetime
            except Exception as ex:
                print(f'Unable to connect to NTP Server {self.NTP_HOST[ntp_try]} with exception:', ex)
                ntp_try += 1
        raise Exception("Unable to contact NTP servers")
                                                

    def getJson(self, url):
        try:
            pool = socketpool.SocketPool(wifi.radio)
            context = ssl.create_default_context()
            #requests = adafruit_requests.Session(pool, context)
            requests = adafruit_requests.Session(pool, ssl.create_default_context())
            print(f'getting url: {url}')
            gc.collect()
            print('free memory', gc.mem_free())

            #response = requests.get(url, stream=True) 
            response = requests.get(url) 
            print('free memory after', gc.mem_free())
            return response.json()
        except Exception as e:
            print('response.json Exception:', e)
            gc.collect()
        return {}        


    def get_interval(self):
        return int(self.INTERVAL)


    def get_pool(self):
        pass


