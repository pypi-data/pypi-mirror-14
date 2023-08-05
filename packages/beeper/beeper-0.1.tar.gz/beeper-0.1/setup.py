"""
Bundle virtualenv and project to an artifact.
"""

from setuptools import setup

setup(
    name='beeper',
    version='0.1',
    url='https://github.com/soasme/beeper',
    license='MIT',
    author='Ju Lin',
    author_email='soasme@gmail.com',
    description='Bundle virtualenv and project to an artifact.',
    long_description=__doc__,
    py_modules=['beeper'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'click>=1.0',
        'PyYAML>=3.11',
    ],
    entry_points={
        'console_scripts': [
            'beeper = beeper:build'
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
