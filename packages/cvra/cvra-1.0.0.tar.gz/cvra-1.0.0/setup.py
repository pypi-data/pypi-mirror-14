from setuptools import setup

setup(
    name='cvra',
    version='1.0.0',
    description='Metapackage for CVRA Python stack',
    author='Club Vaudois de Robotique Autonome',
    author_email='info@cvra.ch',
    url='http://cvra.ch',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ],
    install_requires=[
        'cvra-packager',
        'cvra-bootloader',
        ],
    )

