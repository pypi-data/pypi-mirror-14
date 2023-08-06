from distutils.core import setup

PACKAGE = "da_tracker"
NAME = "da_tracker"
DESCRIPTION = "Django Analytics Tracker"
AUTHOR = "Itai Shirav"
AUTHOR_EMAIL = "itai@platonix.com"
URL = "http://www.djangoanalytics.com/"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="LGPLv3",
    url=URL,
    packages=['da_tracker'],
    install_requires =['requests>=1.0'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
)

