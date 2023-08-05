from setuptools import setup, find_packages

setup(
    name="itssafe",
    version="0.1.0",
    description="A signer and unsigner that can be explained to those who would need to copy the implemenation in non-Python environments",
    author="Mirus Research",
    author_email="frank@mirusresearch.com",
    packages=find_packages(),
    url='https://bitbucket.org/mirusresearch/itssafe',
    license='MIT license, see LICENSE',
    py_modules=["itssafe"],
    # install_requires=[
    #     ],
)
