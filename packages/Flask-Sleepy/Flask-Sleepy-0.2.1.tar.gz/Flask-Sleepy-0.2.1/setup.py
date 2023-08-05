from setuptools import setup

setup(name='Flask-Sleepy',
      version='0.2.1',
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
      url="https://git.prior-it.be/Prior-IT/flask-sleepy",
      download_url="https://git.prior-it.be/Prior-IT/flask-sleepy/archive/0.2.1.tar.gz",
      zip_safe=False,
      include_package_data=True,
      keywords=["flask", "rest", "api", "marshmallow", "sqlalchemy", "restful"],)