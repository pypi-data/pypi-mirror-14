Developer Documentation
=======================

.. toctree::
   :maxdepth: 2

   design
   components
   invocation
   caches
   developing_elements
   stable_interfaces

Quickstart
----------

To get started developing with ``diskimage-builder``, install to a
``virtualenv``::

 $ mkdir dib
 $ cd dib
 $ virtualenv create env
 $ source env/bin/activate
 $ git clone https://git.openstack.org/openstack/diskimage-builder
 $ cd diskimage-builder
 $ pip install -e .

You can now simply use ``disk-image-create`` to start building images
and testing your changes.  When you are done editing, use ``git
review`` to submit changes to the upstream gerrit.
