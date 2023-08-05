from setuptools import setup, find_packages

setup(
    name='PyPTS',
    version='0.2.5',
    packages=find_packages(),
    #packages=['pypts', 'pypts.tgens'],
    #package_data={'pypts': ['examples/*.py']},
    #scripts=['bin/vleafplot.py'],

    # Commented out to prevent mandatory pip installation of the following
    # dependencies that tend to fail on some systems.
    #install_requires=['numpy', 'scipy', 'matplotlib', 'h5py'],

    author='Przemyslaw Klosiewicz',
    author_email='przemek.klosiewicz@gmail.com',
    url='https://pypi.python.org/pypi/PyPTS/',
    license='BSD',
    description='Python toolbox for plant tissue simulation prototypes',
    long_description=open('README.md').read()
)

