markuptools
===========

.. automodule:: abjad.tools.markuptools

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
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=3,
                  group=2,
                  label=TypedList,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
          }
          subgraph cluster_markuptools {
              graph [label=markuptools];
              "abjad.tools.markuptools.Markup.Markup" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Markup,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.markuptools.MarkupCommand.MarkupCommand" [color=black,
                  fontcolor=white,
                  group=3,
                  label=MarkupCommand,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.markuptools.MarkupInventory.MarkupInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=MarkupInventory,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.markuptools.Postscript.Postscript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Postscript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.markuptools.PostscriptOperator.PostscriptOperator" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PostscriptOperator,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.Markup.Markup";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.MarkupCommand.MarkupCommand";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.Postscript.Postscript";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.PostscriptOperator.PostscriptOperator";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.markuptools.MarkupInventory.MarkupInventory";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   Markup
   MarkupCommand
   MarkupInventory
   Postscript
   PostscriptOperator

.. autosummary::
   :nosignatures:

   Markup
   MarkupCommand
   MarkupInventory
   Postscript
   PostscriptOperator
