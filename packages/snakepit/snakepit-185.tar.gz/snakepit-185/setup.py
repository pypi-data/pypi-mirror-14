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
        name = 'snakepit',
        version = '185',
        description = '''Package Python software as an RPM including all dependencies (even the interpreter).''',
        long_description = '''''',
        author = "Valentin Haenel",
        author_email = "valentin@haenel.co",
        license = 'Apache',
        url = 'https://github.com/ImmobilienScout24/snakepit',
        scripts = ['scripts/snakepit'],
        packages = ['snakepit'],
        py_modules = [],
        classifiers = [
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Operating System :: POSIX :: Linux',
            'Topic :: System :: Software Distribution',
            'Topic :: System :: Systems Administration',
            'Topic :: System :: Archiving :: Packaging',
            'Topic :: Utilities'
        ],
        entry_points = {},
        data_files = [],
        package_data = {
            'snakepit': ['templates/TEMPLATE-PyRun.spec', 'templates/TEMPLATE-miniconda.spec']
        },
        install_requires = [
            'docopt',
            'jinja2',
            'pyyaml',
            'requests'
        ],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
    )
