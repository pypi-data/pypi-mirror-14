from distutils.core import setup


setup(
    name='just-another-settings',
    version='1.0',
    packages=['just_another_settings'],
    url='https://github.com/andreyrusanov/just-another-settings',
    license='MIT',
    author='Andrey Rusanov',
    author_email='andrey@rusanov.me',
    description='Small lib to manage settings as object for Flask/Bottle/custom apps',
    long_description=open('README.rst').read(),
    tests_require=[
        'nose==1.3.7',
        'mock==1.3.0'
    ],
    test_suite="nose.collector",
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 5 - Production/Stable',
    ],
)
