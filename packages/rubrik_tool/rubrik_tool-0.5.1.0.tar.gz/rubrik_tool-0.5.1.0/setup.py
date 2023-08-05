from setuptools import setup

setup(name='rubrik_tool',
      version='0.5.1.0',
      description='Python wrappers for Rubrik\'s APIs',
      url='http://github.com/scaledata/rubrik_tool',
      author='Rubrik',
      author_email='adam.goldberg@rubrik.com',
      license='MIT',
      packages=['rubrik_tool'],
      install_requires=[
        'requests',
        'pyyaml',
        'python-dateutil',
        'pytz',
      ],
      entry_points={
        'console_scripts': [
            'rubrik_tool=rubrik_tool.rubrik_tool:cli_entry_point',
        ]
      },
      zip_safe=False,
      classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='rubrik',
      include_package_data=True,
)
