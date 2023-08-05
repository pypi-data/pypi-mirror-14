import sys
from setuptools import setup, find_packages

if sys.version_info <= (2, 6):
    print("ERROR: config-provider requires Python Version 2.7 or above...exiting.")
    sys.exit(1)


def readme():
    with open("README.rst") as f:
        return f.read()


setup(name="config-provider",
      version="1.0.0",
      description="GBDX Config Provider",
      long_description=readme(),
      keywords=['config', 'gbdx'],
      author="Various",
      author_email="tdgplatform@digitalglobe.com",
      url="https://github.com/TDG-Platform/app-config",
      packages=find_packages(),
      platforms="Posix; MacOS X; Windows",
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "License :: Other/Proprietary License",
                   "Operating System :: OS Independent",
                   "Topic :: Internet",
                   "Programming Language :: Python :: 2.7"],
      install_requires=[
          "boto>=2.38.0"
      ],
      py_modules=['config_provider.config_provider'],
      include_package_data=True,
      entry_points={

      }
      )
