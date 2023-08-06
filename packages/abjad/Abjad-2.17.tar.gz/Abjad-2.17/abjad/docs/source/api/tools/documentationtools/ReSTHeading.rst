.. currentmodule:: abjad.tools.documentationtools

ReSTHeading
===========

.. autoclass:: ReSTHeading

Lineage
-------

.. container:: graphviz

   .. graphviz::

      digraph InheritanceGraph {
          graph [background=transparent,
              bgcolor=transparent,
              color=lightslategrey,
              fontname=Arial,
              outputorder=edgesfirst,
              overlap=prism,
              penwidth=2,
              rankdir=LR,
              root="__builtin__.object",
              splines=spline,
              style="dotted, rounded",
              truecolor=true];
          node [colorscheme=pastel19,
              fontname=Arial,
              fontsize=12,
              penwidth=2,
              style="filled, rounded"];
          edge [color=lightsteelblue2,
              penwidth=2];
          subgraph cluster_abctools {
              graph [label=abctools];
              "abjad.tools.abctools.AbjadObject.AbjadObject" [color=1,
                  group=0,
                  label=AbjadObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbstractBase" [color=1,
                  group=0,
                  label=AbstractBase,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=3,
                  group=2,
                  label=TreeNode,
                  shape=box];
          }
          subgraph cluster_documentationtools {
              graph [label=documentationtools];
              "abjad.tools.documentationtools.ReSTHeading.ReSTHeading" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>ReSTHeading</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.ReSTHeading.ReSTHeading";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TreeNode`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.depth
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.depthwise_inventory
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.graph_order
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.heading_characters
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.improper_parentage
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.level
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.name
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.parent
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.proper_parentage
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.rest_format
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.root
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.text
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.__copy__
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.__eq__
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.__format__
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.__hash__
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.__ne__
      ~abjad.tools.documentationtools.ReSTHeading.ReSTHeading.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.graph_order

.. autoattribute:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.heading_characters

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.proper_parentage

.. autoattribute:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.rest_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.root

Read/write properties
---------------------

.. autoattribute:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.level

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.name

.. autoattribute:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.text

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTHeading.ReSTHeading.__repr__
