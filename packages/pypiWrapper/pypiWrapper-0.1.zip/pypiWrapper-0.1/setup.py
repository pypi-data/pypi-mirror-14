from distutils.core import setup

with open('requirements.txt') as file:
    required = file.read().splitlines()

setup(
    name='pypiWrapper',
    version='0.1',
    packages=['pypiWrapper'],
    license='MIT',
    author='Niek Keijzer',
    author_email='info@niekkeijzer.com',
    description='Wrapper for PyPI API',
    url='https://github.com/NiekKeijzer/pypiWrapper',
    download_url='https://github.com/NiekKeijzer/pypiWrapper/tarball/0.1',
    keywords="pypi json api wrapper",
    install_required=required
)
