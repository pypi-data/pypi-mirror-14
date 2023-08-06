from setuptools import setup


setup(
    name="obj2uni",
    description="Object -> unicode mapper",
    version="1.0",
    license="MIT",
    author="Vadim Markovtsev",
    author_email="gmarkhor@gmail.com",
    url="https://github.com/vmarkovtsev/obj2uni",
    download_url='https://github.com/vmarkovtsev/obj2uni',
    packages=["obj2uni"],
    package_dir={"obj2uni": "."},
    keywords=["unicode"],
    package_data={'': ['LICENSE', 'README.md']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries"
    ]
)