import os
import StringIO
import io
import time
import sys, logging, logging.handlers
import traceback
#import urlparse
#import ftplib
from threading import RLock
from threading import Thread
from threading import Event
from Queue import Queue
import math
import urllib2

from PIL import Image
from PIL import ImageEnhance


class WebcamURLProvider(object):
    def __init__(self, url=None):
        self._url=url

    def build(self):
        return self._url

    def get(self):
        return self.build()


class WebcamURLProviderACTI(WebcamURLProvider):
    def __init__(self, host, user, password):
        baseUrl='http://{0}/cgi-bin/encoder?USER={1}&PWD={2}&SNAPSHOT'.format(host, user, password)
        WebcamURLProvider.__init__(self, baseUrl)


#custom provider for http://panorama.simwatch.ch/images/Tzoumaz/2013/08/30/09-00.jpg
class WebcamURLProviderSimwatch(WebcamURLProvider):
    def __init__(self, site='Tzoumaz', timeResolution=30):
        baseUrl='{0}/{1}'.format('http://panorama.simwatch.ch/images', site)
        WebcamURLProvider.__init__(self, baseUrl)
        self.setTimeResolution(timeResolution)

    def setTimeResolution(self, minutes=30):
        self._timeResolution=minutes

    def build(self):
        ltime=time.localtime()
        # rewrite as 2013/08/30/09-00
        urlExt='%d/%02d/%02d/%02d-%02d' % (
            ltime.tm_year,
            ltime.tm_mon,
            ltime.tm_mday,
            ltime.tm_hour,
            (ltime.tm_min//self._timeResolution)*self._timeResolution
        )
        url='{0}/{1}.jpg'.format(self._url, urlExt)
        return url


class Webcam(object):
    def __init__(self, rootid, camid, urlProvider, httpusername=None, httppassword=None, logger=None):
        self._lock=RLock()
        self._rootPath = os.path.join('c:/', 'temp', 'cam')
        self._rootid = rootid or 'generic'
        self._camid = camid or 'mycam'
        self._urlProvider = urlProvider
        self._image=None
        self._imageStamp=0
        self._imageCropBox=None
        self._imageSharpnessEnhancer=1.0
        self._rootPath=None
        self._storageMaxAge=0
        self._eventShoot=Event()
        self._eventStop=Event()
        self._burst=False
        self._burstStamp=0
        self._burstIndex=0
        self._burstFiles=[]
        self._shootPeriod=0
        self._shootCounter=0
        self._cleanTrigger=0
        self._threadManager=None
        self._error=0

        if not logger:
            logger=logging.getLogger("CAM")
            logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler(sys.stdout)
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s:%(name)s::%(levelname)s::%(message)s')
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        self._logger=logger

        self.setImageWidth(0, 240)

        if httpusername:
            pw_manager=urllib2.HTTPPasswordMgrWithDefaultRealm()
            pw_manager.add_password(None,
                uri=self._urlProvider.get(),
                user=httpusername,
                passwd=httppassword)

            auth_handler=urllib2.HTTPBasicAuthHandler(pw_manager)
            opener=urllib2.build_opener(auth_handler)
            urllib2.install_opener(opener)

    @property
    def logger(self):
        return self._logger

    def burstCreateContactSheet(self, files):
        if files:
            try:
                cs=ContactSheet(240, 4, 1)
                self.logger.info('%s/creating contact sheet from burst/%s...' % (self._camid, self._burstStamp))
                cs.createFromFiles(files)
                cs.save(os.path.join(self.getStoragePath(), 'burst', 'contactsheet', self._burstStamp+'.jpg'))
            except:
                pass

    def burst(self, enable=True):
        if bool(enable)!=self._burst:
            self._burst=bool(enable)
            self.logger.info('%s/burst(%d)' % (self._camid, int(enable)))
            if enable:
                self._burstStamp=time.localtime()
                self._burstIndex=0
                self._burstFiles=[]
                self._eventShoot.set()
            else:
                #self.burstCreateContactSheet(self._burstFiles)
                self._burstFiles=[]

    def setStorageMaxAge(self, maxAge=0):
        self._storageMaxAge=maxAge

    def setStoragePath(self, path):
        self._rootPath=path
        self.prepareStorage()

    def getStoragePath(self):
        return os.path.join(self._rootPath, self._rootid, self._camid)

    def createDir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def prepareStorage(self):
        if self._rootPath:
            try:
                self.createDir(os.path.join(self.getStoragePath(), 'thumbnail'))
                self.createDir(os.path.join(self.getStoragePath(), 'poll'))
                self.createDir(os.path.join(self.getStoragePath(), 'burst/contactsheet'))
                return True
            except:
                pass

    def setImageCropBox(self, box):
        self._imageCropBox=box

    def setImageSharpnessEnhancer(self, factor):
        self._imageSharpnessEnhancer=factor

    def setImageWidth(self, imageWidth=0, thumbnailWidth=0):
        self._imageWidth=imageWidth
        self._thumbnailWidth=thumbnailWidth

    def jpeg(self):
        with self._lock:
            try:
                if self._image:
                    buf = StringIO.StringIO()
                    self._image.save(buf, "JPEG")
                    return buf.getvalue()
                    # buf=io.BytesIO()
                    # self._image.save(buf, format= 'JPEG')
                    # buf.seek(0)
                    # value=buf.getvalue()
                    # buf.close()
                    # return value
            except:
                #traceback.print_exc(file=sys.stdout)
                self.logger.error('%s/jpeg() error occured while processing image' % (self._camid))

    def getResizedImage(self, width=640):
        with self._lock:
            wx,wy = self._image.size
            if wy>wx:
                ratio=(1.0 * width)/wy
                wy=width
                wx=int(wx*ratio)
            else:
                ratio=(1.0 * width)/wx
                wx=width
                wy=int(wy*ratio)

            try:
                image = self._image.resize((wx, wy), Image.ANTIALIAS)
                return image
            except:
                pass

    def shoot(self):
        image=None
        try:
            urlRequest=urllib2.Request(self._urlProvider.get())
            r=urllib2.urlopen(urlRequest, None, 15)
            try:
                data=r.read()
                image=Image.open(StringIO.StringIO(data))
                if self._imageCropBox:
                    image=image.crop(self._imageCropBox)

                if self._imageSharpnessEnhancer!=1.0:
                    enhancer=ImageEnhance.Sharpness(image)
                    image=enhancer.enhance(self._imageSharpnessEnhancer)

                with self._lock:
                    self._image=image
                    self._error=0
                    self.saveCurrentImage()
                    self._imageStamp=time.localtime()
            except:
                image=None
                self.logger.error(traceback.format_exc())
            finally:
                r.close()
        except:
            self.logger.error(traceback.format_exc())

        if image is None:
            self._error+=1
            self.logger.error('%s/shoot(%d)' % (self._camid, self._error))

        return image

    def error(self):
        with self._lock:
            return self._error

    def shootRequest(self, counter=1):
        with self._lock:
            if counter<=0:
                counter=1
            self._shootCounter=counter
            self._eventShoot.set()

    def setShootPeriod(self, period):
        self._shootPeriod=period
        self._eventShoot.set()

    def getPollImageStamp(self):
        sformat='%Y%m%d-%H%M%S'
        return '%s-poll' % time.strftime(sformat, self._imageStamp)

    def getBurstImageStamp(self, withIndex=True):
        sformat='%Y%m%d-%H%M%S'
        if withIndex:
            return '%s-burst-%d' % (time.strftime(sformat, self._burstStamp), self._burstIndex)
        else:
            return '%s-burst' % time.strftime(sformat, self._burstStamp)

    def createFileFromImage(self, fpath, width=0):
        try:
            self.logger.info('%s/shoot(%s)' % (self._camid, fpath))
            self.prepareStorage()
            with self._lock:
                image=self._image
                if width>0:
                    image=self.getResizedImage(width)
                image.save(fpath+'.jpg')
        except:
            pass

    def saveCurrentImage(self):
        try:
            if self._burst:
                stamp=self.getBurstImageStamp()
                fpath=os.path.join(self.getStoragePath(), 'burst', stamp)
                self._burstFiles.append(fpath)
                self._burstIndex+=1
            else:
                stamp=self.getPollImageStamp()
                fpath=os.path.join(self.getStoragePath(), 'poll', stamp)

            self.createFileFromImage(fpath, self._imageWidth)

            if self._thumbnailWidth>0:
                if not self._burst or self._burstIndex==0:
                    fpath=os.path.join(self.getStoragePath(), 'thumbnail', stamp)
                    self.createFileFromImage(fpath, self._thumbnailWidth)
        except:
            pass

    def cleanStorage(self):
        if self._rootPath:
            self.prepareStorage()
            if self._storageMaxAge>0:
                try:
                    ttrigger=time.time()-self._storageMaxAge
                    path=self.getStoragePath()
                    for root, dirs, files in os.walk(path):
                        for fname in files:
                            if os.path.splitext(fname)[1].lower()=='.jpg':
                                fpath=os.path.join(root, fname)
                                if os.path.getmtime(fpath)<ttrigger:
                                    self.logger.info('%s/prune(%s)' % (self._camid, fpath))
                                    os.remove(fpath)
                except:
                    pass

    def manager(self):
        while 1:
            self._eventShoot.wait(self._shootPeriod)
            if self._eventStop.isSet():
                break
            result=self.shoot()
            if not self._burst:
                self._eventShoot.clear()
                if self._shootCounter>0:
                    self.logger.warning('%s/reshoot(%d)' % (self._camid, self._shootCounter))
                    self._shootCounter-=1
                    if self._shootCounter>0 and not self._eventStop.isSet():
                        self._eventShoot.set()
                else:
                    if time.time()>self._cleanTrigger:
                        self.cleanStorage()
                        self._cleanTrigger=time.time()+3600


    def start(self):
        self._eventStop.clear()
        self._eventShoot.set()
        self._threadManager=Thread(target=self.manager)
        self.logger.info('%s:manager started' % self._camid)
        self._threadManager.start()


    def stop(self):
        self._eventShoot.set()
        self._eventStop.set()
        self.logger.info('%s:stop requested!' % self._camid)

    def waitForStopDone(self):
        if self._threadManager.isAlive():
            self._threadManager.join()
        self.logger.info('%s:manager stopped' % self._camid)


class WebcamManager(object):
    def __init__(self):
        self._cams=[]

    def addCam(self, cam):
        self._cams.append(cam)

    def cams(self):
        return self._cams

    def start(self):
        for cam in self.cams():
            cam.start()

    def stop(self):
        for cam in self.cams():
            cam.stop()

        for cam in self.cams():
            cam.waitForStopDone()

    def serveForEver(self):
        self.start()

        try:
            while 1:
                time.sleep(1)
        except:
            pass

        self.stop()


class ContactSheet(object):
    def __init__(self, wx=240, nbcol=4, margin=5):
        self._image=None
        self._wx=wx
        self._nbcol=nbcol
        self._margin=margin

    def resizeImage(self, image, width):
        wx,wy = image.size
        if wy>wx:
            ratio=(1.0 * width)/wy
            wy=width
            wx=int(wx*ratio)
        else:
            ratio=(1.0 * width)/wx
            wx=width
            wy=int(wy*ratio)
        try:
            return image.resize((wx, wy), Image.ANTIALIAS)
        except:
            pass

    def createFromFiles(self, files, crop=0):
        col=0
        row=0
        for fpath in files:
            try:
                image=Image.open(fpath)
                image=self.resizeImage(image, self._wx)
                if crop:
                    image=image.crop((crop, crop, wx-crop*2, wy-crop*2))
                    image.load()

                (wx,wy)=image.size

                if not self._image:
                    width=self._margin+(self._nbcol*(self._wx+self._margin))
                    height=self._margin+(int(float(len(files))/self._nbcol+0.5)*(wy+self._margin))
                    self._image=Image.new('RGB', (width, height), 'black')

                self._image.paste(image, (self._margin+col*(self._wx+self._margin), self._margin+row*(wy+self._margin)))

                col+=1
                if col>=self._nbcol:
                    row+=1
                    col=0
            except:
                pass
        return self._image

    def save(self, fpath):
        try:
            self._image.save(fpath)
        except:
            pass

