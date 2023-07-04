from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.readlines()


setup(
    name='ocatari',
    version='0.1.0',
    author='Quentin Delfosse',
    author_email='quentin.delfosse@cs.tu-darmstadt.de',
    packages=find_packages(),
    # package_data={'': extra_files},
    include_package_data=True,
    # package_dir={'':'src'},
    url='https://github.com/k4ntz/OC_Atari',
    description='Object Centric Atari 2600',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements
)
