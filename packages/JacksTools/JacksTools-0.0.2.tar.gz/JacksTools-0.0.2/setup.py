from setuptools import setup, find_packages

setup(
name = 'JacksTools', 
version = '0.0.2',
description = 'Collection of Tools that I commonly use',
url = 'http://github.com/Rodot-/',
author = 'John (Jack) T O\'Brien',
author_email = 'john.t.obrien@drexel.edu',
license = 'GNU',
scripts = ['JacksTools/jmeans.py', 'JacksTools/jio.py', 'JacksTools/transformations.py', 'JacksTools/jools.py'],
packages = find_packages(),
install_requires = ['numpy>=1.6.0','eventlet>=0.18.4','matplotlib>=1.5.1', 'astropy>=1.1.1'],
zip_safe = False)


