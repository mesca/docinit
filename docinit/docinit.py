from setuptools import Command
from pathlib import Path
import os
import configparser
import shutil

from pbr.version import VersionInfo
from setuptools import find_packages

DEFAULT = {
    'doc_directory': 'doc', # relative to setup.cfg
    'template_directory': '_templates', # relative to doc_directory
    'static_directory': '_static', # relative to doc_directory
    'is_subproject': 'false',
    'project_name': '',
    'version': VersionInfo(__name__).version_string(),
    'release': VersionInfo(__name__).release_string()
}

class DocInitCommand(Command):

    description = "Initialize documentation"
    user_options = []
    boolean_options = []
    negative_opt = {}

    def __getattr__(self, name):
        return None

    def initialize_options(self):
        for key in DEFAULT.keys():
            setattr(self, key, None)

    def finalize_options(self):
        pass

    def run(self):
        init()

def init():
    config = get_config()
    src = str(Path(__file__).parent.joinpath('skeleton'))
    dst = str(find_root().joinpath(config['docinit']['doc_directory']))
    copy_tree(src, dst)
    copy_logo(src, dst)

def parse_string(s):
    s = s.strip()
    if s.lower() in ('true', 1): return True
    if s.lower() in ('false', 0): return False
    if s.lower() == 'none': return None
    for t in (int, float, str):
        try:
            s = t(s)
        except ValueError:
            continue
        else:
            break
    return s

def convert(s):
    if ',' in s:
        return [parse_string(s_.strip().replace('"','').replace('\'','')) for s_ in s.split(',')]
    else:
        return parse_string(s)

def get_config():
    path = find_root().joinpath('setup.cfg')
    config = configparser.ConfigParser()
    config.read(path)
    if 'docinit' not in config: config['docinit'] = {}
    config['DEFAULT'] = DEFAULT
    #config = {section: dict(config.items(section)) for section in config.sections()}
    return config

def find_root():
    path = Path(os.getcwd())
    while True:
        file = path.joinpath('setup.cfg')
        if file.is_file():
            return path
        if path == path.parent:
            return False
        path = path.parent

def find_dirs():
    packages = find_packages(str(find_root()))
    dirs = []
    for package in packages:
        if not '.' in package:
            dirs.append(str(Path(package).resolve()))
    return dirs

def copy_tree(src, dst):
    if os.path.isdir(src):
        if not os.path.isdir(dst):
            os.makedirs(dst)
        files = os.listdir(src)
        for file in files:
            copy_tree(os.path.join(src, file), os.path.join(dst, file))
    else:
        # Do not overwrite existing files
        if not os.path.isfile(dst):
            shutil.copyfile(src, dst)

def copy_logo(src, dst):
    pass
