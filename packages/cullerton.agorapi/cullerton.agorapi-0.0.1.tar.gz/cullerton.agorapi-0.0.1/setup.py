from setuptools import setup

packages = [
    'cullerton.agorapi',
]

requires = [
    'cullerton.agora',
    'pyramid',
]

setup(
    name='cullerton.agorapi',
    version="0.0.1",
    packages=packages,
    namespace_packages=['cullerton'],
    install_requires=requires,
    author='mike cullerton',
    author_email='michaelc@cullerton.com',
    description='A simple api for cullerton.agora',
    url='https://github.com/cullerton/cullerton.agorapi',
    download_url='https://github.com/cullerton/cullerton.agorapi/tarball/0.0.1',
    keywords=['academic', 'simple', 'example'],
    classifiers=[],
    entry_points="""\
    [paste.app_factory]
    main = cullerton.agorapi:main
    """,
    package_data={
        '': ['*.txt', '*.rst', '*.ipynb'],
    },
)
