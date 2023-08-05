from setuptools import setup, find_packages

setup(
    name='digimat.cryptedwebservice',
    version='0.1.5',
    description='Digimat Generic Crypted Webservice',
    namespace_packages=['digimat'],
    author='Frederic Hess',
    author_email='fhess@splust.ch',
    url='http://www.digimat.ch',
    license='PSF',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'pycrypto',
        'setuptools'
    ],
    dependency_links=[
        ''
    ],
    zip_safe=False)
