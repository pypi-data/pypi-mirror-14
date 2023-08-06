rhythmtreetools
===============

.. automodule:: abjad.tools.rhythmtreetools

--------

Lineage
-------

.. container:: graphviz

   .. graphviz::

      digraph InheritanceGraph {
          graph [bgcolor=transparent,
              color=lightslategrey,
              dpi=72,
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
              "abjad.tools.abctools.Parser.Parser" [color=1,
                  group=0,
                  label=Parser,
                  shape=oval,
                  style=bold];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.Parser.Parser";
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
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.QGridContainer.QGridContainer" [color=4,
                  group=3,
                  label=QGridContainer,
                  shape=box];
              "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf" [color=4,
                  group=3,
                  label=QGridLeaf,
                  shape=box];
          }
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" [color=black,
                  fontcolor=white,
                  group=4,
                  label=RhythmTreeContainer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf" [color=black,
                  fontcolor=white,
                  group=4,
                  label=RhythmTreeLeaf,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" [color=black,
                  fontcolor=white,
                  group=4,
                  label=RhythmTreeMixin,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser" [color=black,
                  fontcolor=white,
                  group=4,
                  label=RhythmTreeParser,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer";
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser";
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf";
          "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" -> "abjad.tools.quantizationtools.QGridContainer.QGridContainer";
          "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Abstract Classes
----------------

.. toctree::
   :hidden:

   RhythmTreeMixin

.. autosummary::
   :nosignatures:

   RhythmTreeMixin

--------

Classes
-------

.. toctree::
   :hidden:

   RhythmTreeContainer
   RhythmTreeLeaf
   RhythmTreeParser

.. autosummary::
   :nosignatures:

   RhythmTreeContainer
   RhythmTreeLeaf
   RhythmTreeParser

--------

Functions
---------

.. toctree::
   :hidden:

   parse_rtm_syntax

.. autosummary::
   :nosignatures:

   parse_rtm_syntax
