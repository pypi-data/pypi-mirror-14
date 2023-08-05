from setuptools import setup, find_packages

setup(
    name='telestream-cloud',
    version='1.1.0',
    description='A Python implementation of Telestream Cloud REST interface',
    author='Telestream Cloud',
    author_email='cloudsupport@telestream.net',
    url='https://cloud.telestream.net',
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords='telestream cloud rest video encoding stream service',
    license='MIT',
    install_requires=[
        'requests',
    ],
)
