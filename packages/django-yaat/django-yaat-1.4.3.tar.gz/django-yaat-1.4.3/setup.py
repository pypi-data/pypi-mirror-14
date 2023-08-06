# coding: utf-8

from setuptools import setup
from yaat import __version__

vcs_dependencies = [
    # order_with_respect_to can be a tuple in this fork
    'git+https://github.com/yuvadm/django-ordered-model@b875b891b838b26547e1b767e30badc8f4a0331e#egg=django-ordered-model'
]

setup(
    name='django-yaat',
    version=__version__,
    packages=['yaat'],
    install_requires=['Django>=1.8.4', 'django-restify-framework>=0.24', 'django-ordered-model'],
    include_package_data=True,
    dependency_links=vcs_dependencies,
    description='The django-restify-framework resource of the yaat AngularJs module',
    author='Slapec',
    url='https://github.com/slapec/django-yaat',
    license='MIT',
    zip_safe=False,
)
