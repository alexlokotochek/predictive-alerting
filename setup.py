from setuptools import setup, find_packages


setup(
    name='predictive-alerting',
    version='0.0.3',
    description='cian ml etl',
    author='323',
    author_email='323@323.ru',
    url='https://github.com/alexlokotochek/predictive-alerting',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'fbprophet>=0.5',
    ],
)