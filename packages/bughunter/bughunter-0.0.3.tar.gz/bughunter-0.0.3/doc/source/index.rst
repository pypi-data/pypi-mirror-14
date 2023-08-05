.. demo documentation master file, created by
   sphinx-quickstart on Tue Mar 22 11:43:30 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==============
Document Title
==============

--------
SubTitle
--------

SectionTitle
============

我是李浩然
for deploying and managing containers as first class resources in OpenStack.

* **Free software:** under the `Apache license <http://www.apache.org/licenses/LICENSE-2.0>`_
* **Source:** http://git.openstack.org/cgit/openstack/magnum
* **Blueprints:** https://blueprints.launchpad.net/magnum
* **Bugs:** http://bugs.launchpad.net/magnum
* **REST Client:** http://git.openstack.org/cgit/openstack/python-magnumclient

BugHunter
=========
There are several different types of objects in the magnum system:

* **Bay:** A collection of node objects where work is scheduled
* **BayModel:** An object stores template information about the bay which is
  used to create new bays consistently
* **Node:** A baremetal or virtual machine where work executes
* **Pod:** A collection of containers running on one physical or virtual
  machine
* **Service:** An abstraction which defines a logical set of pods and a policy
  by which to access them
* **ReplicationController:** An abstraction for managing a group of pods to
  ensure a specified number of resources are running
* **Container:** A Docker container

Two binaries work together to compose the magnum system.  The first binary
(accessed by the python-magnumclient code) is the magnum-api REST server.  The
REST server may run as one process or multiple processes.  When a REST request
is sent to the client API, the request is sent via AMQP to the
magnum-conductor process.  The REST server is horizontally scalable.  At this
time, the conductor is limited to one process, but we intend to add horizontal
scalability to the conductor as well.

The magnum-conductor process runs on a controller machine and connects to a
Kubernetes or Docker REST API endpoint.  The Kubernetes and Docker REST API
endpoints are managed by the bay object.

When service or pod objects are created, Kubernetes may be directly contacted
via the Kubernetes REST API.  When container objects are acted upon, the
Docker REST API may be directly contacted.

Features
========

* Abstractions for bays, containers, nodes, pods, replication controllers, and
  services
* Integration with Kubernetes and Docker for backend container technology
* Integration with Keystone for multi-tenant security
* Integration with Neutron for Kubernetes multi-tenancy network security

.. code-block:: python
  :linenos:

  def foo():
      print "I love you"

.. literalinclude:: example.py
  :language: python

+-----------+---------+-----------------+
|   node    |   func  |   ip            |
+===========+=========+=================+
|  compute1 |   nova  | 192.168.1.10    |
+-----------+---------+-----------------+

.. csv-table:: Frozen Delights!
  :header: "Treat", "Quality", "Decription"
  :widths: 15, 10, 30

  "BugHunter", 100, "On a stick"

.. list-table:: Frozen Delights!
  :widths: 15 10 30
  :header-rows: 1

  * - Treat
    - Quality
    - Description
  * - Albatross
    - 2.99
    - I love you

Test
====
* 列表第一集

  + 第二级

    - 第三级

  + 第二级的另一个项目

1. 数字
a. 小写字母
A. 大写字母
i) 小写罗马数字
(I) 大写罗马数字


*I love you*

**I love you**

:ref:`buzz <dev-quickstart>`

.. _fig_0101:
.. figure:: bamboo.jpg
  
  chart 1—1 bamboo

:ref:`bamboo <fig_0101>`

H\ :sub:`2`\ O

E = mc\ :sup:`2`

Paragraph
=========

This is a paragraph. It's quite
short.
  
  This paragraph will result in an indented block of
  text,typically used for quoting other text.How about
  the too long paragraph.Oh!I know!

this is another one. 

* **Source:** http://git.openstack.org/cgit/openstack/magnum
* **Blueprints:** https://blueprints.launchpad.net/magnum
* **Bugs:** http://bugs.launchpad.net/magnum

thisis\ *one*\ world

``double * black-quotes``

``*``

\* nidate

Ilvoe*you

1.  number

2.  upper-case letters 
    and it goes over many times

    with two paragraphs and all!

a.  lower case letters

    1.  with a sub-list starting at a different number
    2.  make sure the number are in the correct sequence though!

I.  upper-case roman

i.  lower roman

(1) numbers again

1)  and again


* abullet point using "*"

  - a sub-list using "-"

    + yet another sub-list

  - another item

.. [CIT2002] A citation
  (as often used in journals).

what
  Definition lists associate a term with a definition.

*how*
  The term is a one-line phrase, and the definition is one or more
  paragraphs or body elements, indented relative to the term.
  blank lines are not allowed between term and definition.

An example::

    Whitespace, newlines, blank lines, and all kinds of markup
  (like *this* or \this) is presented by literal nlocks.
  Lookie here, I've dropped an indentation level
  (but not far enough)

no more example

::

  this is preformatted text, and the
  last "::" paragraph is removed

Chapter 1 Title
===============

Section 1.1 Title
-----------------

Subsection 1.1.1 Title
~~~~~~~~~~~~~~~~~~~~~~

Section 1.2 Title
-----------------

Chapter 2 Title
===============

`Test`_

----

[CIT2002]_

Developer Info
==============

.. toctree::
   :maxdepth: 1

   dev/dev-quickstart
   dev/dev-manual-devstack
   dev/dev-build-atomic-image.rst
   dev/dev-kubernetes-load-balancer.rst
   dev/dev-tls.rst
   contributing
   heat-templates
   objects