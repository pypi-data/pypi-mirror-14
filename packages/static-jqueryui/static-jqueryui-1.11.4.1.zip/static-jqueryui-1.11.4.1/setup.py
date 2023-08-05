
import os
import sys

from setuptools import setup, find_packages


version = __import__('jqueryui').__version__

if sys.argv[-1] == 'publish':
    os.system('git tag -a %s -m "version %s"' % (version, version))
    os.system("git push --tags")
    os.system('python setup.py register')
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()


setup(
    name='static-jqueryui',
    version=version,
    url="https://github.com/wtayyeb/static-jqueryui",
    description='jQuery UI packaged in an handy django app to speed up new applications and deployment.',
    author='wtayyeb',
    author_email='wtayyeb@gmail.com',
    license='MIT',
    keywords='django jqueryui staticfiles templatetags',
    packages=find_packages(),
    install_requires=['django-appconf', ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)
