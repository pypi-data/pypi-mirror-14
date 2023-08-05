from setuptools import setup, find_packages

setup(
    name='digimat.nestcam',
    version='0.1.8',
    description='Digimat Nestcam',
    namespace_packages=['digimat'],
    author='Frederic Hess',
    author_email='fhess@splust.ch',
    url='http://www.digimat.ch',
    license='PSF',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'pillow',
        'requests[security]',
        'urllib3[secure]',
        'setuptools'
    ],
    dependency_links=[
        ''
    ],
    zip_safe=False)
