from setuptools import setup, find_packages

setup(
    name='digimat.sankey',
    version='0.1.3',
    description='Digimat Sankey Diagrams',
    namespace_packages=['digimat'],
    author='Frederic Hess',
    author_email='fhess@splust.ch',
    url='http://www.digimat.ch',
    license='PSF',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'digimat.db',
        'py_expression_eval',
        'pillow',
        'matplotlib',
        'numpy',
        'pandas',
        'setuptools'
    ],
    dependency_links=[
        ''
    ],
    zip_safe=False)
