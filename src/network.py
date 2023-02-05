## Class for handling networking. 
import os
import wifi
import socketpool
import adafruit_ntp


class BaseNetwork:
    def __init__(self) -> None:
        self.RETRY_WIFI = 5 # Number of times to attempt to connect to wifi
        self.SSID = os.getenv('WIFI_SSID')
        self.PASS = os.getenv('WIFI_PASSWORD')

        if len(self.SSID) == 0 or len(self.PASS) == 0:
            raise Exception("WIFI_SSID & WIFI_PASSWORD are stored in settings.toml, please add them")

        # NTP specific constants
        self.TZ = os.getenv('TZ_OFFSET')
        self.NTP_HOST = os.getenv('NTP_HOST')
        self.INTERVAL = os.getenv('NTP_INTERVAL')

        print(self.TZ)
        print(self.NTP_HOST)
        print(self.INTERVAL)
        # TODO: validate this ase on what the return is from an empty getenv call

        #if len(self.TZ) == 0 or len(self.NTP_HOST) == 0 or len(self.INTERVAL) == 0:
        #    raise Exception("NTP_HOST, NTP_INTERVAL & TZ_OFFSET are stored in settings.toml, please add them")
        

    def connect(self) -> bool:
        """ If not connected connect to the network."""
        attempt = 1
        while(attempt <= self.network.RETRY_WIFI):
            try:
                if wifi.radio.ipv4_address is None:
                    print("connecting to: {}".format(self.SSID))
                    # TODO: async methods?
                    wifi.radio.connect(self.network.SSID, self.network.PASS)                    
                else:
                    print("already connected with IP: ".format(wifi.radio.ipv4_address))

                return True
            except Exception as e:
                print(e)

            attempt += 1
        raise Exception('Unable to connect')


    def get_time(self):
        # Need better connection testing
        if wifi.radio.ipv4_address is None:
            self.connect()
        pool = socketpool.SocketPool(wifi.radio)
        ntp = adafruit_ntp.NTP(pool, tz_offset=self.TZ, server=self.NTP_HOST)
        return ntp.datetime
                    

    def get_interval(self):
        return int(self.INTERVAL)


    def get_pool(self):
        pass


