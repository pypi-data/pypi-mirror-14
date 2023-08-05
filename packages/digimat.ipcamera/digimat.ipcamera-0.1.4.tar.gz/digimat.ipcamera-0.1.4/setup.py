from setuptools import setup, find_packages

setup(
    name='digimat.ipcamera',
    version='0.1.4',
    description='Digimat IP Camera',
    namespace_packages=['digimat'],
    author='Frederic Hess',
    author_email='fhess@splust.ch',
    url='http://www.digimat.ch',
    license='PSF',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'Pillow',
        'setuptools'
    ],
    dependency_links=[
        ''
    ],
    zip_safe=False)
