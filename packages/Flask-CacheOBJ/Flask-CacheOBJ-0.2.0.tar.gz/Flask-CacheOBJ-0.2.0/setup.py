"""
Flask-CacheOBJ provides some caching decorators
"""

from setuptools import setup

setup(
    name='Flask-CacheOBJ',
    version='0.2.0',
    url='https://github.com/liwushuo/Flask-CacheOBJ',
    license='MIT',
    author='Ju Lin',
    author_email='soasme@gmail.com',
    description='Flask-CacheOBJ provides some caching decorators',
    long_description=__doc__,
    packages=['flask_cacheobj'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'python-dateutil',
        'pytz',
        'msgpack-python',
        'redis',
        'decorator',
    ],
    classifiers=[
        'Framework :: Flask',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
