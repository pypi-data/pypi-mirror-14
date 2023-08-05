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
        name = 'sunstone-rest-client',
        version = '0.0.5',
        description = '''sunstone rest client | an opennebula client in python, using the sunstone ReST API''',
        long_description = '''sunstone rest client

an opennebula client in python, using the sunstone ReST API
instead of the XML-RPC
''',
        author = "Arne Hilmann",
        author_email = "arne.hilmann@gmail.com",
        license = 'Apache License v2.0',
        url = 'https://github.com/arnehilmann/sunstone-rest-client',
        scripts = [],
        packages = ['sunstone_rest_client'],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'bs4',
            'click',
            'requests'
        ],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
    )
