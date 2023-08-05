from setuptools import setup, find_packages

packages = [
    'cullerton.agora',
]

requires = [
    'sqlalchemy',
]

setup(
    name='cullerton.agora',
    version="0.0.2",
    packages=find_packages(),
    namespace_packages=['cullerton'],
    install_requires=requires,
    author='mike cullerton',
    author_email='michaelc@cullerton.com',
    description='A forum for ideas',
    url='https://github.com/cullerton/cullerton.agora',
    download_url='https://github.com/cullerton/cullerton.agora/tarball/0.0.2',
    keywords=['academic', 'simple', 'example'],
    classifiers=[],
    entry_points="""\
    [console_scripts]
    initialize_agora_db = cullerton.agora.initialize_db:main
    """,
    package_data={
        '': ['*.txt', '*.rst', '*.ipynb'],
    },
)
