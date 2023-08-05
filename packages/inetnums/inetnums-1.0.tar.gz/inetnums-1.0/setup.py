from setuptools import setup


setup(
    name="inetnums",
    description="WHOIS inetnum tree builder",
    version="1.0",
    license="MIT",
    author="Vadim Markovtsev",
    author_email="gmarkhor@gmail.com",
    url="https://github.com/vmarkovtsev/plueprint",
    download_url='https://github.com/vmarkovtsev/plueprint',
    packages=["inetnums"],
    package_dir={"inetnums": "."},
    keywords=["whois", "inetnum"],
    install_requires=["pycurl>=7.19.0"],
    package_data={'': ['requirements.txt', 'LICENSE', 'README.md']},
    entry_points={
        'console_scripts': [
            'inetnums=inetnums.__main__:__run__',
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering"
    ]
)