from pathlib import Path

from setuptools import find_packages, setup

readme_file = Path(__file__).parent / 'README.md'
with readme_file.open() as f:
    long_description = f.read()

_base_extras = [
    'django>=4',
    'django-allauth',
    'django-auth-style',
    'django-cors-headers',
    'django-extensions',
    'django-filter',
    'django-girder-utils>=0.9.0',
    # django-oauth-toolkit==1.3.3 doesn't have working PKCE
    'django-oauth-toolkit>=1.4.0',
    'drf-yasg',
    'psycopg2',
    'rich',
    'whitenoise[brotli]',
]

setup(
    name='django-composed-configuration',
    description='Turnkey Django settings for data management applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache 2.0',
    url='https://github.com/girder/django-composed-configuration',
    project_urls={
        'Bug Reports': 'https://github.com/girder/django-composed-configuration/issues',
        'Source': 'https://github.com/girder/django-composed-configuration',
    },
    author='Kitware, Inc.',
    author_email='kitware@kitware.com',
    keywords='django girder configuration configurations setting settings',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 4.0',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python',
    ],
    python_requires='>=3.8',
    install_requires=[
        'django-configurations[database,email]',
    ],
    extras_require={
        # Required for DevelopmentBaseConfiguration / TestingBaseConfiguration
        'dev': _base_extras + ['django-debug-toolbar', 'django-minio-storage'],
        # Required for ProductionBaseConfiguration
        'prod': _base_extras
        + [
            'django-storages[boto3]',
            'sentry-sdk',
        ],
    },
    packages=find_packages(),
    include_package_data=True,
)
