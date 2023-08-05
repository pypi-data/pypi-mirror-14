import sys
from setuptools import setup

py_ver = sys.version_info

CMD_REQ = 'cmd2'
DEP_LINKS = []
if py_ver.major >= 3:
    if py_ver.major > 3 or py_ver.minor >= 5:
        CMD_REQ = 'cmd2>0.6.8'
        DEP_LINKS = ['git+https://github.com/python-cmd2/cmd2.git@0df289c#egg=cmd2-0.6.9a0']

setup(
    name = "aws-identity-manager",
    version = "0.0.3",
    author = "Matthew Reid",
    author_email = "matt@nomadic-recording.com",
    description = "Manage credentials for multiple AWS accounts",
    url='https://github.com/nocarryr/AWS-Identity-Manager',
    license='MIT',
    keywords = "aws",
    packages=['awsident'],
    include_package_data=True,
    entry_points={
        'console_scripts':[
            'awsidentity = awsident.main:run',
        ],
    },
    install_requires=[CMD_REQ],
    dependency_links=DEP_LINKS,
    setup_requires=['setuptools-markdown'],
    tests_require=['pexpect'],
    long_description_markdown_filename='README.md',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
