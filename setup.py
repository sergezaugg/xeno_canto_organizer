
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='xcorganizer',  
    version='0.0.15',
    scripts=['src/xco_download', 'src/xco_make_param'],
    author="Serge Zaugg",
    author_email="serge.zaugg@gmail.com",
    description="Python app to download and organize files from Xeno-Canto",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Serge_23/xeno_canto_organizer",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'requests', 'pandas', 'unidecode',
      ],
 )


