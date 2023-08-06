Changelog
=========

0.5 (2016-03-31)
----------------

- `util.getFlickrImage` and `utils.getRandomFlickrImage` allow to obtain images from loremflickr.com.
  [pcdummy, fRiSi]


0.4 (2016-03-08)
----------------

- Classes can be used to define plugin groups as well as utility names
  [pcdummy]


0.3 (2014-08-25)
----------------

- utils.doWorkflowTransition uses plone_utils internally since
  portal_workflow.doActionFor does not set the effective date when publishing

- errors raised in finally clause did not pop up with debug=True

- added utility function ``createFile`` to create file-content the same way
  as ``createImage`` creates image-content.

- replace _createObjectByType with invokeFactory since - despite a little better
  performance - it has some nasty side-effects. eg the ``_at_creation_flag`` is
  is not properly handeled

- added utility function ``raptus_hide_for`` and ``raptus_show_for`` to be able
  to hide and show content items in specific raptus.article components.

  (see https://pypi.python.org/pypi/raptus.article.default for more information
  on raptus.article)

0.2.2 (2013-05-08)
------------------

- add traceback logging on errors [saily]

- added utility functions (``utils.getImage`` and ``utils.getRandomImage``) to
  download images from lorempixel.com (see wm.sampledata.example for usage)
  [fRiSi]

- more intuitive syntax for blockPortlets (change breaks backward
  compatibility) [fRiSi]

0.2.1 (2012-05-29)
------------------

- fix links for running plugins so they work for
  http://host/plonesite/@@sampledata, too. (not just http://host/@@sampledata)
  [fRiSi]

- added utility method `constrainTypes` to set which objects an be added to
  folderish objects [fRiSi]

0.2 (2011-12-02)
----------------

- ``SampledataView.runPlugin`` returns the result of ``Plugin.generate``. This
  makes it easy to check if the plugin was sucessfully run in unittests.

0.1 (2011-01-31)
----------------

- Initial release
