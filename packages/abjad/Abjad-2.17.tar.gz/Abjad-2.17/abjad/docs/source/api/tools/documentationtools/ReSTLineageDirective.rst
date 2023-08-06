.. currentmodule:: abjad.tools.documentationtools

ReSTLineageDirective
====================

.. autoclass:: ReSTLineageDirective

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
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" [color=4,
                  group=3,
                  label=ReSTDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>ReSTLineageDirective</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective";
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

      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.append
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.argument
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.children
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.depth
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.depthwise_inventory
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.directive
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.extend
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.graph_order
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.improper_parentage
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.index
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.insert
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.leaves
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.name
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.node_class
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.nodes
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.options
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.parent
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.pop
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.proper_parentage
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.remove
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.rest_format
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.root
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__contains__
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__copy__
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__delitem__
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__eq__
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__format__
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__getitem__
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__hash__
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__iter__
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__len__
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__ne__
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__repr__
      ~abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.depthwise_inventory

.. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.directive

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.leaves

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.node_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.options

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.rest_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.argument

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTLineageDirective.ReSTLineageDirective.__setitem__
