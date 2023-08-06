.. currentmodule:: abjad.tools.quantizationtools

WeightedSearchTree
==================

.. autoclass:: WeightedSearchTree

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
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.SearchTree.SearchTree" [color=3,
                  group=2,
                  label=SearchTree,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>WeightedSearchTree</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.SearchTree.SearchTree" -> "abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.SearchTree.SearchTree";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.quantizationtools.SearchTree`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.all_compositions
      ~abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.default_definition
      ~abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.definition
      ~abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.__call__
      ~abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.__eq__
      ~abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.__format__
      ~abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.__hash__
      ~abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.__ne__
      ~abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.all_compositions

.. autoattribute:: abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.default_definition

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.definition

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree.__repr__
