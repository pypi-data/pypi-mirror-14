from setuptools import setup

setup(name='oopyconnector',
      version='0.4.6',
      description='Python wrapper for the Only Once API',
      url='http://github.com/wizardofzos/onlyonce-python',
      author='Henri Kuiper',
      author_email='henrikuiper@zdevops.com',
      license='BSD',
      packages=['oopyconnector'],
      classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
      zip_safe=False)
