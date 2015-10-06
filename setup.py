from setuptools import setup

setup(
    name='comet',
    version='0.1',
    py_modules=['comet'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        comet=comet:cli
    ''',
)
