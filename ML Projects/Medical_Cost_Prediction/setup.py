'''
setup.py is used to build an application (say ML) as a package
'''

# find_packages identifies all the packages used in the application
from setuptools import find_packages, setup

# a function to get read lines in requirements.txt (file_path)
def get_requirements(file_path):
    # requirements = []
    with open(file_path) as requirements_obj:
        requirements = requirements_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if "-e ." in requirements:
            requirements.remove("-e .")

    return requirements

# Metadata of the application
setup(
    name='Medical_Cost_Prediction',
    version='0.0.1',
    author='Anirudh Nuti',
    author_email='nuti.krish4@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)