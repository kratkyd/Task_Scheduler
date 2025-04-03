from setuptools import setup

setup(
    name='script',
    #version='0.1.0',
    py_modules=['script'],
    install_requires=[
        'Click',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'schedule = script:schedule',
        ],
    },
)