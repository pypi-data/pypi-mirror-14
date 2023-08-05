from setuptools import setup, find_packages
setup(
    name = "gi-eagle",
    version = "0.8",
    author = "Christopher Schröder, Christoph Stahl, Felix Mölder, Andre Janowicz, Jasmin Beygo, Marcel Martin and Sven Rahmann",
    author_email = "christopher.schroeder@tu-dortmund.de",
    long_description=__doc__,
    license = "MIT",
    url = "https://bitbucket.org/christopherschroeder/eagle",
    packages=find_packages(),
    py_modules = ["run"],
    package_data={
        'static': 'eagle/static/*',
        'templates': 'eagle/templates/*'},
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'numpy', 'scipy', 'h5py'],
    entry_points = {"console_scripts": [
                        "eagle = run:main"
                    ]},
    classifiers = [
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Framework :: Flask",
        "Environment :: Web Environment",
        "Intended Audience :: Science/Research"]
)
