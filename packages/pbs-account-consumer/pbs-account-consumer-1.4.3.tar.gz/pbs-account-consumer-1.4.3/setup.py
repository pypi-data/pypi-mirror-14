from setuptools import setup, find_packages

PYTHON2_DEPS = ("python-openid>=2.2.5", )
PYTHON3_DEPS = ("python3-openid>=3.0.6", )

setup(
    name='pbs-account-consumer',
    version='1.4.3',
    description='PBS Account Consumer',
    author='PBS Core Services Team',
    author_email='PBSi-Team-Core-Services@pbs.org',
    packages=find_packages(exclude=('test_project', 'test_app')),
    include_package_data=True,
    zip_safe=False,  # Django can't find templates inside zips
    install_requires=('Django>=1.7',),
    extras_require={
        ':python_version=="2.7"': PYTHON2_DEPS,
        ':python_version=="3.4"': PYTHON3_DEPS, # env markers don't support other comparisons yet
        ':python_version=="3.5"': PYTHON3_DEPS  # listing all supported python 3 versions here
    }
)
