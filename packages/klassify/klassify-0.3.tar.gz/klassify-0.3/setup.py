from setuptools import setup, find_packages

setup(
    name='klassify',
    version='0.3',
    description='Redis based text classification service',
    author='Fatih Erikli',
    author_email='fatiherikli@gmail.com',
    url='https://github.com/fatiherikli/klassify',
    packages=find_packages(exclude=['test_project']),
    install_requires=[
        'nltk==3.1',
        'tornado==4.3',
        'tornado-redis==2.4.18'
    ],
    classifiers=[
        'Environment :: Web Environment'
    ]
)
