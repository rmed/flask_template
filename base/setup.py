from setuptools import setup, find_packages

setup(
    name='flask_app_template',
    version='0.1.0',

    description='A Flask template',
    long_description='',

    url='https://github.com/rmed/flask_template',

    author='Rafael Medina García',
    author_email='rafamedgar@gmail.com',

    packages=find_packages(),

    include_package_data=True,
    exclude_package_data={
        '': ['static/.webassets-cache/*']
    },

    zip_safe=False,

    entry_points={
        'console_scripts': [
            'flask_app_template=flask_app_template.commands:cli.main',
        ]
    }
)
