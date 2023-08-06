lilypondnametools
=================

.. automodule:: abjad.tools.lilypondnametools

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
          subgraph cluster_lilypondnametools {
              graph [label=lilypondnametools];
              "abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondContext,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondContextSetting,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondEngraver,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondGrob,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondGrobInterface,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondnametools.LilyPondGrobNameManager.LilyPondGrobNameManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondGrobNameManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondGrobOverride,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondNameManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondnametools.LilyPondSettingNameManager.LilyPondSettingNameManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondSettingNameManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" -> "abjad.tools.lilypondnametools.LilyPondGrobNameManager.LilyPondGrobNameManager";
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" -> "abjad.tools.lilypondnametools.LilyPondSettingNameManager.LilyPondSettingNameManager";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   LilyPondContext
   LilyPondContextSetting
   LilyPondEngraver
   LilyPondGrob
   LilyPondGrobInterface
   LilyPondGrobNameManager
   LilyPondGrobOverride
   LilyPondNameManager
   LilyPondSettingNameManager

.. autosummary::
   :nosignatures:

   LilyPondContext
   LilyPondContextSetting
   LilyPondEngraver
   LilyPondGrob
   LilyPondGrobInterface
   LilyPondGrobNameManager
   LilyPondGrobOverride
   LilyPondNameManager
   LilyPondSettingNameManager
