from distutils.core import setup
from setuptools.command.install import install
from setuptools import find_packages
import subprocess

class CustomInstall(install):
    def run(self):
        # custom stuff here

        command = "sudo apt-get install -y libjpeg-dev zlib1g-dev nodejs-legacy npm python-pip python-dev && sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib && sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib && sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib && sudo npm -g install pageres-cli && sudo apt-get install -y espeak && sudo npm cache clean -f && sudo npm install -g n && sudo n stable && sudo ln -sf /usr/local/n/versions/node/v5.10.0/bin/node /usr/bin/node"
        subprocess.Popen(command).wait()
        install.run(self)

setup(
        name = 'wikimon_bot',
        packages = find_packages(), # this must be the same as the name above
        version = '0.0.7',
        description = 'Wikimon is a Python script which creates an artificial intelligent digital pet that learns through mirroring.',
        author = 'FaceRecog Pte Ltd',
        author_email = 'muhd.amrullah@facerecog.asia',
        url = 'http://facerecog.github.io/wikimon/', # use the URL to the github repo
        download_url = 'https://github.com/facerecog/wikimon/tarball/master',
        keywords = ['bot', 'chat'],
        classifiers = [],
        install_requires=['pytube', 'requests', 'python-Levenshtein', 'flask', 'oauthlib', 'python-axolotl', 'yowsup2'],
        scripts=['wikimon.py'],
        cmdclass={'install': CustomInstall},
        )


