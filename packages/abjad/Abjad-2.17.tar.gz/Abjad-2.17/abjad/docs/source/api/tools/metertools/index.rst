metertools
==========

.. automodule:: abjad.tools.metertools

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
              "abjad.tools.datastructuretools.TypedCounter.TypedCounter" [color=3,
                  group=2,
                  label=TypedCounter,
                  shape=box];
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=3,
                  group=2,
                  label=TypedList,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedCounter.TypedCounter";
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
          }
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.Meter.Meter" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Meter,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.metertools.MeterFittingSession.MeterFittingSession" [color=black,
                  fontcolor=white,
                  group=3,
                  label=MeterFittingSession,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.metertools.MeterInventory.MeterInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=MeterInventory,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.metertools.MeterManager.MeterManager" [color=black,
                  fontcolor=white,
                  group=3,
                  label=MeterManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel" [color=black,
                  fontcolor=white,
                  group=3,
                  label=MetricAccentKernel,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.metertools.OffsetCounter.OffsetCounter" [color=black,
                  fontcolor=white,
                  group=3,
                  label=OffsetCounter,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.metertools.Meter.Meter";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.metertools.MeterManager.MeterManager";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.metertools.MeterFittingSession.MeterFittingSession";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel";
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.metertools.OffsetCounter.OffsetCounter";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.metertools.MeterInventory.MeterInventory";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   Meter
   MeterFittingSession
   MeterInventory
   MeterManager
   MetricAccentKernel
   OffsetCounter

.. autosummary::
   :nosignatures:

   Meter
   MeterFittingSession
   MeterInventory
   MeterManager
   MetricAccentKernel
   OffsetCounter
