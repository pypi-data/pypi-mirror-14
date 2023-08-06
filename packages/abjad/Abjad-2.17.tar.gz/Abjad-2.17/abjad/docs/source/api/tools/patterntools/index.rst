patterntools
============

.. automodule:: abjad.tools.patterntools

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" [color=3,
                  group=2,
                  label=TypedTuple,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedTuple.TypedTuple";
          }
          subgraph cluster_patterntools {
              graph [label=patterntools];
              "abjad.tools.patterntools.CompoundPattern.CompoundPattern" [color=black,
                  fontcolor=white,
                  group=3,
                  label=CompoundPattern,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.patterntools.Pattern.Pattern" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Pattern,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.patterntools.PatternInventory.PatternInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PatternInventory,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.patterntools.Pattern.Pattern";
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.patterntools.CompoundPattern.CompoundPattern";
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.patterntools.PatternInventory.PatternInventory";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   CompoundPattern
   Pattern
   PatternInventory

.. autosummary::
   :nosignatures:

   CompoundPattern
   Pattern
   PatternInventory

--------

Functions
---------

.. toctree::
   :hidden:

   select
   select_all
   select_every
   select_first
   select_last

.. autosummary::
   :nosignatures:

   select
   select_all
   select_every
   select_first
   select_last
