import sys

from setuptools import setup


needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []


setup(
    name='datesuninfo',
    version='0.1.0',
    packages=['datesuninfo'],
    url='https://github.com/okzach/datesuninfo/',
    license='MIT',
    author='Zach Adams',
    author_email='zach@okzach.com',
    description='Mimics PHPs date_sun_info() using pyephem.',
    entry_points={
        'console_scripts': [
            'datesuninfo=datesuninfo:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ],
    install_requires=[
        'ephem>=3.7.6.0',
        'pytz>=2016.3'
    ],
    setup_requires=[]+pytest_runner,
    tests_require=['pytest']
)
