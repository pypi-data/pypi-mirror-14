# coding:utf-8

"""
Flask-Restaction
----------------

http://flask-restaction.readthedocs.org/zh/latest/
"""
from setuptools import setup
from os.path import join, dirname

with open(join(dirname(__file__), 'requires.txt'), 'r') as f:
    install_requires = f.read().split("\n")

setup(
    name="flask-restaction",
    version="0.20.1",
    description="a powerful flask ext for create restful api",
    long_description=__doc__,
    author="guyskk",
    author_email='1316792450@qq.com',
    url="https://github.com/guyskk/flask-restaction",
    license="MIT",
    packages=["flask_restaction"],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[
        'pytest',
        'mock'
    ],
    classifiers=[
        'Framework :: Flask',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
