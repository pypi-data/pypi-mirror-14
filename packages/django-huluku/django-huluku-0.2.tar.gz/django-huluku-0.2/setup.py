from setuptools import setup

setup(name='django-huluku',
      version='0.2',
      description='For making writing of policies easier',
      url='http://github.com/lefootballroi/django-huluku',
      author='Anthony Eli Agbenu',
      author_email='eli.anthony.agbenu@gmail.com',
      license='MIT',
      packages=['huluku'],
      install_requires=[
          'django-ckeditor',
      ],      
      zip_safe=False)
