## Class for handling networking.
import os
import gc
import wifi
import socketpool
import adafruit_ntp
import adafruit_requests
import adafruit_connection_manager

class WifiNetwork:
    def __init__(self) -> None:
        self.RETRY_WIFI = 5 # Number of times to attempt to connect to wifi
        self.SSID = os.getenv('WIFI_SSID')
        self.PASS = os.getenv('WIFI_PASSWORD')

        if self.SSID is None or self.PASS is None or len(self.SSID) == 0 or len(self.PASS) == 0:
            raise Exception("WIFI_SSID & WIFI_PASSWORD are stored in settings.toml, please add them")

        # NTP specific constants
        self.TZ = os.getenv('TZ_OFFSET')
        self.INTERVAL = os.getenv('NTP_INTERVAL')

        # Offer up to 3 ntp api's.
        hosts = os.getenv('NTP_HOST')
        self.NTP_HOST = hosts.split('|') if hosts else None

        if self.TZ is None or self.NTP_HOST is None or self.INTERVAL is None:
            raise Exception("NTP_HOST, NTP_INTERVAL & TZ_OFFSET are stored in settings.toml, please add them")

        self._last_ntp_sync = None
        self.connect()
        ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
        self._pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
        self._requests = adafruit_requests.Session(self._pool, ssl_context)
        self._connection_manager = adafruit_connection_manager.get_connection_manager(self._pool)


    def connect(self) -> bool:
        """ If not connected connect to the network."""
        print("connecting to: {}".format(self.SSID))
        # TODO: async methods?
        attempt = 1
        error = None
        while(attempt <= self.RETRY_WIFI):
            try:
                # TODO: async methods?
                wifi.radio.connect(self.SSID, self.PASS)
                return True
            except Exception as e:
                error = str(e)
                print(e)
            attempt += 1

        raise Exception(error)



    def get_time(self):
        ntp_try = 0
        while ntp_try < len(self.NTP_HOST):
            try:
                ntp = adafruit_ntp.NTP(self._pool, tz_offset=self.TZ, server=self.NTP_HOST[ntp_try])
                self._last_ntp_sync = ntp.datetime
                return ntp.datetime
            except Exception as ex:
                print(f'Unable to connect to NTP Server {self.NTP_HOST[ntp_try]} with exception:', ex)
                ntp_try += 1
        raise Exception("Unable to contact NTP servers")
                                                

    def getJson(self, url):
        try:
            print(f'getting url: {url}')
            gc.collect()
            print('free memory', gc.mem_free())
            with self._requests.get(url) as response:
                print(f'free memory after: {gc.mem_free()} socket count: {self._connection_manager.managed_socket_count}: available: {self._connection_manager.available_socket_count}')
                return response.json()
        except Exception as e:
            print('response.json Exception:', e)
            print(f'free memory: {gc.mem_free()} socket count: {self._connection_manager.managed_socket_count}: available: {self._connection_manager.available_socket_count}')
            gc.collect()
        return {}        


    def get_interval(self):
        return int(self.INTERVAL)


    def get_pool(self):
        pass


