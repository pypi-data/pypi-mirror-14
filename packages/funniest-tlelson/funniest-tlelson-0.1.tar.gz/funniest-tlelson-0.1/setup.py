from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='funniest-tlelson', # N.B this must be unique on PyPi
      ## Random text and information
      version='0.1',
      description='The funniest joke in the world',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      #url='http://github.com/storborg/funniest',
      author='timbo',
      author_email='tim.l.elson@gmail.com',
      license='MIT',

      ## This is a list of the packages to include
      packages=['funniest'], # The packages you want to include. use >>> setuptools.find_packages()
      # Code manifest (Non-code is added in the MANIFEST.in file)
      include_package_data=True,  # Required for next line
      #package_data={"<package_from 'packages'>" : ['list_of_files', '*.py']},

      ## Package and Testing dependecies
      install_requires=[
          'markdown',
      ],
      #test_suite='pytest',  # ??
      tests_require=['pytest'],

      ## Console command access points
      # Method 1
      entry_points={
          'console_scripts': ['funniest-joke=funniest.command_line:main'],
      },
      # Method 2
      # This would require us creating a bin/ in the project, and writing a bash script
      # called funniest-joke that accesses our code. Method 1 is better
      #scripts=['bin/funniest-joke'],

      zip_safe=False)  # ??
