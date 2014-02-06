
Overview
========

ECQuiz is an extension module (a so-called *product*) for the
Plone_ content management system.  It allows you to create and 
deliver multiple-choice tests.

.. _Plone: http://plone.org/


Download
========

`plone.org products page`_

.. _plone.org products page: http://plone.org/products/ecquiz/


Prerequisites
=============

To use ECQuiz you need:

#. A current Plone installation, specifically Plone 3.x; check
   plone.org_ for details.

#. The DataGridField_  product.  This version of ECQuiz has been 
   tested extensively with DataGridField version 1.6.  Newer 
   versions might or might not work as well.

.. _plone.org :http://plone.org/products/plone
.. _DataGridField: http://plone.org/products/datagridfield/


Installation
============

See the `Installing an Add-on Product`_ tutorial for more detailed 
product installation instructions.
        
.. _Installing an Add-on Product: http://plone.org/documentation/tutorial/third-party-products/installing


Installing with buildout
------------------------

If you are using `buildout`_ to manage your instance you can install 
ECQuiz by adding it to the eggs line for your instance::

  [instance]
  eggs =
      ... 
      Products.ECQuiz

After updating the configuration you need to run ``bin/buildout``, 
which will take care of updating your system.

Then restart your zope instance and use the Add/Remove products page
in Site Setup to install ECQuiz.

.. _buildout: http://pypi.python.org/pypi/zc.buildout


Installing without buildout
---------------------------

Move (or symlink) the ``ECQuiz`` folder of this project
(``Products.ECQuiz/Products/ECQuiz``) into the ``Products`` directory 
of the Zope instance it has to be installed for, and restart the 
server.  Use the Add/Remove products page in Site Setup to install 
ECQuiz.


Support
=======

For questions and discussions about ECAssignmentBox, please join the
`eduComponents mailing list`_.

.. _eduComponents mailing list: https://listserv.uni-magdeburg.de/mailman/listinfo/educomponents


Credits
=======

ECQuiz was written by `Wolfram Fenske`_ and `Michael Piotrowski`_.  
Sascha Peilicke implemented the Quick Edit functionality.

The Statistics class was written by `Chad J. Schroeder`_.  It is 
licensed under the `Python license`_.

The L2 Lisp parser was written by Wolfram Fenske.

Several icons used in ECQuiz are from the `Silk icon set`_ by Mark 
James.  They are licensed under a `Creative Commons Attribution 2.5 License`_.

The Slovenian translation was contributed by Matjaž Jeran.  The Italian 
translation was contributed by Elena Momi.

Jim Baack contributed a rough version of the Plone 3 port.

The Plone 3 port was finished by `Eudemonia Solutions AG`_, with funding
from the `ITC of the ILO`_.

ECQuiz was ported to Plone 4 by `Eudemonia Solutions AG`_.

.. _Michael Piotrowski: mxp@dynalabs.de
.. _Wolfram Fenske: wfenske@eudemonia-solutions.de
.. _Chad J. Schroeder: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/409413
.. _Python license: http://www.python.org/license
.. _Silk icon set: http://www.famfamfam.com/lab/icons/silk/
.. _Creative Commons Attribution 2.5 License: http://creativecommons.org/licenses/by/2.5/
.. _Eudemonia Solutions AG: http://www.eudemonia-solutions.de/
.. _ITC of the ILO: http://www.itcilo.org/
