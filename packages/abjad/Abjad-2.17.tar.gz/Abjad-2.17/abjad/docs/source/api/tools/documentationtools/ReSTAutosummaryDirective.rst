.. currentmodule:: abjad.tools.documentationtools

ReSTAutosummaryDirective
========================

.. autoclass:: ReSTAutosummaryDirective

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
              "abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>ReSTAutosummaryDirective</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" [color=4,
                  group=3,
                  label=ReSTDirective,
                  shape=box];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective";
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

      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.append
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.argument
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.children
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.depth
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.depthwise_inventory
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.directive
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.extend
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.graph_order
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.improper_parentage
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.index
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.insert
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.leaves
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.name
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.node_class
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.nodes
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.options
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.parent
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.pop
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.proper_parentage
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.remove
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.rest_format
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.root
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__contains__
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__copy__
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__delitem__
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__eq__
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__format__
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__getitem__
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__hash__
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__iter__
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__len__
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__ne__
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__repr__
      ~abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.depthwise_inventory

.. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.directive

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.leaves

.. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.node_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.options

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.rest_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.argument

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__repr__

.. automethod:: abjad.tools.documentationtools.ReSTAutosummaryDirective.ReSTAutosummaryDirective.__setitem__
