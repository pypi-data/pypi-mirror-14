from setuptools import setup, find_packages

setup(
    name='django-tables-helper',
    py_modules=['django-tables-helper'],
    version='0.1.0',
    description='Helpful table addons for columns and pagination.',
    license='BSD',
    url='https://github.com/paperreduction/django-table-helper',
    download_url='https://github.com/paperreduction/django-table-helper/tarball/0.1.0',
    author='Dan Dietz',
    author_email='danddietz@gmail.com',
    install_requires=['django>=1.5'],
    keywords='django tables2 tables',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
)
