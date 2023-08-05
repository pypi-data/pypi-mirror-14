.. contents::


Why use this?
=============

Standardized sampledata makes it soo much easier to work on a project
(especially when working in teams).

This package eases the generation of sampledata for your plone project.


How to use it
=============

For developers working on a project there's a view listing and running
all available sampledata plugins:

http://localhost/plone/@@sampledata

.. image:: https://raw.githubusercontent.com/collective/wm.sampledata/master/docs/screenshot.png
   :alt: Screenshot of the @@sampledata with enabled example plugin

By default the view does not list any plugins.
The screen above shows the example plugin activated via ``<include package="wm.sampledata.example" />``.


Writing and registering your custom sampledata plugin is very easy::

	from wm.sampledata import utils

    class MyPlugin(object):
        implements(ISampleDataPlugin)

        title = u"My Plugin Content"
        description = u"Creates a portlet and a random image"

        def generate(self, context):
            portlet = StaticAssignment(u"Sample Portlet", "<p>some content</p>")
            utils.addPortlet(context, 'plone.leftcolumn', portlet)

            utils.createImage(context, 'random-nature.jpg',
                        file = utils.getRandomImage(category='nature', gray=False),
                    	title=u"Random Image",
                    	description=u"Downloaded from lorempixel.com")


    myPlugin = MyPlugin()
    component.provideUtility(myPlugin,
                             ISampleDataPlugin
                             'my.plugin')

See `wm.sampledata.example`__
for a complete example of a custom plugin.

.. __: http://dev.plone.org/collective/browser/wm.sampledata/trunk/wm/sampledata/example



You can also group plugins (and even other plugin-gropus) so users need to run only one plugin to setup their sampledata correctly::

    from wm.sampledata import PluginGroup

    class TestPortal(PluginGroup):

        PLUGINS = [
           MyPlugin,  # also 'my.plugin' could be used
           MainMenu,
           AnotherPluginGroup,
        ]

    title = u"Complete Test Portal"
    description = u"Creates Main Menu items, Sampledata Folder and Portlets"

Note that you can use the utility names as well in `PLUGINS` but using classes directly is more straight forward in most cases.


There is a growing set of utility methods in ``wm.sampledata.utils`` (eg for
handling portlets and files, or download images from http://lorempixel.com)
which you can use in your plugins.


Installation
============


Simply add ``wm.sampledata`` to your buildout's instance eggs - a zcml slug is not needed
in plone versions that ship with z3c.autoinclude (Plone>=3.3)::

    [buildout]
    ...
    eggs =
        ...
        wm.sampledata



Why yet another package?
========================

There are several other packages for generating test/sampledata but none of them
fitted my usecase. (Which is providing a user interface for pluggable sampledata generators
so developers/skinners can use standardized data when developing on a project)

A while ago i `asked what other people do on plone.users`__

.. __: http://plone.293351.n2.nabble.com/Best-way-to-create-sampledata-for-tests-and-development-tp338487p338487.html


z3c.sampledata
    Would do the same and much more (dependencies, groups, configuration ui for each plugin)

    for me it was too complex to get it running on my zope2 instance and it
    seems to be tailored for zope3 anyway.

    Basically it would be great to make wm.sampledata use z3c.sampledata
    and provide plone specific plugins for it.

    .. http://comments.gmane.org/gmane.comp.web.zope.plone.devel/17379


`zopyx.ipsumplone`_
    Seems to provide very similar utility methods.
    No pluggable Generators, No User-Interface

	.. _`zopyx.ipsumplone`: https://pypi.python.org/pypi/zopyx.ipsumplone/


`ely.contentgenerator`_
    provides a xml syntax to create samplecontent,
    might be useful to use in custom plugins

    .. _`ely.contentgenerator`: http://ely.googlecode.com/svn/ely.contentgenerator


collective.contentgenerator
    looks like this is meant for creating (random) sampledata for stresstests


`collective.lorem`_
	content action to fill content with lorem-ipsum text and provides `utility methods
	<http://svn.plone.org/svn/collective/collective.lorem/trunk/collective/lorem/generation.txt>`_
	`createStandardContent` to create random content (news, documents, files, image)
	and `createNestedStructure` to create arbitrary nested folder structures.

	.. _`collective.lorem`: http://pypi.python.org/pypi/collective.lorem/


`collective.loremipsum`_
	Allows to create members (names taken from fakenamegenerator.com)

	.. _`collective.loremipsum`: https://github.com/collective/collective.loremipsum


`zettwerk.setup`_
    contains utility methods for setuphandlers. the one in structure.py offers
    a method to create content out of a list of dictionaries.

    .. _`zettwerk.setup`: https://github.com/collective/zettwerk.setup/blob/master/zettwerk/setup/structure.py


TODO
====

Include Ipsum Ipsum text obtained via the api from http://www.randomtext.me/

(for other interesting/funny generators see
http://designshack.net/articles/inspiration/30-useful-and-hilarious-lorem-ipsum-generators/)

use plone.api in utility methods or replace them with plone.api where
appropriate

eventually provide api to use fakenamegenerator.com for names
(collective.loremipsum already uses that)





Contribute
==========

If you have any ideas for improvement or know another alternative to this package please `File a ticket <https://github.com/collective/wm.sampledata/issues>`_ or `drop me a mail <mailto:harald (at) webmeisterei dot com>`_
