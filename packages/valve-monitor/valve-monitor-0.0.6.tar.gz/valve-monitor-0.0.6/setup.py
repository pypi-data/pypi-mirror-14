from setuptools import setup

setup(
    name='valve-monitor',
    version='0.0.6',
    author='Konstantin Kruglov',
    author_email='kruglovk@gmail.com',
    description='Getting A2x information',
    # long_description=a2x.__long_description__,
    keywords=('valve', 'a2s'),
    url='https://github.com/k0st1an/valve-monitor',
    install_requires=('a2x',),
    license='Apache License Version 2.0',
    scripts=['valve-monitor.py'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
