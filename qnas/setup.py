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
    author='Isak Wikman, Edvin Martinson, Axel Blom, Albin Edenmyr, Didrik Palmqvist, Ludvig Nordqvist',
    author_email='isakwi@student.chalmers.se, edvmar@student.chalmers.se, bloaxel@student.chalmers.se, edenmyr@student.chalmers.se, didrikp@student.chalmers.se, ludnor@student.chalmers.se',
    url='https://github.com/isakwi/Kandidatarbete/tree/main/package_test',  # Skapa en ny git för detta?!
    install_requires=['numpy, qutip'],  # list all packages that your package uses
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

    download_url="https://github.com/isakwi/Kandidatarbete/tree/main/package_test",  # This should have a zip-downloadable file
)