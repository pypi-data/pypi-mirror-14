from setuptools import setup

setup(name='loveallufev-crawler',
    version='0.2',
    description='The crawler module',
    url='https://github.com/loveallufev/crawler',
    author='Duc Trung NGUYEN',
    author_email='ductrungkhtn@gmail.com',
    license='MIT',
    packages=['request_core'],
    install_requires=[
		"requests",
		"urllib3",
    ],
    zip_safe=False)
