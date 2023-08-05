try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='libedooon',
    packages=['libedooon'],
    version='0.2',
    description='A Python wrap for Edooon RESTful APIs.',
    author='Lei Yang',
    author_email='yltt1234512@gmail.com',
    url='https://github.com/yangl1996/libedooon',
    keywords=['api', 'library'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: GIS'
    ],
    license='MIT License',
    install_requires=['requests', 'gpxpy'],
)
