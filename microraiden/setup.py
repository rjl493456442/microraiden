#!/usr/bin/env python3

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

with open('requirements.txt') as requirements:
    reqs = requirements.read().split()
with open('requirements-dev.txt') as requirements_dev:
    reqs += requirements_dev.read().split()[2:]

import subprocess
import distutils
import os
from setuptools import Command
from microraiden.config import MICRORAIDEN_VERSION

DESCRIPTION = 'µRaiden is an off-chain, cheap, scalable and low-latency micropayment solution.'


class CompileWebUI(Command):
    description = 'use npm to compile webui code to raiden/ui/web/dist'
    user_options = [
        ('dev', 'D', 'use development preset, instead of production (default)'),
    ]

    def initialize_options(self):
        self.dev = None

    def finalize_options(self):
        pass

    def run(self):
        npm = distutils.spawn.find_executable('npm')
        if not npm:
            self.announce('NPM not found. Skipping webUI compilation', level=distutils.log.WARN)
            return
        cwd = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                'microraiden',
                'webui',
                'microraiden',
            )
        )

        npm_version = subprocess.check_output([npm, '--version'])
        # require npm 4.x.x or later
        if not int(npm_version.decode('utf-8').split('.')[0]) >= 4:
            self.announce(
                'NPM 4.x or later required. Skipping webUI compilation',
                level=distutils.log.WARN,
            )
            return

        command = [npm, 'install']
        self.announce('Running %r in %r' % (command, cwd), level=distutils.log.INFO)
        subprocess.check_call(command, cwd=cwd)

        self.announce('WebUI compiled with success!', level=distutils.log.INFO)


config = {
    'version': MICRORAIDEN_VERSION,
    'scripts': [],
    'name': 'microraiden',
    'author': 'Brainbot AG',
    'author_email': 'info@brainbot.com',
    'description': DESCRIPTION,
    'url': 'https://github.com/raiden-network/microraiden/',
    'include_package_data': True,
    'license': 'MIT',
    'keywords': 'raiden ethereum microraiden blockchain',
    'install_requires': reqs,
    'packages': find_packages(exclude=['test']),
    'package_data': {'microraiden': ['data/contracts.json',
                                     'webui/js/*',
                                     'webui/index.html',
                                     'webui/microraiden/dist/umd/microraiden.js']},
    'classifiers': [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    'cmdclass': {
        'compile_webui': CompileWebUI,
    },
}

setup(**config)
