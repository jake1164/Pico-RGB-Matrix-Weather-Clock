import os
import wifi
import socketpool
import adafruit_ntp


class NtpClient:
    def __init__(self, network) -> None:
        super().__init__()
        self.network = network
        self.RETRY = 5 # Number of times to attempt to connect to wifi
        self.TZ = os.getenv('TZ_OFFSET')
        self.NTP_HOST = os.getenv('NTP_HOST')
        self.INTERVAL = os.getenv('NTP_INTERVAL')


    def get_time(self):
        # Need better connection testing
        attempt = 1
        while(attempt <= self.network.RETRY_WIFI):
            print('attempting to get time: try ', attempt)
            try:
                if wifi.radio.ipv4_address is not None:
                    pool = socketpool.SocketPool(wifi.radio)
                    ntp = adafruit_ntp.NTP(pool, tz_offset=self.TZ, server=self.NTP_HOST)
                    return ntp.datetime
                else:
                    wifi.radio.connect(self.network.SSID, self.network.PASS)
                    pool = socketpool.SocketPool(wifi.radio)
                    ntp = adafruit_ntp.NTP(pool, tz_offset=self.TZ, server=self.NTP_HOST)
                    return ntp.datetime
            except Exception as e:
                print(e)
                
            attempt += 1
        raise Exception('Unable to connect')


    def get_interval(self):
        return int(self.INTERVAL)