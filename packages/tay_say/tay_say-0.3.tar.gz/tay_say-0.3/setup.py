from distutils.core import setup

setup(
    name='tay_say',
    packages=['tay_say'],  # this must be the same as the name above
    version='0.3',
    description='A simple lib that prints out a random Taylor Swift lyric',
    author='Justin Beall',
    author_email='jus.beall@gmail.com',
    url='https://github.com/DEV3L/python-tay-say',
    download_url='https://github.com/DEV3L/python-tay-say/tarball/0.3',
    keywords=['testing', 'dev3l', 'taylor swift'],  # arbitrary keywords
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    entry_points={
        'console_scripts': [
            'tay_say = tay_say:print_lyric'
        ]},
)
