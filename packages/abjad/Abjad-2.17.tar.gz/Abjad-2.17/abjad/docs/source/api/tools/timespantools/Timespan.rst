.. currentmodule:: abjad.tools.timespantools

Timespan
========

.. autoclass:: Timespan

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
          subgraph cluster_mathtools {
              graph [label=mathtools];
              "abjad.tools.mathtools.BoundedObject.BoundedObject" [color=3,
                  group=2,
                  label=BoundedObject,
                  shape=box];
          }
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan" [color=4,
                  group=3,
                  label=AnnotatedTimespan,
                  shape=box];
              "abjad.tools.timespantools.Timespan.Timespan" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>Timespan</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.timespantools.Timespan.Timespan" -> "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.BoundedObject.BoundedObject";
          "abjad.tools.mathtools.BoundedObject.BoundedObject" -> "abjad.tools.timespantools.Timespan.Timespan";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.mathtools.BoundedObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.timespantools.Timespan.Timespan.axis
      ~abjad.tools.timespantools.Timespan.Timespan.contains_timespan_improperly
      ~abjad.tools.timespantools.Timespan.Timespan.curtails_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.delays_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.divide_by_ratio
      ~abjad.tools.timespantools.Timespan.Timespan.duration
      ~abjad.tools.timespantools.Timespan.Timespan.get_overlap_with_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.happens_during_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.intersects_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.is_closed
      ~abjad.tools.timespantools.Timespan.Timespan.is_congruent_to_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.is_half_closed
      ~abjad.tools.timespantools.Timespan.Timespan.is_half_open
      ~abjad.tools.timespantools.Timespan.Timespan.is_left_closed
      ~abjad.tools.timespantools.Timespan.Timespan.is_left_open
      ~abjad.tools.timespantools.Timespan.Timespan.is_open
      ~abjad.tools.timespantools.Timespan.Timespan.is_right_closed
      ~abjad.tools.timespantools.Timespan.Timespan.is_right_open
      ~abjad.tools.timespantools.Timespan.Timespan.is_tangent_to_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.is_well_formed
      ~abjad.tools.timespantools.Timespan.Timespan.offsets
      ~abjad.tools.timespantools.Timespan.Timespan.overlaps_all_of_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.overlaps_only_start_of_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.overlaps_only_stop_of_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.overlaps_start_of_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.overlaps_stop_of_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.reflect
      ~abjad.tools.timespantools.Timespan.Timespan.round_offsets
      ~abjad.tools.timespantools.Timespan.Timespan.scale
      ~abjad.tools.timespantools.Timespan.Timespan.set_duration
      ~abjad.tools.timespantools.Timespan.Timespan.set_offsets
      ~abjad.tools.timespantools.Timespan.Timespan.split_at_offset
      ~abjad.tools.timespantools.Timespan.Timespan.split_at_offsets
      ~abjad.tools.timespantools.Timespan.Timespan.start_offset
      ~abjad.tools.timespantools.Timespan.Timespan.starts_after_offset
      ~abjad.tools.timespantools.Timespan.Timespan.starts_after_timespan_starts
      ~abjad.tools.timespantools.Timespan.Timespan.starts_after_timespan_stops
      ~abjad.tools.timespantools.Timespan.Timespan.starts_at_offset
      ~abjad.tools.timespantools.Timespan.Timespan.starts_at_or_after_offset
      ~abjad.tools.timespantools.Timespan.Timespan.starts_before_offset
      ~abjad.tools.timespantools.Timespan.Timespan.starts_before_or_at_offset
      ~abjad.tools.timespantools.Timespan.Timespan.starts_before_timespan_starts
      ~abjad.tools.timespantools.Timespan.Timespan.starts_before_timespan_stops
      ~abjad.tools.timespantools.Timespan.Timespan.starts_during_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.starts_when_timespan_starts
      ~abjad.tools.timespantools.Timespan.Timespan.starts_when_timespan_stops
      ~abjad.tools.timespantools.Timespan.Timespan.stop_offset
      ~abjad.tools.timespantools.Timespan.Timespan.stops_after_offset
      ~abjad.tools.timespantools.Timespan.Timespan.stops_after_timespan_starts
      ~abjad.tools.timespantools.Timespan.Timespan.stops_after_timespan_stops
      ~abjad.tools.timespantools.Timespan.Timespan.stops_at_offset
      ~abjad.tools.timespantools.Timespan.Timespan.stops_at_or_after_offset
      ~abjad.tools.timespantools.Timespan.Timespan.stops_before_offset
      ~abjad.tools.timespantools.Timespan.Timespan.stops_before_or_at_offset
      ~abjad.tools.timespantools.Timespan.Timespan.stops_before_timespan_starts
      ~abjad.tools.timespantools.Timespan.Timespan.stops_before_timespan_stops
      ~abjad.tools.timespantools.Timespan.Timespan.stops_during_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.stops_when_timespan_starts
      ~abjad.tools.timespantools.Timespan.Timespan.stops_when_timespan_stops
      ~abjad.tools.timespantools.Timespan.Timespan.stretch
      ~abjad.tools.timespantools.Timespan.Timespan.translate
      ~abjad.tools.timespantools.Timespan.Timespan.translate_offsets
      ~abjad.tools.timespantools.Timespan.Timespan.trisects_timespan
      ~abjad.tools.timespantools.Timespan.Timespan.__and__
      ~abjad.tools.timespantools.Timespan.Timespan.__eq__
      ~abjad.tools.timespantools.Timespan.Timespan.__format__
      ~abjad.tools.timespantools.Timespan.Timespan.__ge__
      ~abjad.tools.timespantools.Timespan.Timespan.__gt__
      ~abjad.tools.timespantools.Timespan.Timespan.__hash__
      ~abjad.tools.timespantools.Timespan.Timespan.__illustrate__
      ~abjad.tools.timespantools.Timespan.Timespan.__le__
      ~abjad.tools.timespantools.Timespan.Timespan.__len__
      ~abjad.tools.timespantools.Timespan.Timespan.__lt__
      ~abjad.tools.timespantools.Timespan.Timespan.__ne__
      ~abjad.tools.timespantools.Timespan.Timespan.__or__
      ~abjad.tools.timespantools.Timespan.Timespan.__repr__
      ~abjad.tools.timespantools.Timespan.Timespan.__sub__
      ~abjad.tools.timespantools.Timespan.Timespan.__xor__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.axis

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.duration

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.is_closed

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.is_half_closed

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.is_half_open

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.is_left_closed

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.is_left_open

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.is_open

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.is_right_closed

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.is_right_open

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.is_well_formed

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.offsets

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.start_offset

