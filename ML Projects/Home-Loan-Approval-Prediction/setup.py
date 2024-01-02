import setuptools

with open('README.md','r',encoding='utf-8') as f:
    long_description = f.read()

__version__ = '0.0.1'

REPO_NAME = 'homeLoan'
AUTHOR_NAME = 'Utpal Paul'
AUTHOR_USER_NAME = 'utpal108'
SRC_REPO = 'Home-Loan-Approval-Prediction'
AUTHOR_EMAIL = 'utpalpaul108@gmail.com'


setuptools.setup(

    name=REPO_NAME,
    version=__version__,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description='Home Loan Approval Prediction',
    long_description=long_description,
    long_description_content="text/markdown",
    url=f'https://github.com/{AUTHOR_USER_NAME}/{SRC_REPO}',
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{SRC_REPO}/issues",
    },
    package_dir={'':'src'},
    packages=setuptools.find_packages(where='src')

)