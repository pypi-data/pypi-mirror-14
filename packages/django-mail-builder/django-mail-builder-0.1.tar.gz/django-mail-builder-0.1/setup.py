from setuptools import setup


setup(
    name='django-mail-builder',
    description='Simple template-based EmailMessage builder for Django',
    version='0.1',
    packages=['mail_builder'],
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    license='BSD',
    keywords='django email template',
    url='https://github.com/funkybob/django-mail-builder',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
