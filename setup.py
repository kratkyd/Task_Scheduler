from setuptools import setup

setup(
    name='schedule',
    #version='0.1.0',
    py_modules=['project.script'],
    install_requires=[
        'Click',
        'pandas',
        'pytest'
    ],
    entry_points={
        'console_scripts': [
            'schedule = project.script:schedule',
        ],
    },
)