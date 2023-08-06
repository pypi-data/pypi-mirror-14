schemetools
===========

.. automodule:: abjad.tools.schemetools

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
          subgraph cluster_schemetools {
              graph [label=schemetools];
              "abjad.tools.schemetools.Scheme.Scheme" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Scheme,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.schemetools.SchemeAssociativeList.SchemeAssociativeList" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SchemeAssociativeList,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.schemetools.SchemeColor.SchemeColor" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SchemeColor,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.schemetools.SchemeMoment.SchemeMoment" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SchemeMoment,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.schemetools.SchemePair.SchemePair" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SchemePair,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.schemetools.SchemeSymbol.SchemeSymbol" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SchemeSymbol,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.schemetools.SchemeVector.SchemeVector" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SchemeVector,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.schemetools.SchemeVectorConstant.SchemeVectorConstant" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SchemeVectorConstant,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeAssociativeList.SchemeAssociativeList";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeColor.SchemeColor";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeMoment.SchemeMoment";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemePair.SchemePair";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeSymbol.SchemeSymbol";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeVector.SchemeVector";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeVectorConstant.SchemeVectorConstant";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.schemetools.Scheme.Scheme";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   Scheme
   SchemeAssociativeList
   SchemeColor
   SchemeMoment
   SchemePair
   SchemeSymbol
   SchemeVector
   SchemeVectorConstant

.. autosummary::
   :nosignatures:

   Scheme
   SchemeAssociativeList
   SchemeColor
   SchemeMoment
   SchemePair
   SchemeSymbol
   SchemeVector
   SchemeVectorConstant

--------

Functions
---------

.. toctree::
   :hidden:

   make_spacing_vector

.. autosummary::
   :nosignatures:

   make_spacing_vector
