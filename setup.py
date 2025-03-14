'''
Te setup.py file is an essential part of packaging and distributig python projects.
It is used by setuptoools (or dstutils in older pytho versions) to define th configuration
of tyour project, such as metadata, dependecies and more. 
'''

from setuptools import find_packages,setup
from typing import List

requirements :List[str] = []
def get_requirements()-> List[str]:
    "this function will return list of requirements"
    try: 
        with open('requirements.txt', 'r') as file:
            #read lines 
            lines = file.readlines()
            #process each line
            for line in lines :
                requirement= line.strip()
                #ignore comments
                if requirement.startswith('#'):
                    continue
                #ignore empty lines and -e .
                if requirement == '' or requirement =='-e .':
                    continue
                else:
                    requirements.append(requirement)

            


    except FileNotFoundError:
        raise FileNotFoundError('requirements.txt file not found')
     
    return requirements

print(get_requirements())


setup(
    name='CyberSecurity-Tools',
    version='0.1',
    author="Nitin-Mehta",
    author_email="nitin@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()

)