.. autoattribute:: abjad.tools.timespantools.Timespan.Timespan.stop_offset

Methods
-------

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.contains_timespan_improperly

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.curtails_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.delays_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.divide_by_ratio

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.get_overlap_with_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.happens_during_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.intersects_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.is_congruent_to_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.is_tangent_to_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.overlaps_all_of_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.overlaps_only_start_of_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.overlaps_only_stop_of_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.overlaps_start_of_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.overlaps_stop_of_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.reflect

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.round_offsets

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.scale

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.set_duration

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.set_offsets

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.split_at_offset

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.split_at_offsets

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.starts_after_offset

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.starts_after_timespan_starts

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.starts_after_timespan_stops

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.starts_at_offset

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.starts_at_or_after_offset

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.starts_before_offset

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.starts_before_or_at_offset

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.starts_before_timespan_starts

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.starts_before_timespan_stops

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.starts_during_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.starts_when_timespan_starts

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.starts_when_timespan_stops

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.stops_after_offset

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.stops_after_timespan_starts

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.stops_after_timespan_stops

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.stops_at_offset

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.stops_at_or_after_offset

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.stops_before_offset

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.stops_before_or_at_offset

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.stops_before_timespan_starts

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.stops_before_timespan_stops

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.stops_during_timespan

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.stops_when_timespan_starts

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.stops_when_timespan_stops

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.stretch

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.translate

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.translate_offsets

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.trisects_timespan

Special methods
---------------

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__and__

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__eq__

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__format__

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__ge__

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__gt__

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__hash__

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__illustrate__

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__le__

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__len__

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__lt__

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__ne__

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.Timespan.Timespan.__repr__

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__sub__

.. automethod:: abjad.tools.timespantools.Timespan.Timespan.__xor__
