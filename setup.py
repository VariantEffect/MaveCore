import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    "fqfa>=1.2.1",
    "mavehgvs>=0.4.0",
    "idutils>=1.1.0",
    "pandas>=1.1.0",
]

setuptools.setup(
    name="mavecore",
    version="0.1.4",
    author="MaveDB Developers",
    author_email="alan.rubin@wehi.edu.au",
    description=("MaveCore implements shared functionality for MaveTools and MaveDB."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VariantEffect/MaveCore/tree/testMaveCore",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    test_suite="tests",
)
