from setuptools import setup, find_packages

setup(
    name='digimat.ip01',
    version='0.1.12',
    description='Digimat IP01',
    namespace_packages=['digimat'],
    author='Frederic Hess',
    author_email='fhess@splust.ch',
    url='http://www.digimat.ch',
    license='PSF',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'pytz',
        'suds',
        'requests[security]',
        'setuptools'
    ],
    dependency_links=[
        ''
    ],
    zip_safe=False)
