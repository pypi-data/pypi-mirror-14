from plytix.retailers import enum
from plytix.retailers.fields import *
from plytix.retailers.models import BaseModel


PRODUCT_OWNERSHIP = enum(ALL='ALL', OWN='OWN', THIRD='THIRD')


class Product(BaseModel):
    """ Model: Product
    """
    def __init__(self, name, ean, gtin, jan, sku, upc, folder, thumb=None, id=None, brand_id=None, brand_name=None):
        """
        :param name: Name.
        :param owner: Owner.
        :param sku: SKU.
        :param folder: Parent folder.
        :param thumb: Thumbnail.
        :param id: Identifier.
        :param brand_id: Product's brand identifier.
        :param brand_name: Product's brand name.
        :return:
        """
        self.id = id
        self.name = name
        self.ean = ean
        self.gtin = gtin
        self.jan = jan
        self.sku = sku
        self.upc = upc
        self.thumb = thumb
        self.folder = folder

        self.brand_id = brand_id
        self.brand_name = brand_name

    def to_dict(self, include_id=True):
        """
        :return: A dictionary within the product's field.
        """
        product = {
            'name': self.name,
            'ean': self.ean,
            'gtin': self.gtin,
            'jan': self.jan,
            'sku': self.sku,
            'upc': self.upc,
            'folder': self.folder,
        }
        if self.id and include_id:
            product['id'] = self.id
        if self.thumb:
            product['thumb'] = self.thumb
        if self.brand_id:
            product['brand_id'] = self.brand_id
        if self.brand_name:
            product['brand_name'] = self.brand_name
        return product

    @staticmethod
    def parse(data):
        """
        :param data: The product data.
        :return: The Product object.
        """
        id = data['id']
        name = data['name']
        ean = data['ean']
        gtin = data['gtin']
        jan = data['jan']
        sku = data['sku']
        upc = data['upc']
        thumb = data['thumb']
        folder = data['folder']
        brand_id = data.get('brand_id', None)
        brand_name = data.get('brand_name', None)

        return Product(name, ean, gtin, jan, sku, upc, folder, thumb=thumb, id=id, brand_id=brand_id, brand_name=brand_name)


class Picture(BaseModel):
    """ Model: Picture
    """
    def __init__(self, **kwargs):
        """
        :param kwargs: Contains a dictionary of size keys and url values.
        :return:
        """
        self._sizes = []
        for size, pic in kwargs.items():
            setattr(self, size, pic)
            self._sizes.append(size)

    def to_dict(self):
        """
        :return: A dictionary within the Picture's field.
        """
        picture = {}
        for size in self._sizes:
            picture[size] = getattr(self, size, '')
        return picture

    @staticmethod
    def parse(data):
        """
        :param data: The Picture data.
        :return: The Picture object.
        """
        return Picture(**data)


class ProductPictures(BaseModel):
    """ Model: ProductPictures
    """
    def __init__(self, id, pictures):
        """
        :param id: Identifier.
        :param pictures: List of the product pictures in all sizes.
        :return:
        """
        self.id = id
        self.pictures = pictures

    def to_dict(self):
        """
        :return: A dictionary within the product's field.
        """
        product = {
            'id': self.id,
            'pictures': [picture.to_dict() for picture in self.pictures],
        }
        return product

    @staticmethod
    def parse(data):
        """
        :param data: The product data.
        :return: The ProductPictures object.
        """
        id = data['id']
        pictures = [Picture.parse(picture) for picture in data['pictures']]
        return ProductPictures(id, pictures)