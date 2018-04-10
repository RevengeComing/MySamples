from setuptools import setup
from cnfmanager import __version__ as version

long_description = """
Service to manage Configurations.
"""

def requirements():
    reqs = []
    with open('requirements.txt', 'r') as f:
        for line in f:
            reqs.append(line.replace('\n', ''))
    return reqs


setup(
    name='cnfmanager',
    version=version,

    description='Configuration manager service',
    long_description=long_description,

    author='Sepehr Hamzehlouy',
    author_email='s.hamzelooy@gmail.com',
    install_requires=requirements(),
    packages=['cnfmanager'],

    scripts = [
            'bin/cnfmanager'
        ],
    package_data = {
        'cnfmanager': ['config.yaml'],
    },
    test_suite='test'
)