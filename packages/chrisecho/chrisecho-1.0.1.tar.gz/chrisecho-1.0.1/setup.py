from setuptools import setup, find_packages

setup(
    name='chrisecho',
    version='1.0.1',
    description='Echos something to the console.',
    author='Chris Lombaard',
    author_email='chrislombaard@gmail.com',
    #url='https://www.python.org/sigs/distutils-sig/',
    packages=find_packages(),
    test_suite="test",
    install_requires = [
        'requests',
        'tox',
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
    )
