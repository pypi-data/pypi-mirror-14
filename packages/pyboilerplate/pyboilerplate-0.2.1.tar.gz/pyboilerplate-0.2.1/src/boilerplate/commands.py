import os
import hashlib
import codecs
import configparser
from contextlib import contextmanager
from collections import OrderedDict
import jinja2
from boilerplate.inputs import *


__all__ = ['make_new']
datadir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
pkg_loader = jinja2.PackageLoader('boilerplate', 'templates')
jinja_env = jinja2.Environment(loader=pkg_loader)
license_alias = {
    'gpl': 'gpl3',
}


def write_template(template: str, namespace=None, ignore=False, path=None,
                   verbose=True, hash=None):
    """Render jinja template with the given namespace and saves it in the
    desired path"""

    if path is None:
        path = template

    template = jinja_env.get_template(template)
    data = template.render(**(namespace or {}))

    if os.path.exists(path) and ignore:
        return
    elif os.path.exists(path):
        with open(path) as F:
            filedata = F.read()
            if filedata == data:
                return

        # If hash is compatible with given hash, we simply overwrite
        ask = True
        if hash:
            filehash = hashlib.md5(filedata.encode('utf8')).digest()
            filehash = codecs.encode(filehash, 'base64').decode()
            if hash == filehash:
                os.rename(path, path + '.bak')
                ask = False

        if ask:
            msg = 'File %r exists. Save backup and overwrite?' % path
            response = yn_input(msg)
            if response == 'yes':
                os.rename(path, path + '.bak')
            else:
                return

    if verbose:
        print('    creating %s...' % os.path.abspath(path))

    with open(path, 'w') as F:
        F.write(data)

    return data


@contextmanager
def visit_dir(dir):
    """Visit directory and come back after the with block is finish."""

    currdir = os.getcwd()
    os.chdir(dir)
    yield
    os.chdir(currdir)


def make_new(**kwds):
    """Create a new project.

    Parameters
    ----------

    project : str
        Project's name
    """

    factory = ProjectFactory(**kwds)
    factory.make()


# noinspection PyAttributeOutsideInit
class ProjectFactory:
    """A new project job.

    Interacts with the user and keeps a common namespace for all sub-routines
    """
    _valid_attrs = ['project', 'author', 'email', 'version', 'license']

    def __init__(self, **kwds):
        self.basepath = os.getcwd()
        self.basepath_len = len(self.basepath)

        # Config parser
        self.config = configparser.ConfigParser()
        self.config.optionxform = str

        if os.path.exists('boilerplate.ini'):
            with open('boilerplate.ini') as F:
                self.config.read_file(F)

        if 'options' not in self.config:
            self.config.add_section('options')
        if 'file hashes' not in self.config:
            self.config.add_section('file hashes')

        # Save values and use the default config
        for attr in self._valid_attrs:
            try:
                setattr(self, attr, kwds.pop(attr))
                continue
            except KeyError:
                pass

            try:
                value = self.config.get('options', attr)
                setattr(self, attr, value)
            except configparser.NoOptionError:
                setattr(self, attr, None)

        if kwds:
            raise TypeError('invalid attribute: %s' % kwds.popitem()[0])

    def make(self):

        # Asks basic info
        self.project = self.project or input("Project's name: ")
        self.author = self.author or input("Author's name: ")
        self.email = self.email or input("Author's email: ")

        # Fetch version from existing VERSION file or asks the user
        if self.version is None and os.path.exists('VERSION'):
            self.version = open('VERSION').read().strip()
        self.version = self.version or default_input("Version: ", '0.1.0')

        # Ask other input
        self.license = self.license or default_input('License: ', 'gpl')

        # Make each part of the source tree
        self.make_base(ignore=False)
        self.make_setup_py(ignore=False)
        self.make_package(ignore=False)
        self.make_docs(ignore=False)
        self.make_license(ignore=False)

        # Save config file
        basic = self.config['options']
        basic['project'] = self.project
        basic['author'] = self.author
        basic['email'] = self.email
        basic['version'] = self.version
        basic['license'] = self.license

        with open('boilerplate.ini', 'w') as F:
            self.config.write(F)

    def write_template(self, template, ignore=False, path=None, base=None):
        base = os.getcwd()
        file = os.path.join(base, path or template)
        file = file[self.basepath_len + 1:]
        data = write_template(template, vars(self), ignore=ignore, path=path)
        if data is not None:
            filehash = hashlib.md5(data.encode('utf8')).digest()
            filehash = codecs.encode(filehash, 'base64').decode()
            self.config.set('file hashes', file, filehash)

    def make_base(self, ignore=True):
        self.write_template('VERSION.txt', ignore=True, path='VERSION')
        self.write_template('gitignore.txt', ignore=ignore, path='.gitignore')

    def make_setup_py(self, ignore=True):
        self.write_template('setup.py', ignore=ignore)
        self.write_template('MANIFEST.in', ignore=ignore)
        self.write_template('requirements.txt', ignore=ignore)
        self.write_template('requirements-dev.txt', ignore=ignore)

    def make_package(self, ignore=True):
        curdir = os.getcwd()
        try:
            # Make src/project directory
            for directory in ['src', self.project]:
                if not os.path.exists(directory):
                    os.mkdir(directory)
                os.chdir(directory)

            self.write_template('init.py', ignore=True, path='__init__.py')
            self.write_template('__main__.py', ignore=ignore)
            self.write_template('__meta__.py', ignore=True)

            # Make test folder
            if not os.path.exists('test'):
                os.mkdir('test')
            os.chdir('test')

            if not os.path.exists('__init__.py'):
                with open('__init__.py', 'w') as F:
                    F.write('\n')
            self.write_template('test_project.py', ignore=ignore,
                           path='test_%s.py' % self.project)

        finally:
            os.chdir(curdir)

    def make_readme(self, ignore=True):
        self.write_template('README.rst', ignore=True)
        self.write_template('INSTALL.rst', ignore=ignore)

    def make_docs(self, ignore=True):
        self.make_readme(ignore=True)

        # Make src/project directory
        if not os.path.exists('docs'):
            os.mkdir('docs')
        with visit_dir('docs'):
            self.write_template('conf.py', ignore=ignore)
            self.write_template('index.rst', ignore=ignore)
            self.write_template('install.rst', ignore=ignore)
            self.write_template('license.rst', ignore=ignore)
            self.write_template('apidoc.rst', ignore=ignore)
            self.write_template('warning.rst', ignore=ignore)
            self.write_template('make.bat', ignore=True)
            self.write_template('makefile.txt', ignore=True, path='Makefile')

            # Make sphinx folders
            for folder in ['_static', '_build', '_templates']:
                if not os.path.exists(folder):
                    os.mkdir(folder)

    def make_license(self, ignore=True):
        license = license_alias.get(self.license, self.license)
        license_path = 'licenses/%s.txt' % license
        self.write_template(license_path, ignore=ignore, path='LICENSE')


class attrdict(dict):
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError

    def __setattr__(self, attr, value):
        self[attr] = value

    def sub(self, keys):
        if isinstance(keys, str):
            keys = keys.split()
        return attrdict({k: self[k] for k in keys})


if __name__ == '__main__':
    dirname = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    root = os.path.dirname(dirname)
    os.chdir(os.path.join(root, 'playground'))
    print(os.listdir(os.getcwd()))

    if yn_input('clean?') == 'yes':
        os.system('rm * -Rv')

    make_new(author='Chips', email='foo@bar', project='foobar', version='0.1',
             license='gpl')