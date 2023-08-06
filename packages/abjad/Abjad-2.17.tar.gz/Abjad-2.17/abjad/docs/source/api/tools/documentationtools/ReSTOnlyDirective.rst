.. currentmodule:: abjad.tools.documentationtools

ReSTOnlyDirective
=================

.. autoclass:: ReSTOnlyDirective

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
              "abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>ReSTOnlyDirective</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective";
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

      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.append
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.argument
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.children
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.depth
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.depthwise_inventory
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.directive
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.extend
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.graph_order
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.improper_parentage
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.index
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.insert
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.leaves
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.name
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.node_class
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.nodes
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.options
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.parent
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.pop
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.proper_parentage
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.remove
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.rest_format
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.root
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__contains__
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__copy__
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__delitem__
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__eq__
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__format__
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__getitem__
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__hash__
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__iter__
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__len__
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__ne__
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__repr__
      ~abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.depthwise_inventory

.. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.directive

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.leaves

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.node_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.options

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.rest_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.argument

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTOnlyDirective.ReSTOnlyDirective.__setitem__
