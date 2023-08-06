.. currentmodule:: abjad.tools.documentationtools

ReSTTOCDirective
================

.. autoclass:: ReSTTOCDirective

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
              "abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>ReSTTOCDirective</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.documentationtools.ReSTDirective.ReSTDirective" -> "abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective";
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

      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.append
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.argument
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.children
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.depth
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.depthwise_inventory
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.directive
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.extend
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.graph_order
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.improper_parentage
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.index
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.insert
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.leaves
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.name
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.node_class
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.nodes
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.options
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.parent
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.pop
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.proper_parentage
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.remove
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.rest_format
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.root
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__contains__
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__copy__
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__delitem__
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__eq__
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__format__
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__getitem__
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__hash__
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__iter__
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__len__
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__ne__
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__repr__
      ~abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.depthwise_inventory

.. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.directive

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.leaves

.. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.node_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.options

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.rest_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.root

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.argument

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__repr__

.. automethod:: abjad.tools.documentationtools.ReSTTOCDirective.ReSTTOCDirective.__setitem__
