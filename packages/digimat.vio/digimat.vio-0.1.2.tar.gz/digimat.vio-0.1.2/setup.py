from setuptools import setup, find_packages

setup(
    name='digimat.vio',
    version='0.1.2',
    description='Digimat Managed VIO',
    namespace_packages=['digimat'],
    author='Frederic Hess',
    author_email='fhess@splust.ch',
    url='http://www.digimat.ch',
    license='PSF',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'pytweening',
        'setuptools'
    ],
    dependency_links=[
        ''
    ],
    zip_safe=False)
