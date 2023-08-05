from plytix.retailers.models import BaseModel


class Brand(BaseModel):
    """ Model: Brand
    """
    def __init__(self, name, website=None, picture=None, id=None):
        """
        :param name: Name.
        :param website: Website.
        :param picture: Picture.
        :param id: Identifier.
        :return:
        """
        self.id = id
        self.name = name
        self.website = website
        self.picture = picture

    def to_dict(self, include_id=True):
        """
        :return: A dictionary within the brand's field.
        """
        brand = {
            'name': self.name,
        }
        if self.id and include_id:
            brand['id'] = self.id
        if self.website:
            brand['website'] = self.website
        if self.picture:
            brand['picture'] = self.picture
        return brand

    @staticmethod
    def parse(data):
        """
        :param data: The brand data.
        :return: The brand object.
        """
        name = data['name']
        id = data.get('id', None)
        website = data.get('website', None)
        picture = data.get('picture', None)

        return Brand(name, website=website, picture=picture, id=id)
