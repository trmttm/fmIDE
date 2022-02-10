"""
py2app build script for MyApplication

Usage:
    python setup.py py2app
"""
import glob

from setuptools import setup

setup(
    app=["fmIDE.py"],
    setup_requires=["py2app"],
    data_files=[
        ('src/Pickles', glob.glob('src/Pickles/*')),
        ('src/PicklesCommands', glob.glob('src/PicklesCommands/*')),
        ('src/Resources', glob.glob('src/Resources/*')),
        ('', glob.glob('applet.icns')),
    ],
    options=dict(py2app=dict(
        iconfile='applet.icns',
        packages=['src.Pickles', 'src.PicklesCommands', 'src.Resources']))
)
