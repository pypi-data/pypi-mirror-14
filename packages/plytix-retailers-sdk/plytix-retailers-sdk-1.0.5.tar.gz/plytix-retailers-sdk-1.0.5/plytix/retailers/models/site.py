from plytix.retailers.exceptions import *
from plytix.retailers.models import BaseModel


class PictureSize(object):
    """ Single picture size of a site.
    """
    def __init__(self, width, height):
        """ Initialize a PictureSize object
        :param width: Width of the size.
        :param height: Height of the size.
        :return: The picture size initialized.
        """
        if not isinstance(width, int):
            raise ValueError('Incorrect width type')
        if not isinstance(height, int):
            raise ValueError('Incorrect width type')

        self.width = width
        self.height = height

    def to_dict(self):
        return {'width': self.width, 'height': self.height}


class Site(BaseModel):
    """ Model: Site
    """
    def __init__(self, debug, name, large_size, medium_size, small_size, protocol, timezone, url, id=None):
        """ Initialize a site object.
        :param debug: Test mode.
        :param name: Name.
        :param large_size: Large picture size.
        :param medium_size: Medium picture size.
        :param small_size: Small picture size.
        :param protocol: Protocol.
        :param timezone: Timezone.
        :param url: Url.
        :param id: Identifier.
        :return: The site object.
        """
        if large_size and not isinstance(large_size, PictureSize):
            raise TypeError('Large size must be a PictureSize instance.')
        if medium_size and not isinstance(medium_size, PictureSize):
            raise TypeError('Medium size must be a PictureSize instance.')
        if small_size and not isinstance(small_size, PictureSize):
            raise TypeError('Small size must be a PictureSize instance.')

        self.debug = debug
        self.name = name
        self.large_size = large_size
        self.medium_size = medium_size
        self.small_size = small_size
        self.protocol = protocol
        self.timezone = timezone
        self.url = url
        self.id = id

    def to_dict(self, include_id=True):
        """
        :return: A dictionary within the site's fields.
        """
        try:
            site = {
                'debug': self.debug,
                'name': self.name,
                'url': self.url,

            }
            picture_sizes = {} if self.large_size or self.medium_size or self.small_size else {}
            if self.large_size:
                picture_sizes['large'] = self.large_size.to_dict()
            if self.medium_size:
                picture_sizes['medium'] = self.medium_size.to_dict()
            if self.small_size:
                picture_sizes['small'] = self.small_size.to_dict()
            if picture_sizes:
                site['picture_sizes'] = picture_sizes

            if self.protocol:
                site['protocol'] = self.protocol

            if self.timezone:
                site['timezone'] = self.timezone

            if self.id and include_id:
                site['id'] = self.id
            return site
        except Exception as e:
            raise BadRequestError

    @staticmethod
    def parse(data):
        id = data.get('id', None)
        debug = data.get('debug', None)
        name = data.get('name', None)
        large = None
        medium = None
        small = None
        if 'picture_sizes' in data:
            large = PictureSize(width=data['picture_sizes']['large']['width'],
                                height=data['picture_sizes']['large']['height'])
            medium = PictureSize(width=data['picture_sizes']['medium']['width'],
                                 height=data['picture_sizes']['medium']['height'])
            small = PictureSize(width=data['picture_sizes']['small']['width'],
                                height=data['picture_sizes']['small']['height'])
        protocol = data.get('protocol', None)
        timezone = data.get('timezone', None)
        url = data.get('url', None)

        return Site(debug=debug, name=name, protocol=protocol, timezone=timezone, url=url,
                    id=id, large_size=large, medium_size=medium, small_size=small)

