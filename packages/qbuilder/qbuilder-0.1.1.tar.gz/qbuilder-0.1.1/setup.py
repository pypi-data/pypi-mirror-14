from distutils.core import setup
setup(
    name='qbuilder',
    packages=['qbuilder'],
    version='0.1.1',
    include_package_data=False,
    description=(
        'A library to build human '
        'readable SQL query string using a pythonic API'),
    long_description=open("README.md").read(),
    author='Brijesh Bittu',
    author_email='brijeshb42@gmail.com',
    url='https://github.com/brijeshb42/qbuilder',
    download_url='https://github.com/brijeshb42/qbuilder/tarball/0.1.0',
    keywords=['SQL', 'peewee', 'querybuilder'],
    license="http://www.opensource.org/licenses/mit-license.php",
    classifiers=[],
)
