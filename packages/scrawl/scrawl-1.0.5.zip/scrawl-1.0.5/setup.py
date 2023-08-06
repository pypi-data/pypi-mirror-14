from setuptools import setup, find_packages
setup(
    name='scrawl',
    version='1.0.5',
    description='A python note-taking console app ',
    long_description="",
    url='https://github.com/ten-c/bc-6-scrawl',
    author='Ten Chege',
    author_email='10.chege@gmail.com',
    keywords='sample setuptools development',
    # py_modules=['scrawl','scrawl2'],
    packages=find_packages(),
    package_data={
        'scrawl': ['data.db'],
    },
    include_package_data = True,
    install_requires=[
        'Click',
        'python-firebase',
        'colorama',
        # 'sqlite'
    ],
    entry_points='''
        [console_scripts]
        scrawl=scrawl.cli:scrawl
        scrawl2=scrawl.cli:scrawl2
    ''',
)

# packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
# package_data={
#     'sample': ['package_data.dat'],
# },
# data_files=[('my_data', ['data/data_file'])],