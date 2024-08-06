from setuptools import setup
from setuptools.command.install import install
import subprocess

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        subprocess.check_call(['pip', 'uninstall', '-y', 'torch', 'torchaudio'])
        subprocess.check_call(['pip', 'install', 'torch==2.1.0+cpu', 'torchaudio==2.1.0+cpu', '-f', 'https://download.pytorch.org/whl/torch_stable.html'])

setup(
    name='streamstem',
    version='1.0',
    cmdclass={
        'install': PostInstallCommand,
    },
)
