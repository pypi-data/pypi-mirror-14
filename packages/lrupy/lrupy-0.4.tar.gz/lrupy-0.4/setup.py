from distutils.core import setup

setup(
    name="lrupy",
    packages=['lrupy'],
    version="0.4",
    py_modules=['lrupy.lrupy'],
    description="A simple in-memory (LRU) cache implementation",
    author="Abhinav Upadhyay",
    author_email="er.+abhinav.+updadhyay@gmail.com",
    url="https://github.com/abhinav-upadhyay/lrupy",
    download_url="https://github.com/abhinav-upadhyay/lrupy/archive/0.4.tar.gz",
    keywords=['development', 'cache', 'performance'],
    license='BSD',
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
    long_description=open('README.md').read())

