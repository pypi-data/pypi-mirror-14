import requests
import datetime


class Package:
    def __init__(self, package_name=None):
        self.host = 'https://pypi.python.org/pypi/%s/json' % package_name
        self.HTTP = requests.session()

    def convert_to_int_or_float(self, value):
        '''
        :param value: Value to convert
        :return: Inputted value as int or float
        '''
        if not isinstance(value, str):
            return value

        if value.isdigit():
            return int(value)

        try:
            return float(value)
        except ValueError:
            return value

    def request(self, url, object=None, params={}, json=False):
        '''
        :param url: Host name
        :param object: Object to convert response to
        :param params: Parameters to send to host
        :param json: Return raw json data
        :return: JSON or object
        '''
        response = self.HTTP.get(url, params=params)
        if json:
            return response

        if object is not None:
            if response.status_code == 400:
                raise ConnectionAbortedError('Invalid package name')

            dictionary = response.json()
            return self.objectify(object, dictionary)

    def fetch(self):
        '''
        Fetch data from PyPI API
        '''
        self.request(self.host, Package)

    def objectify(self, object, data):
        '''
        :param object: Object to return instance
        :param data: dictionary to objectify
        :return: Instance of object
        '''
        instance = object()

        for key, item in data.items():
            if isinstance(instance, Package):
                if key == 'releases':
                    releases = []
                    for release_key, release_item in item.items():
                        release_item[0]['version'] = release_key
                        releases.append(self.objectify(Release, release_item[0]))
                    item = releases

                elif key == 'urls':
                    item = [self.objectify(URL, url_item) for url_item in item]

                elif key == 'info':
                    for info_key, info_item in item.items():
                        if info_key == 'downloads':
                            info_item = self.objectify(Downloads, info_item)

                        setattr(self, info_key, info_item)

                setattr(self, key, item)
                continue

            if isinstance(instance, Release) or isinstance(instance, URL):
                if key == 'upload_time':
                    item = datetime.datetime.strptime(item, '%Y-%m-%dT%H:%M:%S')

            setattr(instance, key, item)
        return instance


class Release:
    def __repr__(self):
        return '<Release %s>' % self.version


class URL:
    def __repr__(self):
        return '<URL>'


class Downloads:
    def __repr__(self):
        return '<Downloads>'
