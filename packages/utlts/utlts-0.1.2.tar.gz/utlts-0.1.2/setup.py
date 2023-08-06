from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='utlts',
        packages=find_packages(),
        version='0.1.2',
        description='Utility functions functions.',
        long_description='',
        url='https://github.com/asalomatov/utlts',
        author='Andrei Salomatov',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Operating System :: OS Independent',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License', 
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            ],
        install_requires=[
            'pandas>=0.17.1',
            'numpy>=1.10.2',
            'pysam>=0.8.3'
        ],
)
