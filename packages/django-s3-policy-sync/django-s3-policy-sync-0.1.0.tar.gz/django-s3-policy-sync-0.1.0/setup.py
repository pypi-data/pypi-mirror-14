from setuptools import setup

setup(name='django-s3-policy-sync',
      version='0.1.0',
      description='Django middleware that synchronizes S3 policy to from files',
      url='https://github.com/Rhumbix/django-s3-policy-sync.git',
      author='Kenneth Jiang',
      author_email='kenneth@rhumbix.com',
      license='MIT',
      packages=['s3_policy_sync'],
      install_requires=[
          'Django',
          'boto',
      ],
      zip_safe=False)
