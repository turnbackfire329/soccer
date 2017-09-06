import setuptools

setuptools.setup(
    name="soccer",
    version="0.0.1",
    url="https://github.com/hhllcks/soccer",

    author="Hendrik Hilleckes",
    author_email="hhllcks@gmail.com",

    description="A soccer data framework",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
          'footballdataorg',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6'
    ],
)
