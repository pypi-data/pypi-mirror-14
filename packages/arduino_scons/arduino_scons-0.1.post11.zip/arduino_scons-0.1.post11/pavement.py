import sys
import platform

from paver.easy import task, needs
from paver.setuputils import setup

sys.path.insert(0, '.')
import version


install_requires = ['path_helpers', 'arduino_helpers>=0.3.post13']

if platform.system() == 'Windows':
    install_requires += ['pywin32']

setup(name='arduino_scons',
      version=version.getVersion(),
      description='SCons tools for building Arduino projects.',
      author='Christian Fobel',
      author_email='christian@fobel.net',
      url='http://github.com/wheeler-microfluidics/arduino_scons.git',
      license='GPLv2',
      install_requires=install_requires,
      # Install data listed in `MANIFEST.in`
      include_package_data=True,
      packages=['arduino_scons', 'arduino_scons.site_tools',
                'arduino_scons.site_tools.disttar'])


@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass
