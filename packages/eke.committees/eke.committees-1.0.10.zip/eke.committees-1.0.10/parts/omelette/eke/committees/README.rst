This package provides Plone 3 content objects for the EDRN Knowledge
Environment (EKE_)'s management, display, and RDF ingest of committees.


Content Types
=============

The content types introduced in this package include the following:

Committee Folder
    A folder that contains Committees.  It can also repopulate its
    contents from an RDF data source.
Committee
    A single EDRN committee identified by URI_.

The remainder of this document demonstrates the content types and RDF ingest
using a series of functional tests.


Tests
=====

In order to execute these tests, we'll first need a test browser::

    >>> app = layer['app']
    >>> from plone.testing.z2 import Browser
    >>> from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
    >>> browser = Browser(app)
    >>> browser.handleErrors = False
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
    >>> portal = layer['portal']    
    >>> portalURL = portal.absolute_url()

We'll also have a second browser that's unprivileged for some later
demonstrations::

    >>> unprivilegedBrowser = Browser(app)

Let's go!


Addable Content
---------------

Here we'll exercise some of the content objects available in this project and
demonstrate their properties and constraints.


Committee Folder
~~~~~~~~~~~~~~~~

A Committee Folder contains Committees.  They can be created anywhere in the
portal::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='committee-folder')
    >>> l.url.endswith('createObject?type_name=Committee+Folder')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'Senate Committees'
    >>> browser.getControl(name='description').value = u'This folder is just for functional tests.'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/committees/a'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'senate-committees' in portal.objectIds()
    True
    >>> f = portal['senate-committees']
    >>> f.title
    'Senate Committees'
    >>> f.description
    'This folder is just for functional tests.'
    >>> f.rdfDataSource
    'testscheme://localhost/committees/a'

Committee Folders hold Committees as well as other Committee Folders.  We'll
test adding Committees below, but let's make sure there's a link to create
nested Committee Folders::

    >>> browser.open(portalURL + '/senate-committees')
    >>> l = browser.getLink(id='committee-folder')
    >>> l.url.endswith('createObject?type_name=Committee+Folder')
    True


Committee
~~~~~~~~~

A single Committee object represents an EDRN committee.  Committees can be
created only in Committee Folders::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='committee')
    Traceback (most recent call last):
    ...
    LinkNotFoundError

However, before we create one, we'll need some people in the system that can
be committee members.  So, let's add some::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='site-folder').click()
    >>> browser.getControl(name='title').value = 'Questionable Sites'
    >>> browser.getControl(name='description').value = 'This folder is just for functional tests.'
    >>> browser.getControl(name='rdfDataSource').value = 'testscheme://localhost/sites/b'
    >>> browser.getControl(name='peopleDataSource').value = 'testscheme://localhost/people/b'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/questionable-sites/ingest')

Now we can create our own committee::

    >>> browser.open(portalURL + '/senate-committees')
    >>> l = browser.getLink(id='committee')
    >>> l.url.endswith('createObject?type_name=Committee')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = 'Agriculture, Nutrition, and Forestry'
    >>> browser.getControl(name='abbreviatedName').value = 'ANF'
    >>> browser.getControl(name='committeeType').value = 'Committee'
    >>> browser.getControl(name='chair:list').displayValue = ['Alottaspank, Dirk (2d)']
    >>> browser.getControl(name='coChair:list').displayValue = ['Cusexijilomimi, Crystal Hotstuff (3d)', 'Pawaka, Makin (3d)']
    >>> browser.getControl(name='consultant:list').displayValue = ['Pawaka, Makin (3d)']
    >>> browser.getControl(name='member:list').displayValue = ['Alottaspank, Dirk (2d)', 'Cusexijilomimi, Crystal Hotstuff (3d)', 'Pawaka, Makin (3d)']
    >>> browser.getControl(name='form.button.save').click()
    >>> 'agriculture-nutrition-and-forestry' in f.objectIds()
    True
    >>> c = f['agriculture-nutrition-and-forestry']
    >>> c.title
    'Agriculture, Nutrition, and Forestry'
    >>> c.committeeType
    'Committee'
    >>> len(c.chair)
    1
    >>> c.chair[0].title
    'Alottaspank, Dirk'
    >>> len(c.coChair)
    2
    >>> coChairs = [i.title for i in c.coChair]
    >>> coChairs.sort()
    >>> coChairs
    ['Cusexijilomimi, Crystal Hotstuff', 'Pawaka, Makin']
    >>> len(c.consultant)
    1
    >>> c.consultant[0].title
    'Pawaka, Makin'
    >>> len(c.member)
    3
    >>> members = [i.title for i in c.member]
    >>> members.sort()
    >>> members
    ['Alottaspank, Dirk', 'Cusexijilomimi, Crystal Hotstuff', 'Pawaka, Makin']


Committee View
~~~~~~~~~~~~~~

The default view for a Committee is fairly basic.  The only special thing is
that members should be hyperlinks::

    >>> browser.open(portalURL + '/senate-committees/agriculture-nutrition-and-forestry')
    >>> browser.contents
    '...Chair...href=.../alottaspank-dirk...Alottaspank, Dirk...'


