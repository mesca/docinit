import os
import subprocess
from datetime import datetime
from configparser import ConfigParser
from urllib.request import urlopen
from shutil import copyfile, copyfileobj
from pathlib import Path
from setuptools import Command, find_packages
from setuptools.config import ConfigHandler, ConfigOptionsHandler
from pbr.version import VersionInfo


class DocInitCommand(Command):

    description = 'Initialize documentation'
    user_options = []
    boolean_options = []
    negative_opt = {}

    def __getattr__(self, name):
        pass

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        init_doc()


class Parse():

    @classmethod
    def option(cls, value):
        value = value.strip(' \r')
        if value.startswith('file:'):
            return ConfigHandler._parse_file(value)
        if value.startswith('attr:'):
            return ConfigOptionsHandler._parse_attr(value)
        if value in ['find:', 'find_namespace:']:
            return _get_packages()
        if '=' in value:
            return cls._parse_dict(ConfigHandler._parse_dict(value))
        if ',' in value or '\n' in value:
            return cls._parse_list(ConfigHandler._parse_list(value))
        return cls._parse_value(value)

    @classmethod
    def _parse_list(cls, l):
        return [cls._parse_value(v) for v in l]

    @classmethod
    def _parse_dict(cls, d):
        return {k: cls._parse_value(v) for k, v in d.items()}

    @staticmethod
    def _parse_value(v):
        if v.lower() in ('true', '1', 'yes'): return True
        if v.lower() in ('false', '0', 'no'): return False
        if v.lower() == 'none': return None
        for t in (int, float, str):
            try:
                v = t(v)
            except ValueError:
                continue
            else:
                break
        return v


class Config():

    options = [ 'doc_dir', 'name', 'parent_url', 'logo_url', 'favicon_url', 'version', 'release', 'packages', 'author', 'copyright']

    def __init__(self, path):
        self.config = {
            'metadata': {},
            'options': {},
            'docinit': {},
            'build_sphinx': {},
            'git': Git().info
        }
        parser = ConfigParser()
        parser.read(path)
        for section in parser.sections():
            self.config[section] = {k: Parse.option(v) for (k, v) in parser.items(section)}
        for option in self.options:
            if option not in self.config['docinit']:
                try:
                    getattr(self, '_set_' + option)()
                except AttributeError:
                    self.config['docinit'][option] = None

    def _set_doc_dir(self):
        self.config['docinit']['doc_dir'] = self._find([
            ('build_sphinx', 'source-dir')
        ], 'doc')

    def _set_name(self):
        self.config['docinit']['name'] = self._find([
            ('build_sphinx', 'project'),
            ('metadata', 'name'),
            ('git', 'name')
        ], 'Project')

    def _set_version(self):
        self.config['docinit']['version'] = self._find([
            ('build_sphinx', 'version'),
            ('metadata', 'version')
        ], VersionInfo(__name__).version_string())

    def _set_release(self):
        self.config['docinit']['release'] = self._find([
            ('build_sphinx', 'release')
        ], VersionInfo(__name__).release_string())

    def _set_author(self):
        self.config['docinit']['author'] = self._find([
            ('metadata', 'author'),
            ('git', 'author')
        ], 'Anonymous')

    def _set_copyright(self):
        begin_year = self.config['git']['year']
        current_year = str(datetime.now().year)
        author = self.config['docinit']['author']
        if (begin_year is None) or (begin_year == current_year):
            copyright = f'{current_year}, {author}'
        else:
            copyright = f'{begin_year}-{current_year}, {author}'
        self.config['docinit']['copyright'] = self._find([
            ('build_sphinx', 'copyright')
        ], copyright)

    def _set_packages(self):
        self.config['docinit']['packages'] = self._find([
            ('options', 'packages')
        ], _get_packages())

    def _find(self, lookups, default=None):
        for lookup in lookups:
            value = self.config
            for key in lookup:
                try:
                    value = value[key]
                except KeyError:
                    value = None
            if value:
                return value
        return default


class Git():

    def __init__(self):
        self.info = {
            'year': None,
            'name': None,
            'author': None,
            'email': None
        }
        try:
            commit = self._run("git rev-list --max-parents=0 HEAD")
            info = self._run(f"git show -s --format=%ci|%cn|%ce {commit}").split('|')
            self.info['year'] = info[0][0:4]
            self.info['author'] = info[1]
            self.info['email'] = info[2]
            url = self._run("git config --get remote.origin.url")
            self.info['name'] = os.path.basename(url)[0:-4]
        except:
            pass

    def _run(self, command):
        p = subprocess.run(command.split(), capture_output=True)
        return p.stdout.decode().strip()


def init_doc():
    config = get_config()
    src = str(Path(__file__).parent.joinpath('skeleton'))
    dst = str(_find_root().joinpath(config['docinit']['doc_dir']))
    _copy_tree(src, dst)
    _download_file(config['docinit']['logo_url'], Path(dst).joinpath('_static/logo.png'))
    _download_file(config['docinit']['favicon_url'], Path(dst).joinpath('_static/favicon.ico'))

def get_config():
    path = _find_root().joinpath('setup.cfg')
    config = Config(path)
    return  config.config

def set_vars(scope, config=None):
    if not config:
        config = get_config()
    reserved = Config.options
    for key, value in config['docinit'].items():
        if key not in reserved:
            scope[key] = value

def _find_root():
    path = Path(os.getcwd())
    while True:
        file = path.joinpath('setup.cfg')
        if file.is_file():
            return path
        if path == path.parent:
            return False
        path = path.parent

def _get_packages():
    root = _find_root()
    packages = find_packages(str(root))
    dirs = []
    for package in packages:
        if not '.' in package:
            dirs.append(str(root.joinpath(package)))
    return dirs

def _copy_tree(src, dst):
    if os.path.isdir(src):
        if not os.path.isdir(dst):
            os.makedirs(dst)
        files = os.listdir(src)
        for file in files:
            _copy_tree(os.path.join(src, file), os.path.join(dst, file))
    else:
        # Do not overwrite existing files
        if not os.path.isfile(dst):
            copyfile(src, dst)

def _download_file(url, dst):
    if url is None:
        return
    with urlopen(url) as response:
        with open(dst, 'wb') as file:
            copyfileobj(response, file)

