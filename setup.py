
from os.path import join, dirname
from setuptools import setup


setup(
    name='notify_telegram',
    version='0.1',
    maintainer='Andreas Grapentin',
    maintainer_email='andreas@grapentin.org',
    url='https://github.com/oaken-source/notify_telegram',
    description='A lightweight telegram backend notification-daemon',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),

    keywords='notification-daemon telegram',
    packages=['notify_telegram'],

    entry_points={
        'console_scripts': [
            'notify_telegram = notify_telegram:main',
        ],
    },

    install_requires=[
        'pygobject',
        'python-telegram-bot',
    ],

    license='GPLv3',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
