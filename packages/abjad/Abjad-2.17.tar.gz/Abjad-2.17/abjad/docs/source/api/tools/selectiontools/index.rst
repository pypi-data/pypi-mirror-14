selectiontools
==============

.. automodule:: abjad.tools.selectiontools

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
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=3,
                  group=2,
                  label=TypedList,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
          }
          subgraph cluster_selectiontools {
              graph [label=selectiontools];
              "abjad.tools.selectiontools.Descendants.Descendants" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Descendants,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.Lineage.Lineage" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Lineage,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.LogicalTie.LogicalTie" [color=black,
                  fontcolor=white,
                  group=3,
                  label=LogicalTie,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.Parentage.Parentage" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Parentage,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.Selection.Selection" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Selection,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.SelectionInventory.SelectionInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=SelectionInventory,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.VerticalMoment.VerticalMoment" [color=black,
                  fontcolor=white,
                  group=3,
                  label=VerticalMoment,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.Descendants.Descendants";
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.Lineage.Lineage";
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.LogicalTie.LogicalTie";
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.Parentage.Parentage";
              "abjad.tools.selectiontools.Selection.Selection" -> "abjad.tools.selectiontools.VerticalMoment.VerticalMoment";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.selectiontools.SelectionInventory.SelectionInventory";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.object" -> "abjad.tools.selectiontools.Selection.Selection";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   Descendants
   Lineage
   LogicalTie
   Parentage
   Selection
   SelectionInventory
   VerticalMoment

.. autosummary::
   :nosignatures:

   Descendants
   Lineage
   LogicalTie
   Parentage
   Selection
   SelectionInventory
   VerticalMoment
