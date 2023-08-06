from distutils.core import setup

setup(
    name='micescraper',
    version='0.0.4',
    description='Applicant pdf scraper for MICE',
    url='https://github.com/sirrice/micescraper',
    author='Eugene wu',
    author_email='ewu@cs.columbia.edu',
    packages=['micescraper'],
    package_dir = {'micescraper' : 'micescraper'},
    scripts=['bin/micescraper'],
    keywords=['scraper'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ],
    long_description='see http://github.com/sirrice/micescraper',
    install_requires = [ 'click', 'requests', 'pyquery' ]
)
