from setuptools import setup, find_packages


setup(
    version='7.0.0',
    name='incuna-videos',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'FeinCMS>=1.11,<1.12',
        'django-imagekit>=3.3,<3.4',
    ],
    description='Generic extensible video content.',
    author='Incuna Ltd',
    author_email='admin@incuna.com',
    url='https://github.com/incuna/incuna-videos',
)
