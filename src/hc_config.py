import time
import pychromecast
from multiprocessing import Process

class home_cinema():
    def __init__(self):
        self.a_cast = None
        self.v_cast = None
        self.v_mc = None
        self.a_mc = None
        self.services, self.browser = pychromecast.discovery.discover_chromecasts()
        pychromecast.discovery.stop_discovery(self.browser)
        # p = Process(target=self.monitoring, args=(10,))
        # p.start()
    
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
        pychromecast.discovery.stop_discovery(self.browser)
    
    def synchro(self, tolerance = 0.10, DT=2):
        # TODO: resolve synchro and manual play/pause uncompatibility
        # TODO: status whithout pausing
        self.pause()
        tv = self.v_mc.status.current_time
        ta = self.a_mc.status.current_time
        print(tv-ta)
        if  tv-ta > tolerance:
            print('tv-ta', tv-ta)
            self.a_mc.play()
            time.sleep((tv-ta)/DT)
            self.v_mc.play()
            return (tv-ta)
        elif ta-tv > tolerance:
            print('ta-tv', ta-tv)
            self.v_mc.play()
            time.sleep((ta-tv)/DT)
            self.a_mc.play()
            return (ta-tv)
        else:
            self.play()
            return 0

    def getTime(self):
        tt = self.v_mc.status.current_time
        return tt
    
    def getVStatus(self):
        # TODO: 'current time' does not reactualize need to be paused ...
        status = self.v_mc.status
        return status

    def getAStatus(self):
        # TODO: 'current time' does not reactualize need to be paused ...
        status = self.a_mc.status
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
        # TODO: without the "sleep step ?"
        self.v_mc.play_media(url, 'video/mp4')
        self.a_mc.play_media(url, 'video/mp4')
        time.sleep(2)
        self.calibration(max_ite=20)

    def pause(self):
        self.v_mc.pause()
        self.a_mc.pause()

    def play(self):
        self.v_mc.play()
        self.a_mc.play()

    def monitoring(self, timestep):
       ##TODO: monitor inside a worker, the state of v_mc and a_mc in order to synchro
       while 1:
           time.sleep(timestep)
           print('Monitoring ...')
           if not isinstance(self.a_mc, type(None)):
               self.synchro()

    def calibration(self, sleeptime = 10, tolerance = 0.10, max_ite = 10, DT=2):
        calib = False
        delays = [1,1,1]
        for i in range(max_ite):
            if not (calib):
                tt = self.synchro(tolerance=tolerance, DT=DT)
                delays.append(tt)
                time.sleep(sleeptime)
                if (delays[-1] + delays[-2] + delays[-3] == 0):
                    calib = True
        if not (calib):
            for i in range(max_ite):
                if not (calib):
                    tt = self.synchro(tolerance=tolerance, DT=DT/2)
                    delays.append(tt)
                    time.sleep(sleeptime)
                    if (delays[-1] + delays[-2] + delays[-3] == 0):
                        calib = True
        return 0 