Committee Folder View
~~~~~~~~~~~~~~~~~~~~~

A Committee Folder by default displays its committees in alphabetical order by
title.  Let's check that.  First, we'll need to toss in a couple other
committees::

    >>> browser.open(portalURL + '/senate-committees')
    >>> browser.getLink(id='committee').click()
    >>> browser.getControl(name='title').value = 'Foreign Relations'
    >>> browser.getControl(name='committeeType').value = 'Committee'
    >>> browser.getControl(name='form.button.save').click()

That's one; now another::

    >>> browser.open(portalURL + '/senate-committees')
    >>> browser.getLink(id='committee').click()
    >>> browser.getControl(name='title').value = 'Armed Services'
    >>> browser.getControl(name='committeeType').value = 'Committee'
    >>> browser.getControl(name='form.button.save').click()

Now, the ordering::

    >>> browser.open(portalURL + '/senate-committees')
    >>> browser.contents
    '...Agriculture...Armed Services...Foreign Relations...'

Additionally, any nested Committees Folders should appear above the list of
committees::

    >>> 'Special Subsection' not in browser.contents
    True
    >>> browser.getLink(id='committee-folder').click()
    >>> browser.getControl(name='title').value = 'Special Subsection on Independent Committees'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/senate-committees')
    >>> browser.contents
    '...Special Subsection...Agriculture...Armed Services...Foreign Relations...'


RDF Ingestion
-------------

Committee Folders support a URL-callable method that causes them to ingest
RDF and create corresponding objects, just like Knowledge Folders in the
``eke.knowledge`` package.  However, they don't create Committee objects at
all like we've seen just above.  They used to, but not anymore!  Instead, they
now create Group Space objects from the ``edrnsite.collaborations`` package.

That's right, you can now add Group Spaces to Committee Folders::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='committee-folder').click()
    >>> browser.getControl(name='title').value = 'House Committees'
    >>> browser.getControl(name='rdfDataSource').value = u'testscheme://localhost/committees/a'
    >>> browser.getControl(name='siteSumDataSource').value = u'testscheme://localhost/summary/a'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/house-committees/content_status_modify?workflow_action=publish')
    >>> f = portal['house-committees']
    >>> l = browser.getLink(id='group-space')
    >>> l.url.endswith('createObject?type_name=Group+Space')
    True

Watch what happens when we ingest from the RDF data source
``testscheme://localhost/committees/a``::

    >>> browser.getLink('Ingest').click()
    >>> browser.contents
    '...The following items have been created...Appropriations...'
    >>> len(f.objectIds())
    2
    >>> 'appropriations' in f.objectIds() and 'ways-and-means' in f.objectIds()
    True
    >>> a = f['appropriations']
    >>> a.title
    'Appropriations'
    >>> a.description
    'Abbreviated name: App. Committee type: Committee.'
    >>> a.index_html.chair.title
    'Alottaspank, Dirk'
    >>> a.index_html.coChair.title
    'Pawaka, Makin'
    >>> 'Cusexijilomimi, Crystal Hotstuff' in [i.title for i in a.index_html.members]
    True

A group space is an interactive place where people can share documents and
arrange meetings.  For example, here we'll add a file to the Appropriations
space::

    >>> from StringIO import StringIO
    >>> fakeFile = StringIO('%PDF-1.5\nThis is sample PDF file in disguise.\nDo not try to render it; it may explode.')
    >>> browser.open(portalURL + '/house-committees/appropriations')
    >>> l = browser.getLink('New File')
    >>> l.url.endswith('createObject?type_name=File')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'Shiny New File'
    >>> browser.getControl(name='description').value = u'A file for functional tests.'
    >>> browser.getControl(name='file_file').add_file(fakeFile, 'application/pdf', 'test.pdf')
    >>> browser.getControl(name='form.button.save').click()

Neat.

More RDF?  Sure, the source ``testscheme://localhost/committees/b`` contains
both the above committees and an additional one.  Since ingestion purges
existing objects, we shouldn't get duplicate copies of the above committees::

    >>> browser.open(portalURL + '/house-committees')
    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='rdfDataSource').value = 'testscheme://localhost/committees/b'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink('Ingest').click()
    >>> objIDs = f.objectIds()
    >>> objIDs.sort()
    >>> objIDs
    ['appropriations', 'science-and-technology', 'ways-and-means']

And the file in the Appropriations committee is still there too::

    >>> 'shiny-new-file' in a.keys()
    True


RDF Data Sources
~~~~~~~~~~~~~~~~

The URL to an RDF data source is nominally displayed on a Committee folder,
but only if you're an administrator, which our test browser is logged in as.
See, there's the RDF URL::

    >>> browser.open(portalURL + '/house-committees')
    >>> browser.contents
    '...RDF Data Source...testscheme://localhost/committees/b...'

However, mere mortals shouldn't see that::

    >>> unprivilegedBrowser.open(portalURL + '/house-committees')
    >>> 'RDF Data Source' not in unprivilegedBrowser.contents
    True

That's it!


.. References:
.. _EKE: http://cancer.jpl.nasa.gov/documents/applications/knowledge-environment
.. _RDF: http://w3.org/RDF/
.. _URI: http://w3.org/Addressing/
