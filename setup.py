from setuptools import setup, find_packages


__version__ = '1.1.3'


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='ocatari',
    version=__version__,
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
    install_requires=[
        "gymnasium",
        "matplotlib",
        "numpy",
        "opencv_python",
        "scikit_image",
        "termcolor",
        "seaborn",
        "pandas",
        "scikit-learn",
        "keyboard",
        "tqdm",
        "pygame",
        "pyfiglet",
    ]
)

print("Please install gymnasium atari dependencies, using:\n", 
      "pip install gymnasium[atari, accept-rom-license]")
