try:
    import multiprocessing
except ImportError:
    pass


from setuptools import setup

setup(
    name='Flask-Imagine',
    version='0.1.5',
    description='Dynamic image resizing and storing on AWS S3 for Flask.',
    url='https://github.com/kronas/Flask-Imagine',
        
    author='Kronas',
    author_email='kronas.sw@gmail.com',
    license='MIT',

    packages=['flask_imagine'],

    install_requires=[

        'Flask>=0.9',
        'itsdangerous', # For Flask v0.9
        'Pillow',

    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    zip_safe=False,
)
