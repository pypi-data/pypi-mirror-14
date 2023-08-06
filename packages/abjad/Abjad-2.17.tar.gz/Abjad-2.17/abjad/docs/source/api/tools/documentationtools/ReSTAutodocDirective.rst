.. currentmodule:: abjad.tools.documentationtools

ReSTAutodocDirective
====================

.. autoclass:: ReSTAutodocDirective

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
              "abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>ReSTAutodocDirective</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" [color=4,
                  group=3,
                  label=ReSTDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.documentationtools.ReSTDirective.ReSTDirective";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.documentationtools.ReSTDirective`

- :py:class:`abjad.tools.datastructuretools.TreeContainer`

- :py:class:`abjad.tools.datastructuretools.TreeNode`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.append
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.argument
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.children
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.depth
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.depthwise_inventory
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.directive
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.extend
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.graph_order
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.improper_parentage
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.index
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.insert
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.leaves
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.name
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.node_class
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.nodes
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.options
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.parent
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.pop
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.proper_parentage
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.remove
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.rest_format
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.root
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__contains__
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__copy__
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__delitem__
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__eq__
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__format__
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__getitem__
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__hash__
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__iter__
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__len__
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__ne__
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__repr__
      ~abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.leaves

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.node_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.options

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.rest_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.argument

.. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.directive

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutodocDirective.ReSTAutodocDirective.__setitem__
