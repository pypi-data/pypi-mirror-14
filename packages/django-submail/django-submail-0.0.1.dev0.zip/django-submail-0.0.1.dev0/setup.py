from setuptools import setup, find_packages
import smbackend

setup(
    name='django-submail',
    version=smbackend.__version__,
    author=smbackend.__author__,
    author_email='dzhuang.scut@gmail.com',
    keywords="django, submail, backend",
    url='https://github.com/dzhuang/django-submail',
    packages=find_packages(exclude=["demo"]),
    include_package_data=True,
    license=smbackend.__licence__,
    description=smbackend.__desc__,
    long_description=open('./README.rst').read(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: %s" % smbackend.__licence__,
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    )
