import time
import pychromecast

class home_cinema():
    def __init__(self):
        self.a_cast = None
        self.v_cast = None
        self.v_mc = None
        self.a_mc = None
        self.services, self.browser = pychromecast.discovery.discover_chromecasts()
        pychromecast.discovery.stop_discovery(self.browser)
    
    def config(self, v_name, a_name):
        print(v_name, a_name)
        
        chromecasts, self.browser = pychromecast.get_listed_chromecasts(friendly_names=[v_name])
        print(chromecasts)
        self.v_cast = chromecasts[0]
        self.v_cast.wait()
        self.v_mc = self.v_cast.media_controller
        
        
        chromecasts, self.browser = pychromecast.get_listed_chromecasts(friendly_names=[a_name])
        print(chromecasts)
        self.a_cast = chromecasts[0]
        self.a_cast.wait()
        self.a_mc = self.a_cast.media_controller
        # pychromecast.discovery.stop_discovery(browser)
    
    def synchro(self, tolerance = 0.25 ):
        self.v_mc.pause()
        self.a_mc.pause()
        tv = self.v_mc.status.current_time
        ta = self.a_mc.status.current_time
        if tv > ta and tv-ta > tolerance:
            self.v_mc.play()
            time.sleep(tv-ta)
            self.a_mc.play()
        elif ta > tv and ta-tv > tolerance:
            self.a_mc.play()
            time.sleep(ta-tv)
            self.v_mc.play()
        else:
            self.v_mc.play()
            self.a_mc.play()

    def getTime(self):
        tt = self.v_mc.status.current_time
        return tt
    
    def getVStatus(self):
        status = self.v_mc.status
        return status

    def getDevices(self):
        list_devices = []
        services, browser = pychromecast.discovery.discover_chromecasts()
        for uuid, service in browser.services.items():
            print(service)
            list_devices.append({'friendly_name':service.friendly_name})
        pychromecast.discovery.stop_discovery(browser)
        return list_devices
    
    def seek(self, time):
        self.v_mc.seek(time)
        self.a_mc.seek(time)

    def playUrl(self, url):
        self.v_mc.play_media(url, 'video/mp4')
        self.a_mc.play_media(url, 'video/mp4')
        time.sleep(7)
        self.pause()
        self.seek(1)
        self.play()
        time.sleep(10)
        self.synchro()

    def pause(self):
        self.v_mc.pause()
        self.a_mc.pause()

    def play(self):
        self.v_mc.play()
        self.a_mc.play()