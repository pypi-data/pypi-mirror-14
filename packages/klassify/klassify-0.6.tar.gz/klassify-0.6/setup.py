from setuptools import setup, find_packages

setup(
    name='klassify',
    version='0.6',
    description='Redis based text classification service',
    author='Fatih Erikli',
    author_email='fatiherikli@gmail.com',
    url='https://github.com/fatiherikli/klassify',
    packages=[
        'klassify',
        'klassify.backend',
    ],
    install_requires=[
        'nltk==3.1',
        'tornado==4.3',
        'tornado-redis==2.4.18'
    ],
    classifiers=[
        'Environment :: Web Environment'
    ]
)
