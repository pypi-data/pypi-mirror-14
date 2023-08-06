.. currentmodule:: abjad.tools.pitchtools

NamedInterval
=============

.. autoclass:: NamedInterval

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
              "abjad.tools.pitchtools.NamedInterval.NamedInterval" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NamedInterval</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Interval.Interval" -> "abjad.tools.pitchtools.NamedInterval.NamedInterval";
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

      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.cents
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.direction_number
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.direction_string
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.from_pitch_carriers
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.interval_class
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.interval_string
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.is_named_interval_abbreviation
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.is_named_interval_quality_abbreviation
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.named_interval_class
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.number
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.octaves
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.quality_string
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.semitones
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.staff_spaces
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__abs__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__add__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__copy__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__eq__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__float__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__format__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__ge__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__gt__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__hash__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__int__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__le__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__lt__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__mul__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__ne__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__neg__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__repr__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__rmul__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__str__
      ~abjad.tools.pitchtools.NamedInterval.NamedInterval.__sub__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.NamedInterval.NamedInterval.cents

.. autoattribute:: abjad.tools.pitchtools.NamedInterval.NamedInterval.direction_number

.. autoattribute:: abjad.tools.pitchtools.NamedInterval.NamedInterval.direction_string

.. autoattribute:: abjad.tools.pitchtools.NamedInterval.NamedInterval.interval_class

.. autoattribute:: abjad.tools.pitchtools.NamedInterval.NamedInterval.interval_string

.. autoattribute:: abjad.tools.pitchtools.NamedInterval.NamedInterval.named_interval_class

.. autoattribute:: abjad.tools.pitchtools.NamedInterval.NamedInterval.number

.. autoattribute:: abjad.tools.pitchtools.NamedInterval.NamedInterval.octaves

.. autoattribute:: abjad.tools.pitchtools.NamedInterval.NamedInterval.quality_string

.. autoattribute:: abjad.tools.pitchtools.NamedInterval.NamedInterval.semitones

.. autoattribute:: abjad.tools.pitchtools.NamedInterval.NamedInterval.staff_spaces

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.from_pitch_carriers

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.is_named_interval_abbreviation

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.is_named_interval_quality_abbreviation

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__abs__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__add__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__copy__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__eq__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__format__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__ge__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__gt__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__hash__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__int__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__le__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__lt__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__mul__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__ne__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__neg__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__repr__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__rmul__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__str__

.. automethod:: abjad.tools.pitchtools.NamedInterval.NamedInterval.__sub__
