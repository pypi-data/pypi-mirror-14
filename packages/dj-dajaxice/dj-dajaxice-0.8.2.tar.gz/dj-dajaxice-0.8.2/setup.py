from distutils.core import setup

setup(
    name='dj-dajaxice',
    version='0.8.2',
    author='Dheerendra Rathor',
    author_email='dheeru.rathor14@gmail.com',
    description='Agnostic and easy to use ajax library for django',
    url='http://dajaxproject.com',
    license='BSD',
    packages=['dajaxice',
              'dajaxice.templatetags',
              'dajaxice.core'],
    package_data={'dajaxice': ['templates/dajaxice/*']},
    long_description=(
        """
        Original Project :- Django Dajaxice (django-dajaxice)

        This project is an attempt to make it compatible to Django 1.9+ as original
        project is unmaintained.

        """
        "Easy to use AJAX library for django, all the "
        "presentation logic resides outside the views and "
        "doesn't require any JS Framework. Dajaxice uses the "
        "unobtrusive standard-compliant (W3C) XMLHttpRequest "
        "1.0 object."),
    install_requires=[
        'Django>=1.8'
    ],
    classifiers=['Development Status :: 4 - Beta',
                'Environment :: Web Environment',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: BSD License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Topic :: Utilities']
)
