from setuptools import setup, find_packages


setup(
    name='ocatari',
    version='0.1.0',
    author='Quentin Delfosse',
    author_email='hikisan.gouv',
    packages=find_packages(),
    # package_data={'': extra_files},
    include_package_data=True,
    # package_dir={'':'src'},
    url='tba',
    description='Object Centric Atari 2600',
    long_description=open('README.md').read(),
    install_requires=[
        "matplotlib",
        "numpy",
        "seaborn",
        "setuptools",
        "torch",
        "tqdm",
        "gymnasium[atari]",
        "opencv_python",
        "scikit_image",
        "termcolor",
        "pandas",
        "scikit-learn",
        "ipdb"
    ]
)
