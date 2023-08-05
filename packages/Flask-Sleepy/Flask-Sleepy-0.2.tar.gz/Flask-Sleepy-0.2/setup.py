from setuptools import setup

setup(name='Flask-Sleepy',
      version='0.2',
      description="REST is hard. Let's go shopping",
      author='Robin Ramael',
      author_email='robin.ramael@gmail.com',
      packages=['sleepy'],
      install_requires=[
          'Flask',
          'Flask-Script',
          'Flask-SQLAlchemy',
          'Flask-Testing',
          'Flask-Marshmallow',
          'marshmallow-sqlalchemy'
      ],
      url="https://github.com/RobinRamael/flask-sleepy",
      download_url="https://github.com/RobinRamael/flask-sleepy/tarball/0.1.2",
      zip_safe=False,
      include_package_data=True,
      keywords=["flask", "rest", "api"])