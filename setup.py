from setuptools import setup
import py2exe
import glob

setup(
    name='fmIDE',
    version='',
    packages=['src'],
    url='',
    license='',
    author='STTM',
    author_email='',
    description='',
    windows=[
        {
            'script': 'fmIDE.py',
            'icon_resources': [(1, 'applet.ico')]
        },
    ],
    data_files=[
        ('src/Pickles', glob.glob('src/Pickles/*')),
        ('src/PicklesCommands', glob.glob('src/PicklesCommands/*')),
        ('src/Resources', glob.glob('src/Resources/*')),
        ('', glob.glob('applet.ico')),
    ],
    options={
        'py2exe': {
            'bundle_files': 1,
            'compressed': True,
            'packages': ['src.Pickles', 'src.PicklesCommands', 'src.Resources', ],
        },
    },
)
