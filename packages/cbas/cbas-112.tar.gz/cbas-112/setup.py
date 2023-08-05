#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'cbas',
        version = '112',
        description = '''Command line interface to the c-bastion''',
        long_description = '''''',
        author = "Sebastian Spoerer, Valentin Haenel",
        author_email = "sebastian.spoerer@immobilienscout24.de, valentin.haenel@immobilienscout24.de",
        license = '',
        url = 'https://github.com/ImmobilienScout24/cbas',
        scripts = ['scripts/cbas'],
        packages = ['cbas'],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'click',
            'keyring',
            'requests',
            'secretstorage',
            'yamlreader'
        ],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
    )
