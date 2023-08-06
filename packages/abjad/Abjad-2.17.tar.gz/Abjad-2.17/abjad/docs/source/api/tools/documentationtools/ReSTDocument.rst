.. currentmodule:: abjad.tools.documentationtools

ReSTDocument
============

.. autoclass:: ReSTDocument

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
              "abjad.tools.datastructuretools.TreeContainer.TreeContainer" [color=3,
                  group=2,
                  label=TreeContainer,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=3,
                  group=2,
                  label=TreeNode,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.datastructuretools.TreeContainer.TreeContainer";
          }
          subgraph cluster_documentationtools {
              graph [label=documentationtools];
              "abjad.tools.documentationtools.ReSTDocument.ReSTDocument" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>ReSTDocument</B>>,
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
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.ReSTDocument.ReSTDocument";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TreeContainer`

- :py:class:`abjad.tools.datastructuretools.TreeNode`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.append
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.children
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.depth
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.depthwise_inventory
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.extend
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.graph_order
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.improper_parentage
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.index
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.insert
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.leaves
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.name
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.node_class
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.nodes
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.parent
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.pop
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.proper_parentage
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.remove
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.rest_format
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.root
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__contains__
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__copy__
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__delitem__
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__eq__
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__format__
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__getitem__
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__hash__
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__iter__
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__len__
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__ne__
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__repr__
      ~abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.leaves

.. autoattribute:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.node_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.proper_parentage

.. autoattribute:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.rest_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTDocument.ReSTDocument.__setitem__
