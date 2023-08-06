import setuptools


if __name__ == "__main__":
    setuptools.setup(
        # Name of the project
        name='stft',

        # Version
        version='0.5.2',

        # Description
        description='Short Time Fourier transform for NumPy.',

        # Your contact information
        author='Nils Werner',
        author_email='nils.werner@gmail.com',

        # License
        license='MIT',

        # Packages in this project
        # find_packages() finds all these automatically for you
        packages=setuptools.find_packages(exclude=['tests']),

        # Dependencies, this installs the entire Python scientific
        # computations stack
        install_requires=[
            'numpy>=1.6',
            'scipy>=0.9',
        ],

        extras_require={
            'docs': [
                'sphinx',
                'sphinxcontrib-napoleon',
                'sphinx_rtd_theme',
                'numpydoc',
            ],
            'tests': [
                'pytest',
                'pytest-cov',
                'pytest-pep8',
                'tox',
            ],
        },

        tests_require=[
            'pytest',
            'pytest-cov',
            'pytest-pep8',
        ],

        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Telecommunications Industry',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Multimedia :: Sound/Audio :: Analysis',
            'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis'
        ],
        zip_safe=True,
    )
