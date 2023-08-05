from distutils.core import setup

setup(name='pygnucash',
      author='Matthias Braun',
      author_email='matze@braunis.de',
      maintainer='Thomas Levine',
      maintainer_email='_@thomaslevine.com',
      description='read gnucash files in python',
      url='https://github.com/MatzeB/pygnucash',
      py_modules=['gnucash', 'gnucashutil'],
      scripts=['edit.py', 'gnucash2ledger.py', 'stockreport.py'],
      version='0.1',
      license='2-clause BSD',
      classifiers=[
          'Programming Language :: Python :: 3.5',
      ],
)
