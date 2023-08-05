from distutils.core import setup

setup(
    name="Packilog",
    version="0.0.2",
    author="Kenneth Wilke",
    author_email="kenneth.wilke@rackspace.com",
    packages=['libpackilog'],
    scripts=['bin/packilog'],
    url='https://github.com/KennethWilke/Packilog',
    license='LICENSE.txt',
    description="A package manager for SystemVerilog.",
    long_description=open('README.txt').read(),
    install_requires=[
        "requests >= 2.9.1"
    ],
)
