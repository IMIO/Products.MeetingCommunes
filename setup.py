from setuptools import find_packages
from setuptools import setup


version = '4.2b13'

setup(
    name='Products.MeetingCommunes',
    version=version,
    description="Official meetings management for college and council of belgian"
    "communes (PloneMeeting extension profile)",
    long_description=open("README.rst").read() + "\n" + open("CHANGES.rst").read(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='',
    author='Gauthier Bastien',
    author_email='gauthier@imio.be',
    url='http://www.imio.be/produits/gestion-des-deliberations',
    license='GPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=['Products.PloneMeeting[test]'],
        templates=['Genshi', ]),
    install_requires=[
        'setuptools',
        'Products.CMFPlone',
        'Pillow',
        'Products.PloneMeeting'],
    entry_points={},
)
