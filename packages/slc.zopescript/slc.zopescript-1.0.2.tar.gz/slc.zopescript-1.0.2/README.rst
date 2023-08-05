.. image:: https://secure.travis-ci.org/plone/plone.api.png
    :target: http://travis-ci.org/#!/plone/plone.api

====================
slc.zopescript
====================

Base classes for running code as Zope console scripts

* `Source code @ GitHub <https://github.com/syslabcom/slc.zopescript>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/slc.zopescript>`_
* `Documentation @ ReadTheDocs <http://slczopescript.readthedocs.org>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/syslabcom/slc.zopescript>`_

Installation
============

To install `slc.zopescript` you add ``slc.zopescript``
to the dependencies of your own egg.

Usage
=====

slc.zopescript allows running code from the command line with a full Zope
instance and request available.

To create a console script you can derive a class from
`slc.zopescript.script.ConsoleScript` and implement the `run()` method. The
Zope app will be available as self.app and the first Plone Site as self.portal.
A request will be set up so that you can e.g. call browser views.
Example::

    from my.egg import MailHandler
    from slc.zopescript.script import ConsoleScript


    class MailHandlerScript(ConsoleScript):
        def run(self):
            mailhandler_view = MailHandler(self.context, self.context.REQUEST)
            mailhandler_view()

    mail_handler = MailHandlerScript()


In your buildout you can generate the console script e.g. with zc.recipe.egg::

    [mail_handler]
    recipe = zc.recipe.egg
    eggs = ${instance:eggs}
    scripts = mail_handler
    arguments = '${instance:location}/etc/zope.conf','admin',server_url='http://localhost:8081/Plone',context_path='/Plone/news'

The first argument must be the path to a valid zope.conf file. The second
argument is the user to run the script as. The optional server_url should be
the URL under which your site is externally reachable and allows you to use
meaningful absolute_url() calls. The optional context_path is the path to
an object that will be available as self.context in your script class.
