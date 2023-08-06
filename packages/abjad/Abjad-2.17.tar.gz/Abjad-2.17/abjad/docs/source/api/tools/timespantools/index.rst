timespantools
=============

.. automodule:: abjad.tools.timespantools

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
          subgraph cluster_mathtools {
              graph [label=mathtools];
              "abjad.tools.mathtools.BoundedObject.BoundedObject" [color=4,
                  group=3,
                  label=BoundedObject,
                  shape=box];
          }
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan" [color=black,
                  fontcolor=white,
                  group=4,
                  label=AnnotatedTimespan,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.timespantools.CompoundInequality.CompoundInequality" [color=black,
                  fontcolor=white,
                  group=4,
                  label=CompoundInequality,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.timespantools.Inequality.Inequality" [color=black,
                  fontcolor=white,
                  group=4,
                  label=Inequality,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation" [color=black,
                  fontcolor=white,
                  group=4,
                  label=OffsetTimespanTimeRelation,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.timespantools.TimeRelation.TimeRelation" [color=black,
                  fontcolor=white,
                  group=4,
                  label=TimeRelation,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.timespantools.Timespan.Timespan" [color=black,
                  fontcolor=white,
                  group=4,
                  label=Timespan,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.timespantools.TimespanInventory.TimespanInventory" [color=black,
                  fontcolor=white,
                  group=4,
                  label=TimespanInventory,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation" [color=black,
                  fontcolor=white,
                  group=4,
                  label=TimespanTimespanTimeRelation,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.timespantools.TimeRelation.TimeRelation" -> "abjad.tools.timespantools.OffsetTimespanTimeRelation.OffsetTimespanTimeRelation";
              "abjad.tools.timespantools.TimeRelation.TimeRelation" -> "abjad.tools.timespantools.TimespanTimespanTimeRelation.TimespanTimespanTimeRelation";
              "abjad.tools.timespantools.Timespan.Timespan" -> "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.BoundedObject.BoundedObject";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.timespantools.Inequality.Inequality";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.timespantools.TimeRelation.TimeRelation";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.timespantools.CompoundInequality.CompoundInequality";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.timespantools.TimespanInventory.TimespanInventory";
          "abjad.tools.mathtools.BoundedObject.BoundedObject" -> "abjad.tools.timespantools.Timespan.Timespan";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Time relations
--------------

.. toctree::
   :hidden:

   CompoundInequality
   Inequality
   OffsetTimespanTimeRelation
   TimeRelation
   TimespanTimespanTimeRelation

.. autosummary::
   :nosignatures:

   CompoundInequality
   Inequality
   OffsetTimespanTimeRelation
   TimeRelation
   TimespanTimespanTimeRelation

--------

Timespans
---------

.. toctree::
   :hidden:

   AnnotatedTimespan
   Timespan
   TimespanInventory

.. autosummary::
   :nosignatures:

   AnnotatedTimespan
   Timespan
   TimespanInventory

--------

Functions
---------

.. toctree::
   :hidden:

   offset_happens_after_timespan_starts
   offset_happens_after_timespan_stops
   offset_happens_before_timespan_starts
   offset_happens_before_timespan_stops
   offset_happens_during_timespan
   offset_happens_when_timespan_starts
   offset_happens_when_timespan_stops
   timespan_2_contains_timespan_1_improperly
   timespan_2_curtails_timespan_1
   timespan_2_delays_timespan_1
   timespan_2_happens_during_timespan_1
   timespan_2_intersects_timespan_1
   timespan_2_is_congruent_to_timespan_1
   timespan_2_overlaps_all_of_timespan_1
   timespan_2_overlaps_only_start_of_timespan_1
   timespan_2_overlaps_only_stop_of_timespan_1
   timespan_2_overlaps_start_of_timespan_1
   timespan_2_overlaps_stop_of_timespan_1
   timespan_2_starts_after_timespan_1_starts
   timespan_2_starts_after_timespan_1_stops
   timespan_2_starts_before_timespan_1_starts
   timespan_2_starts_before_timespan_1_stops
   timespan_2_starts_during_timespan_1
   timespan_2_starts_when_timespan_1_starts
   timespan_2_starts_when_timespan_1_stops
   timespan_2_stops_after_timespan_1_starts
   timespan_2_stops_after_timespan_1_stops
   timespan_2_stops_before_timespan_1_starts
   timespan_2_stops_before_timespan_1_stops
   timespan_2_stops_during_timespan_1
   timespan_2_stops_when_timespan_1_starts
   timespan_2_stops_when_timespan_1_stops
   timespan_2_trisects_timespan_1

.. autosummary::
   :nosignatures:

   offset_happens_after_timespan_starts
   offset_happens_after_timespan_stops
   offset_happens_before_timespan_starts
   offset_happens_before_timespan_stops
   offset_happens_during_timespan
   offset_happens_when_timespan_starts
   offset_happens_when_timespan_stops
   timespan_2_contains_timespan_1_improperly
   timespan_2_curtails_timespan_1
   timespan_2_delays_timespan_1
   timespan_2_happens_during_timespan_1
   timespan_2_intersects_timespan_1
   timespan_2_is_congruent_to_timespan_1
   timespan_2_overlaps_all_of_timespan_1
   timespan_2_overlaps_only_start_of_timespan_1
   timespan_2_overlaps_only_stop_of_timespan_1
   timespan_2_overlaps_start_of_timespan_1
   timespan_2_overlaps_stop_of_timespan_1
   timespan_2_starts_after_timespan_1_starts
   timespan_2_starts_after_timespan_1_stops
   timespan_2_starts_before_timespan_1_starts
   timespan_2_starts_before_timespan_1_stops
   timespan_2_starts_during_timespan_1
   timespan_2_starts_when_timespan_1_starts
   timespan_2_starts_when_timespan_1_stops
   timespan_2_stops_after_timespan_1_starts
   timespan_2_stops_after_timespan_1_stops
   timespan_2_stops_before_timespan_1_starts
   timespan_2_stops_before_timespan_1_stops
   timespan_2_stops_during_timespan_1
   timespan_2_stops_when_timespan_1_starts
   timespan_2_stops_when_timespan_1_stops
   timespan_2_trisects_timespan_1
