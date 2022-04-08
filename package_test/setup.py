import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='qnas',  # should match the package folder
    packages=['qnas'],  # should match the package folder
    version='0.0.1',  # important for updates
    license='MIT',  # should match your chosen license
    description='Testing installation of Package',
    long_description=long_description,  # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Isak Wikman, Edvin Martinssin, Axel Blom, Albin Edenmyr, Didrik Palmqvist, Ludvig Nordqvist',
    author_email='våramail@hej.com',
    url='https://github.com/mike-huls/toolbox_public',  # Skapa en ny git för detta?!
    install_requires=['numpy'],  # list all packages that your package uses
    keywords=["pypi", "qnas", "algorithm-simulator"],  # descriptive meta-data
    classifiers=[  # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Physicians, Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    download_url="https://github.com/mike-huls/toolbox_public/archive/refs/tags/0.0.3.tar.gz",
)