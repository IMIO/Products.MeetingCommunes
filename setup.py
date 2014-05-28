from setuptools import setup, find_packages
import os

version = '3.2.1dev'

setup(name='Products.MeetingCommunes',
      version=version,
      description="Official meetings management for college and council of belgian communes (PloneMeeting extension profile)",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://www.communesplone.org/les-outils/applications-metier/gestion-des-deliberations',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
            test=['unittest2',
                  'zope.testing',
                  'plone.testing',
                  'plone.app.testing',
                  'plone.app.robotframework',
                  'communesplone.iconified_document_actions',
                  'Products.CMFPlacefulWorkflow',
                  'zope.testing',
                  'Products.PloneTestCase',
                  'collective.ckeditor',
                  'plonetheme.imioapps'],
            templates=['Genshi',
                  ]),
      install_requires=[
          'setuptools',
          'appy',
          'Products.CMFPlone',
          'Pillow',
          'communesplone.iconified_document_actions',
          'Products.PloneMeeting',
          'collective.ckeditor',
          'plonetheme.imioapps'],
      entry_points={},
      )
