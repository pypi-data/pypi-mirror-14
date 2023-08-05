# import pprint

import collections

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from StringIO import StringIO
from PIL import Image

import logging
import logging.handlers

NEXUS_API_URL='https://nexusapi.dropcam.com'
DROPCAM_API_URL='https://www.dropcam.com/api/v1'


class Channel(object):
    def __init__(self, user, password, logServer='localhost', logLevel=logging.DEBUG):
        self._user=user
        self._password=password
        self._proxies=None
        # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self._cams={}

        logger=logging.getLogger("NESTCAMS")
        logger.setLevel(logLevel)
        socketHandler = logging.handlers.SocketHandler(logServer, logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        logger.addHandler(socketHandler)
        self._logger=logger

        self._session=None
        self._cameras={}

    @property
    def logger(self):
        return self._logger

    def debug(self):
        import httplib as http_client
        http_client.HTTPConnection.debuglevel = 1

    def setProxies(self, proxies):
        self._proxies=proxies

    def url(self, api, call):
        if api and call:
            return '%s/%s' % (api, call)

    def urlDropcam(self, service, method):
        if method:
            call='%s.%s' % (service, method)
        else:
            call=service
        return self.url(DROPCAM_API_URL, call)

    def urlNexus(self, service):
        return self.url(NEXUS_API_URL, service)

    def login(self):
        if self._session and self._token:
            return self._session

        self.close()
        try:
            session=requests.Session()

            # some user-agent will return 403 FORBIDDEN error
            session.headers.update({'User-agent': 'python-requests/2.7.0 CPython/2.7.11 Darwin/15.2.0'})

            params={'username': self._user, 'password': self._password}
            url=self.urlDropcam('login', 'login')

            r=session.post(url, data=params, proxies=self._proxies, timeout=10.0)
            if r and r.status_code in (200, 201):
                response=r.json()
                self.logger.debug(str(response))
                if response['status'] in (0, 200, 201):
                    self._token=response['items'][0]['session_token']
                    if self._token:
                        self._session=session
                        return self._session
        except:
            # self.logger.exception('open()')
            pass
        self.logger.error('login failure')

    def open(self):
        retry=2
        while retry>=0:
            session=self.login()
            if session:
                return session
            retry-=1

    def close(self):
        if self._session is not None:
            self.logger.info('close()')
        self._session=None
        self._token=None

    def post(self, url, params=None, headers=None):
        session=self.open()
        if url and session and url:
            try:
                if not params:
                    params={}
                self.logger.debug('post(%s)%s' % (url, str(params)))
                if not headers:
                    headers={}
                r=session.post(url,
                        headers=headers,
                        data=params,
                        proxies=self._proxies,
                        timeout=10.0,
                        allow_redirects=True)
                # pprint.pprint(r.text)
                if r and r.status_code in (200, 201):
                    ctype=r.headers['content-type']
                    if ctype.find('application/json')>=0:
                        data=r.json()
                        # pprint.pprint(data)
                        self.logger.debug(str(data))
                        return data['items']
                    self.logger.warning('unsupported content-type %s' % ctype)
                    return None
            except:
                self.logger.exception('post()')
        self.close()

    def get(self, url, params=None):
        session=self.open()
        if session and url:
            try:
                if not params:
                    params={}
                self.logger.debug('get(%s)%s' % (url, str(params)))
                r=session.get(url,
                        data=params,
                        proxies=self._proxies,
                        timeout=10.0,
                        allow_redirects=True)

                if r and r.status_code in (200, 201):
                    ctype=r.headers['content-type']
                    if ctype.find('application/json')>=0:
                        data=r.json()
                        self.logger.debug(str(data))
                        return data['items']
                    if ctype.find('image/')>=0:
                        try:
                            return Image.open(StringIO(r.content))
                        except:
                            pass
                        return None
                    self.logger.warning('unsupported content-type %s' % ctype)
                    return None
            except:
                self.logger.exception('get()')
        self.close()

    def retrieveCameras(self):
        params={'group_cameras': True}
        url=self.urlDropcam('cameras', 'get_visible')
        try:
            response=self.get(url, params)[0]
            for data in response['owned']:
                try:
                    c=Camera(self, data)
                    camera=self.cameraFromUUID(c.uuid)
                    if camera:
                        camera.updateProperties(c.properties())
                        self.logger.info('Updated prpertied %s' % str(c))
                    else:
                        self._cameras[c.uuid]=c
                        self.logger.info('New %s' % str(c))
                except:
                    pass
        except:
            self.logger.exception('retrieveCameras()')
            pass

    def cameras(self, refresh=False):
        if refresh or not self._cameras:
            self.retrieveCameras()
        try:
            return self._cameras.values()
        except:
            pass

    def cameraFromUUID(self, uuid):
        if uuid:
            try:
                return self._cameras[uuid]
            except:
                pass

    def cameraFromIndex(self, index):
        try:
            return self.cameras()[index]
        except:
            pass

    def camera(self, key):
        if isinstance(key, int):
            return self.cameraFromIndex(key)
        return self.cameraFromUUID(key)

    def __get__(self, key):
        return self.camera(key)


class Camera(object):
    def __init__(self, channel, properties):
        self._channel=channel
        self._properties=properties
        if not self.uuid:
            raise Exception('Invalid camera properties')

    @property
    def channel(self):
        return self._channel

    @property
    def logger(self):
        return self.channel.logger

    def properties(self):
        return self._properties

    def updateProperties(self, properties):
        for key, value in properties.iteritems():
            if isinstance(value, collections.Mapping) and value:
                returned = self.updateProperties(self._properties.get(key, {}), value)
                self._propertie[key] = returned
            else:
                self._properties[key] = properties[key]
        return self._properties

    def getProperty(self, name, default=None):
        try:
            return self._properties[name]
        except:
            return default

    def hasCapability(self, name):
        try:
            if name and name in self.get('capabilities'):
                return True
        except:
            pass

    @property
    def uuid(self):
        return self.getProperty('uuid')

    @property
    def name(self):
        return self.getProperty('name')

    def isOnline(self):
        return bool(self.getProperty('is_online'))

    def isStreaming(self):
        return bool(self.getProperty('is_streaming'))

    def __repr__(self):
        return 'Camera(%s/%s)%s' % (self.uuid, self.name, str(self._properties))

    def refresh(self):
        params={'uuid': self.uuid}
        # 'cameras.get' may also be used
        url=self.channel.urlDropcam('cameras', 'update')
        try:
            data=self.channel.post(url, params)[0]
            self.updateProperties(data)
        except:
            pass

    def setProperty(self, name, value):
        params={'uuid': self.uuid, 'key': name, 'value': value}
        url=self.channel.urlDropcam('dropcams', 'set_property')
        try:
            data=self.channel.post(url, params)[0]
            if data:
                self.updateProperties(data)
                return data[name]==value
        except:
            self.logger.exception('setProperty()')
            pass

    def enable(self, state=True):
        return self.setProperty('streaming.enabled', state)

    def disable(self):
        return self.enable(False)

    def shoot(self, width=720):
        params={'uuid': self.uuid, 'width': width}
        url=self.channel.urlDropcam('cameras', 'get_image')
        try:
            return self.channel.get(url, params)
        except:
            self.logger.exception('shoot()')
            pass

    def save(self, fname, width=720):
        image=self.shoot(width)
        if image:
            try:
                image.save(fname)
                return True
            except:
                pass


    # def save_image(self, path, width=720, seconds=None):
    #     """
    #     Saves a camera image to disc.

    #     :param path: file path to save image
    #     :param width: image width or X resolution
    #     :param seconds: time of image capture (in seconds from epoch)
    #     :raises: ConnectionError
    #     """
    #     f = open(path, "wb")
    #     response = self.get_image(width, seconds)
    #     f.write(response.read())
    #     f.close()


if __name__ == "__main__":
    pass
