.. currentmodule:: abjad.tools.quantizationtools

SearchTree
==========

.. autoclass:: SearchTree

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
              "abjad.tools.quantizationtools.SearchTree.SearchTree" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>SearchTree</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.UnweightedSearchTree.UnweightedSearchTree" [color=3,
                  group=2,
                  label=UnweightedSearchTree,
                  shape=box];
              "abjad.tools.quantizationtools.WeightedSearchTree.WeightedSearchTree" [color=3,
                  group=2,
                  label=WeightedSearchTree,
                  shape=box];
              "abjad.tools.quantizationtools.SearchTree.SearchTree" -> "abjad.tools.quantizationtools.UnweightedSearchTree.UnweightedSearchTree";
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

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.quantizationtools.SearchTree.SearchTree.default_definition
      ~abjad.tools.quantizationtools.SearchTree.SearchTree.definition
      ~abjad.tools.quantizationtools.SearchTree.SearchTree.__call__
      ~abjad.tools.quantizationtools.SearchTree.SearchTree.__eq__
      ~abjad.tools.quantizationtools.SearchTree.SearchTree.__format__
      ~abjad.tools.quantizationtools.SearchTree.SearchTree.__hash__
      ~abjad.tools.quantizationtools.SearchTree.SearchTree.__ne__
      ~abjad.tools.quantizationtools.SearchTree.SearchTree.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.quantizationtools.SearchTree.SearchTree.default_definition

.. autoattribute:: abjad.tools.quantizationtools.SearchTree.SearchTree.definition

Special methods
---------------

.. automethod:: abjad.tools.quantizationtools.SearchTree.SearchTree.__call__

.. automethod:: abjad.tools.quantizationtools.SearchTree.SearchTree.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.SearchTree.SearchTree.__format__

.. automethod:: abjad.tools.quantizationtools.SearchTree.SearchTree.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.SearchTree.SearchTree.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.SearchTree.SearchTree.__repr__
