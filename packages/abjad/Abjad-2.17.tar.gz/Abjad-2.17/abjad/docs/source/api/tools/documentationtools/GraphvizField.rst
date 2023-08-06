.. currentmodule:: abjad.tools.documentationtools

GraphvizField
=============

.. autoclass:: GraphvizField

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
              "abjad.tools.documentationtools.GraphvizField.GraphvizField" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>GraphvizField</B>>,
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
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.documentationtools.GraphvizField.GraphvizField";
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

      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.canonical_name
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.depth
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.depthwise_inventory
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.edges
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.field_name
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.graph_order
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.improper_parentage
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.label
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.name
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.parent
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.proper_parentage
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.root
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.struct
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.__copy__
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.__eq__
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.__format__
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.__hash__
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.__ne__
      ~abjad.tools.documentationtools.GraphvizField.GraphvizField.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.documentationtools.GraphvizField.GraphvizField.canonical_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizField.GraphvizField.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizField.GraphvizField.depthwise_inventory

.. autoattribute:: abjad.tools.documentationtools.GraphvizField.GraphvizField.edges

.. autoattribute:: abjad.tools.documentationtools.GraphvizField.GraphvizField.field_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizField.GraphvizField.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizField.GraphvizField.improper_parentage

.. autoattribute:: abjad.tools.documentationtools.GraphvizField.GraphvizField.label

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizField.GraphvizField.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizField.GraphvizField.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizField.GraphvizField.root

.. autoattribute:: abjad.tools.documentationtools.GraphvizField.GraphvizField.struct

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.documentationtools.GraphvizField.GraphvizField.name

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizField.GraphvizField.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizField.GraphvizField.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizField.GraphvizField.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizField.GraphvizField.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizField.GraphvizField.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.GraphvizField.GraphvizField.__repr__
