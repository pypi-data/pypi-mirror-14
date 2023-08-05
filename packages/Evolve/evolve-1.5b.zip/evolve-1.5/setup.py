from distutils.core import setup

setup(
    name='evolve',
    version='1.5',
    packages=['morphs'],
    #package_data={'evolve': ['web/css/*.css'],},
    #data_files=[('web',['web/css/*.css'])],
    url='https://github.com/JamesHabben/evolve',
    license='',
    author='James Habben',
    author_email='james@habben.net',
    description='Web interface for the Volatility Memory Forensics Framework',
    install_requires=[
        'bottle',
        'maxminddb',
    ]
)
