from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='windy',
    version='0.9.8.4',
    packages = find_packages(),
    entry_points={
        "console_scripts": ['windy = windy.gui.application:main'],
        'gui_scripts': ['windy = windy.gui.application:main', ]
        },
    description='windy is an application for managing Windows user/system environment variables.',
    #long_description=long_description,
    url='http://github.com/zeljko.m.gavrilovic/windy',
    author='BigNumbers',
    author_email='zeljko.m.gavrilovic@gmail.com',
    license='GPLv3',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Desktop Environment",
        "License :: Freeware",
        "Topic :: Utilities"
      ],
    keywords=["windows", "environment", "variables", "path", "developer", "java"],
    zip_safe=False
    )