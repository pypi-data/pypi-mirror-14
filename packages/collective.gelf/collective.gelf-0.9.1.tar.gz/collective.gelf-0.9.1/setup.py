from setuptools import setup, find_packages


setup(
    name='collective.gelf',
    version='0.9.1',
    description='Graylog logging handler for Plone',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    classifiers=[
        'Programming Language :: Python',
    ],
    keywords='',
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    url='https://github.com/datakurre/collective.gelf',
    license='EUPL',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'ZConfig',
        'pygelf'
    ],
    extras_require={'test': [
    ]},
    entry_points="""
    """,
)
