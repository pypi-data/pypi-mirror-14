.. currentmodule:: abjad.tools.pitchtools

NumberedInterval
================

.. autoclass:: NumberedInterval

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
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.Interval.Interval" [color=3,
                  group=2,
                  label=Interval,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.NumberedInterval.NumberedInterval" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NumberedInterval</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Interval.Interval" -> "abjad.tools.pitchtools.NumberedInterval.NumberedInterval";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.Interval.Interval";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.pitchtools.Interval`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.cents
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.direction_number
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.direction_string
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.from_pitch_carriers
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.is_named_interval_abbreviation
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.is_named_interval_quality_abbreviation
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.number
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.numbered_interval_number
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.semitones
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.to_named_interval
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__abs__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__add__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__copy__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__eq__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__float__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__format__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__ge__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__gt__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__hash__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__int__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__le__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__lt__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__ne__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__neg__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__repr__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__str__
      ~abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__sub__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.cents

.. autoattribute:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.direction_number

.. autoattribute:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.direction_string

.. autoattribute:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.number

.. autoattribute:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.numbered_interval_number

.. autoattribute:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.semitones

Methods
-------

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.to_named_interval

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.from_pitch_carriers

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.is_named_interval_abbreviation

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.is_named_interval_quality_abbreviation

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__abs__

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__add__

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__copy__

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__eq__

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__format__

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__ge__

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__gt__

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__hash__

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__int__

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__le__

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__ne__

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__neg__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__repr__

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__str__

.. automethod:: abjad.tools.pitchtools.NumberedInterval.NumberedInterval.__sub__
