from setuptools import setup, find_packages


setup(
    name='recipe_collector',
    version='0.0.6',
    author='Brian Hines',
    author_email='brian@projectweekend.net',
    description='Collect and process recipes from various sources',
    url='https://github.com/projectweekend/recipe-collector',
    license='MIT',
    packages=find_packages(),
    py_modules=[],
    scripts=[],
    install_requires=[
        'boto3==1.3.0',
        'requests==2.9.1',
    ],
)
