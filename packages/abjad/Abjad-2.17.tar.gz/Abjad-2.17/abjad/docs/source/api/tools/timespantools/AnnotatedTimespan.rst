.. currentmodule:: abjad.tools.timespantools

AnnotatedTimespan
=================

.. autoclass:: AnnotatedTimespan

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
              "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>AnnotatedTimespan</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.timespantools.Timespan.Timespan" [color=4,
                  group=3,
                  label=Timespan,
                  shape=box];
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

- :py:class:`abjad.tools.timespantools.Timespan`

- :py:class:`abjad.tools.mathtools.BoundedObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.annotation
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.axis
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.contains_timespan_improperly
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.curtails_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.delays_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.divide_by_ratio
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.duration
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.get_overlap_with_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.happens_during_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.intersects_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_closed
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_congruent_to_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_half_closed
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_half_open
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_left_closed
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_left_open
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_open
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_right_closed
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_right_open
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_tangent_to_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_well_formed
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.offsets
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.overlaps_all_of_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.overlaps_only_start_of_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.overlaps_only_stop_of_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.overlaps_start_of_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.overlaps_stop_of_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.reflect
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.round_offsets
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.scale
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.set_duration
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.set_offsets
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.split_at_offset
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.split_at_offsets
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.start_offset
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_after_offset
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_after_timespan_starts
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_after_timespan_stops
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_at_offset
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_at_or_after_offset
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_before_offset
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_before_or_at_offset
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_before_timespan_starts
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_before_timespan_stops
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_during_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_when_timespan_starts
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_when_timespan_stops
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stop_offset
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_after_offset
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_after_timespan_starts
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_after_timespan_stops
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_at_offset
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_at_or_after_offset
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_before_offset
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_before_or_at_offset
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_before_timespan_starts
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_before_timespan_stops
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_during_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_when_timespan_starts
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_when_timespan_stops
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stretch
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.translate
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.translate_offsets
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.trisects_timespan
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__and__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__eq__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__format__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__ge__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__gt__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__hash__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__illustrate__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__le__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__len__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__lt__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__ne__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__or__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__repr__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__sub__
      ~abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__xor__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.axis

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.duration

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_closed

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_half_closed

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_half_open

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_left_closed

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_left_open

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_open

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_right_closed

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_right_open

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_well_formed

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.offsets

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.start_offset

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stop_offset

Read/write properties
---------------------

.. autoattribute:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.annotation

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.contains_timespan_improperly

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.curtails_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.delays_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.divide_by_ratio

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.get_overlap_with_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.happens_during_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.intersects_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_congruent_to_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.is_tangent_to_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.overlaps_all_of_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.overlaps_only_start_of_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.overlaps_only_stop_of_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.overlaps_start_of_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.overlaps_stop_of_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.reflect

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.round_offsets

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.scale

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.set_duration

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.set_offsets

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.split_at_offset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.split_at_offsets

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_after_offset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_after_timespan_starts

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_after_timespan_stops

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_at_offset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_at_or_after_offset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_before_offset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_before_or_at_offset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_before_timespan_starts

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_before_timespan_stops

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_during_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_when_timespan_starts

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.starts_when_timespan_stops

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_after_offset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_after_timespan_starts

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_after_timespan_stops

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_at_offset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_at_or_after_offset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_before_offset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_before_or_at_offset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_before_timespan_starts

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_before_timespan_stops

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_during_timespan

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_when_timespan_starts

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stops_when_timespan_stops

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.stretch

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.translate

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.translate_offsets

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.trisects_timespan

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__sub__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan.__xor__
