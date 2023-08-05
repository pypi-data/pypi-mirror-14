from setuptools import setup

__VERSION__ = '0.2'

setup(
    name='ndl',
    packages=['ndl'],
    py_modules=['ndl'],
    description='Easy file searching from the command-line',
    author='Sully Sullenberger',
    author_email='sully@sadburger.com',
    url='https://github.com/msull/needle',
    download_url='https://github.com/msull/needle/tarball/%s' % __VERSION__,
    keywords=['search', 'files', 'terminal'],
    classifiers=[],
    version=__VERSION__,
    install_requires=[
        'Click',
    ],
    entry_points="""
        [console_scripts]
        ndl=ndl.cli:cli
    """,
)
