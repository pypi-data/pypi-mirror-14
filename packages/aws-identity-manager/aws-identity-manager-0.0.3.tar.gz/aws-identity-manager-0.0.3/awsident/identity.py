import json

class AttrProp(object):
    def __init__(self, name):
        self.name = name
    def __get__(self, obj, objtype):
        return getattr(obj, self.name)
    def __set__(self, obj, value):
        attr_name = self.name.lstrip('_')
        old = getattr(obj, self.name)
        setattr(obj, self.name, value)
        if obj.storage is not None:
            obj.storage.on_identity_update(identity=obj,
                                           attr=attr_name,
                                           old=old,
                                           value=value)

class Identity(object):
    """Representation of an AWS identity

    Stores identity name and credentials
    """
    __slots__ = ['_name', '_access_key_id', '_secret_access_key', 'storage']
    def __init__(self, **kwargs):
        self._name = kwargs.get('name')
        self._access_key_id = kwargs.get('access_key_id')
        self._secret_access_key = kwargs.get('secret_access_key')
        self.storage = kwargs.get('storage')
    @property
    def id(self):
        return self.access_key_id
    name = AttrProp('_name')
    access_key_id = AttrProp('_access_key_id')
    secret_access_key = AttrProp('_secret_access_key')
    def __eq__(self, other):
        if not isinstance(other, Identity):
            return False
        for attr in self.__slots__:
            if attr == 'storage':
                continue
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True
    def __ne__(self, other):
        if not isinstance(other, Identity):
            return True
        for attr in self.__slots__:
            if getattr(self, attr) != getattr(other, attr):
                return True
        return False
    def __repr__(self):
        return '<Identity: {0} ({1})>'.format(self, self.id)
    def __str__(self):
        return self.name

class IdentityEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Identity):
            keys = (k.lstrip('_') for k in obj.__slots__ if k.startswith('_'))
            return {k:getattr(obj, k) for k in keys}
        return super(IdentityEncoder, self).default(obj)
