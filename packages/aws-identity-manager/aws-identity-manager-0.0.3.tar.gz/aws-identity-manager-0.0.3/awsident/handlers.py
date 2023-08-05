import os
import stat
import shutil
import datetime
import json
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from awsident.identity import Identity
from awsident.storage import identity_store

class ConfigHandler(object):
    """Handler for getting and setting config file credentials

    """
    conf_root = '~'
    conf_filename = None
    section_name = 'default'
    attr_map = {
        'access_key_id':'aws_access_key_id',
        'secret_access_key':'aws_secret_access_key',
    }
    handler_config_path = os.path.expanduser('~/.aws-identity-manager')
    handler_config_attrs = [
        'conf_root', 'conf_filename', 'section_name', 'attr_map',
    ]
    def __init__(self, conf=None):
        self.update_from_handler_config(conf)
    @classmethod
    def save_identity(cls, identity=None):
        """Saves any currently configured credentials to an :class:`Identity`

        """
        if identity is None:
            now = datetime.datetime.now()
            name = now.strftime('Saved Identity - %Y%m%d-%H%M%S')
            identity = Identity(name=name)
        for h in ConfigHandler.build_handlers():
            h._save_identity(identity)
        identity_store.add_identity(identity)
        return identity
    @classmethod
    def change_identity(cls, identity):
        """Sets all config files to the credentials of the provided :class:`Identity`

        """
        if not isinstance(identity, Identity):
            identity = identity_store.get(identity)
        assert identity is not None
        for h in ConfigHandler.build_handlers():
            h._change_identity(identity)
        return identity
    @classmethod
    def build_handlers(cls, conf=None):
        if conf is None:
            conf = cls.read_handler_config()
        handlers = []
        for _cls in cls.__subclasses__():
            handlers.append(_cls(conf))
        cls.write_handler_config(handlers)
        return handlers
    @classmethod
    def read_handler_config(cls):
        fn = os.path.join(cls.handler_config_path, 'handlers.json')
        if not os.path.exists(fn):
            return
        with open(fn, 'r') as f:
            s = f.read()
        return json.loads(s)
    @classmethod
    def write_handler_config(cls, handlers):
        fn = os.path.join(cls.handler_config_path, 'handlers.json')
        if not os.path.exists(os.path.dirname(fn)):
            os.makedirs(os.path.dirname(fn))
        d = cls.get_handler_config_vars(handlers)
        s = json.dumps(d, indent=2)
        with open(fn, 'w') as f:
            f.write(s)
    @classmethod
    def get_handler_config_vars(cls, handlers):
        d = {'Global':{}}
        for attr in cls.handler_config_attrs:
            d['Global'] = getattr(cls, attr)
        for h in handlers:
            d[h.__class__.__name__] = h._get_handler_config_vars()
        return d

    def update_from_handler_config(self, conf=None):
        if conf is None:
            conf = self.read_handler_config()
            if conf is None:
                return
        parsed = set()
        clsname = self.__class__.__name__
        for key, val in conf.get(clsname, {}).items():
            parsed.add(key)
            setattr(self, key, val)
        for key, val in conf.get('Global', {}).items():
            if key in parsed:
                continue
            setattr(self, key, val)
    def _get_handler_config_vars(self):
        d = {}
        for attr in self.handler_config_attrs:
            val = getattr(self, attr)
            if val == getattr(ConfigHandler, attr):
                continue
            d[attr] = val
        return d

    @property
    def full_conf_filename(self):
        fn = os.path.join(self.conf_root, self.conf_filename)
        fn = os.path.expanduser(fn)
        return fn
    def _save_identity(self, identity):
        self._handle_identity_save(identity)
    def _change_identity(self, identity):
        self.handle_paths()
        self._handle_identity_change(identity)
        self.handle_perms()
    def handle_paths(self):
        fn = self.full_conf_filename
        bak_fn = '.'.join([fn, 'bak'])
        if os.path.exists(fn) and not os.path.exists(bak_fn):
            shutil.copy2(fn, bak_fn)
        if os.path.dirname(self.conf_filename) != '~':
            dirname = os.path.dirname(fn)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
                os.chmod(dirname, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    def load_config(self):
        fn = self.full_conf_filename
        p = configparser.SafeConfigParser()
        if os.path.exists(fn):
            p.read(fn)
        if self.section_name.lower() != 'default':
            if not p.has_section(self.section_name):
                p.add_section(self.section_name)
        return p
    def iter_conf_vals(self, identity=None):
        val = None
        for ident_key, option_name in self.attr_map.items():
            if identity is not None:
                val = getattr(identity, ident_key)
            yield option_name, ident_key, val
    def _handle_identity_save(self, identity):
        p = self.load_config()
        for option_name, ident_key, val in self.iter_conf_vals(identity):
            if val is not None:
                continue
            if self.section_name.lower() == 'default':
                val = p.defaults().get(option_name)
            else:
                try:
                    val = p.get(self.section_name, option_name)
                except configparser.NoOptionError:
                    val = None
            if not val:
                continue
            setattr(identity, ident_key, val)
    def _handle_identity_change(self, identity):
        p = self.load_config()
        fn = self.full_conf_filename
        for option_name, ident_key, val in self.iter_conf_vals(identity):
            if self.section_name.lower() == 'default':
                p.defaults()[option_name] = val
            else:
                p.set(self.section_name, option_name, val)
        with open(fn, 'w') as f:
            p.write(f)
    def handle_perms(self):
        fn = self.full_conf_filename
        os.chmod(fn, stat.S_IRUSR | stat.S_IWUSR)

class BotoConfigHandler(ConfigHandler):
    conf_filename = '.boto'
    section_name = 'Credentials'

class S3CmdConfigHandler(ConfigHandler):
    conf_filename = '.s3cfg'
    attr_map = {
        'access_key_id':'access_key',
        'secret_access_key':'secret_key',
    }

class AwsConfigHandler(ConfigHandler):
    conf_filename = '.aws/credentials'
