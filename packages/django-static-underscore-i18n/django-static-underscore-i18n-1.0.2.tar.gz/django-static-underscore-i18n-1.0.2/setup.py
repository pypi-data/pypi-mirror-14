from setuptools import setup, find_packages

setup(
    name="django-static-underscore-i18n",
    version="1.0.2",
    author="Dmytro Voloshyn",
    author_email="dmytro@preply.com",
    url="http://django-static-underscore-i18n.readthedocs.org/",
  	download_url = 'https://github.com/cubicova17/django-static-underscore-i18n/tarball/1.9',
    description="A Django app that provides helper for generating "
                "Javascript Underscore templates to static files with i18n support.",
    long_description=open('README.rst').read(),
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Django>=1.4",
        "django-appconf>=0.4",
    ],
    license="BSD",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)
