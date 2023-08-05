from plytix.retailers.fields import *
from plytix.retailers.models import BaseModel
from plytix.retailers.models.product import Product


class Folder(BaseModel):
    """ Model: Folder
    """
    def __init__(self, name=None, id=None, folders=None, products=None, parent=None):
        """
        :param name: Name.
        :param id: Identifier.
        :param folders: Children folders.
        :param products: Children products.
        :param parent: Parent folder.
        :return:
        """
        self.name = name
        self.id = id
        self.folders = folders
        self.products = products
        self.parent = parent

    def __repr__(self):
        return 'Folder:{}'.format(self.name)

    def to_dict(self, include_id=True, complete=False):
        """
        :return: A dictionary within the folder's fields.
        """
        folder = {
            'name': self.name
        }
        if self.id:
            folder['id'] = self.id
        if complete:
            if self.folders:
                folder[MODEL_FOLDERS] = [f.to_dict() for f in self.folders]
            if self.products:
                folder[MODEL_PRODUCTS] = [p.to_dict() for p in self.products]
            folder['parent'] = self.parent

        return folder

    @staticmethod
    def parse(data):
        """
        :param data: Response's data that includes a folder.
        :return: The Folder object.
        """
        id = data.get('id', None)
        name = data.get('name', None)
        parent = data.get('parent', None)

        folders = None
        if MODEL_FOLDERS in data and data[MODEL_FOLDERS]:
            folders = [Folder.parse(folder) for folder in data[MODEL_FOLDERS]]

        products = None
        if MODEL_PRODUCTS in data and data[MODEL_PRODUCTS]:
            products = [Product.parse(product) for product in data[MODEL_PRODUCTS]]

        return Folder(name=name, id=id, folders=folders, products=products, parent=parent)


