.. currentmodule:: abjad.tools.documentationtools

ReSTInheritanceDiagram
======================

.. autoclass:: ReSTInheritanceDiagram

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
              "abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>ReSTInheritanceDiagram</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram";
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

      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.append
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.argument
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.children
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.depth
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.depthwise_inventory
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.directive
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.extend
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.graph_order
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.improper_parentage
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.index
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.insert
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.leaves
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.name
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.node_class
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.nodes
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.options
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.parent
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.pop
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.proper_parentage
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.remove
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.rest_format
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.root
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__contains__
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__copy__
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__delitem__
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__eq__
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__format__
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__getitem__
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__hash__
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__iter__
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__len__
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__ne__
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__repr__
      ~abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.depthwise_inventory

.. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.directive

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.leaves

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.node_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.options

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.rest_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.argument

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTInheritanceDiagram.ReSTInheritanceDiagram.__setitem__
