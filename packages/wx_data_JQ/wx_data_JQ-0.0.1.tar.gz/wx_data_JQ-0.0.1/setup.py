#top 2 lines ... This boilerplate installs setuptools when the user (who is running setup.py)
# hasn't installed setuptools:
from ez_setup import use_setuptools 
use_setuptools()
from setuptools import setup, find_packages
setup(
    name = "wx_data_JQ",
    version = "0.0.1",
    install_requires = ['python3.4.3'],
#packages = find_packages() .. does all the trick... The exclude argument keeps it from 
#auto-detecting things that look like packages. otherwise, need to list all the packages 
#that should be installed, including subpackages, like ['packagename', ...].
    packages = find_packages(),
    srcipts = ['wx_data.py'],
    dependency_links= ["www.SomeLinks.com" ],
         
    # meatadata for upload to PyPi
    author = "JQ",
    author_email = "contact@SomeEmail.com",
    discription = "Program reads the data and process accordingly",
    licence = "ABC", # dummy value
    keywords = "may need to add some keywords at later stage",
    url = "www.MayNeedToAddLater.com",  
    # we can define entry points, keywords, classifiers etc if needed late on  
    #entry_points={
    #    'console_scripts': [
    #        'foo = my_package.some_module:main_func',
    #        'bar = other_module:some_func',
    #    ],}

    #classifiers=[
    #         # maturity of the project 3 - alpha, 4 - beta, 5 - production/stable
    #         'Development status :: 3 - Alpha',
    #         'intended audience :: developers in this project',
    #         'topic :: software to read weather data',
    #         'licence :: ABC Licence', # should be same as above
    #         'programming language :: Python :: 3.4.3',
    #         ],    
 
    )