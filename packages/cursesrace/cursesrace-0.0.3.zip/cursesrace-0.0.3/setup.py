from setuptools import setup, find_packages


setup(name='cursesrace',
      version='0.0.3',
      description='An ncurses example: RACE',
      long_description='',
      classifiers=[],
      url='http://github.com/storborg/cursesrace',
      keywords='',
      author='Scott Torborg',
      author_email='storborg@gmail.com',
      install_requires=[],
      license='MIT',
      packages=find_packages(),
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False,
      entry_points="""\
      [console_scripts]
      cursesrace = cursesrace:main
      """,
      )
