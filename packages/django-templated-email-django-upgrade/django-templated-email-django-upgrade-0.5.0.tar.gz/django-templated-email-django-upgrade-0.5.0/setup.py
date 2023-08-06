from setuptools import setup

DESCRIPTION = "Fork of a Django oriented templated / transaction email abstraction"

LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Framework :: Django',
]

setup(
    name='django-templated-email-django-upgrade',
    version='0.5.0',
    packages=['templated_email', 'templated_email.backends'],
    author='Bharadwaj Srigiriraju',
    author_email='krishna.bharadwaj6@gmail.com',
    url='http://github.com/bharadwaj6/django-templated-email/',
    license='MIT',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'six',
    ],
)
