from setuptools import setup

setup(name='loveallufev-crawler',
    version='0.1',
    description='The crawler module',
    url='https://github.com/loveallufev/crawler',
    author='Duc Trung NGUYEN',
    author_email='ductrungkhtn@gmail.com',
    license='MIT',
    packages=['request_core'],
    install_requires=[
        "beautifulsoup4",
		"lxml",
		"requests",
		"urllib3",
		"virtualenv",
		"wheel",
    ],
    zip_safe=False)
