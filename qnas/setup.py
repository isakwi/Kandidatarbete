import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='qnas',  # should match the package folder
    version='1.0.0',  # important for updates
    license='MIT',  # should match your chosen license
    description='QnAS package',
    long_description=long_description,  # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Isak Wikman, Edvin Martinson, Axel Blom, Albin Edenmyr, Didrik Palmqvist, Ludvig Nordqvist',
    author_email='isakwi@student.chalmers.se, edvmar@student.chalmers.se, bloaxel@student.chalmers.se, edenmyr@student.chalmers.se, didrikp@student.chalmers.se, ludnor@student.chalmers.se',
    url='https://github.com/isakwi/Kandidatarbete/tree/main/qnas',  # Skapa en ny git för detta?!
    install_requires=['numpy', 'qutip', 'qiskit', 'pandas', 'regex'],  # list all packages that your package uses
    keywords=["pypi", "qnas", "algorithm-simulator", "quantum", "quantum-algorithm-simulator", "algorithm","noise","simulator"],  # descriptive meta-data
    classifiers=[  # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],

    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)