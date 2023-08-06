selectortools
=============

.. automodule:: abjad.tools.selectortools

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
          subgraph cluster_selectortools {
              graph [label=selectortools];
              "abjad.tools.selectortools.ContiguitySelectorCallback.ContiguitySelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=ContiguitySelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.CountsSelectorCallback.CountsSelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=CountsSelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.DurationInequality.DurationInequality" [color=black,
                  fontcolor=white,
                  group=2,
                  label=DurationInequality,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.DurationSelectorCallback.DurationSelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=DurationSelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.ExtraLeafSelectorCallback.ExtraLeafSelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=ExtraLeafSelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.FlattenSelectorCallback.FlattenSelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=FlattenSelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.Inequality.Inequality" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Inequality,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.selectortools.ItemSelectorCallback.ItemSelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=ItemSelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.LengthInequality.LengthInequality" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LengthInequality,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.LengthSelectorCallback.LengthSelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LengthSelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.LogicalMeasureSelectorCallback.LogicalMeasureSelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LogicalMeasureSelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.LogicalTieSelectorCallback.LogicalTieSelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LogicalTieSelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.PartitionByRatioCallback.PartitionByRatioCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=PartitionByRatioCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.PatternedSelectorCallback.PatternedSelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=PatternedSelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.PitchSelectorCallback.PitchSelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=PitchSelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.PrototypeSelectorCallback.PrototypeSelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=PrototypeSelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.RunSelectorCallback.RunSelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=RunSelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.Selector.Selector" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Selector,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.SliceSelectorCallback.SliceSelectorCallback" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SliceSelectorCallback,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.selectortools.Inequality.Inequality" -> "abjad.tools.selectortools.DurationInequality.DurationInequality";
              "abjad.tools.selectortools.Inequality.Inequality" -> "abjad.tools.selectortools.LengthInequality.LengthInequality";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.ContiguitySelectorCallback.ContiguitySelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.CountsSelectorCallback.CountsSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.DurationSelectorCallback.DurationSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.ExtraLeafSelectorCallback.ExtraLeafSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.FlattenSelectorCallback.FlattenSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.Inequality.Inequality";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.ItemSelectorCallback.ItemSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.LengthSelectorCallback.LengthSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.LogicalMeasureSelectorCallback.LogicalMeasureSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.LogicalTieSelectorCallback.LogicalTieSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.PartitionByRatioCallback.PartitionByRatioCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.PatternedSelectorCallback.PatternedSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.PitchSelectorCallback.PitchSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.PrototypeSelectorCallback.PrototypeSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.RunSelectorCallback.RunSelectorCallback";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.Selector.Selector";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.SliceSelectorCallback.SliceSelectorCallback";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Callbacks
---------

.. toctree::
   :hidden:

   ContiguitySelectorCallback
   CountsSelectorCallback
   DurationSelectorCallback
   ExtraLeafSelectorCallback
   FlattenSelectorCallback
   ItemSelectorCallback
   LengthSelectorCallback
   LogicalMeasureSelectorCallback
   LogicalTieSelectorCallback
   PartitionByRatioCallback
   PatternedSelectorCallback
   PitchSelectorCallback
   PrototypeSelectorCallback
   RunSelectorCallback
   SliceSelectorCallback

.. autosummary::
   :nosignatures:

   ContiguitySelectorCallback
   CountsSelectorCallback
   DurationSelectorCallback
   ExtraLeafSelectorCallback
   FlattenSelectorCallback
   ItemSelectorCallback
   LengthSelectorCallback
   LogicalMeasureSelectorCallback
   LogicalTieSelectorCallback
   PartitionByRatioCallback
   PatternedSelectorCallback
   PitchSelectorCallback
   PrototypeSelectorCallback
   RunSelectorCallback
   SliceSelectorCallback

--------

Inequalities
------------

.. toctree::
   :hidden:

   DurationInequality
   Inequality
   LengthInequality

.. autosummary::
   :nosignatures:

   DurationInequality
   Inequality
   LengthInequality

--------

Selectors
---------

.. toctree::
   :hidden:

   Selector

.. autosummary::
   :nosignatures:

   Selector

--------

Functions
---------

.. toctree::
   :hidden:

   select_all_but_first_logical_tie_in_pitched_runs
   select_all_but_last_logical_tie_in_pitched_runs
   select_first_logical_tie_in_pitched_runs
   select_last_logical_tie_in_pitched_runs
   select_pitched_runs

.. autosummary::
   :nosignatures:

   select_all_but_first_logical_tie_in_pitched_runs
   select_all_but_last_logical_tie_in_pitched_runs
   select_first_logical_tie_in_pitched_runs
   select_last_logical_tie_in_pitched_runs
   select_pitched_runs
