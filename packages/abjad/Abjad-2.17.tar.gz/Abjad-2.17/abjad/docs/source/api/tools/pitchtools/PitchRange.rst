.. currentmodule:: abjad.tools.pitchtools

PitchRange
==========

.. autoclass:: PitchRange

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
              "abjad.tools.pitchtools.PitchRange.PitchRange" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>PitchRange</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.PitchRange.PitchRange";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.PitchRange.PitchRange.from_pitches
      ~abjad.tools.pitchtools.PitchRange.PitchRange.is_range_string
      ~abjad.tools.pitchtools.PitchRange.PitchRange.list_octave_transpositions
      ~abjad.tools.pitchtools.PitchRange.PitchRange.one_line_named_pitch_repr
      ~abjad.tools.pitchtools.PitchRange.PitchRange.one_line_numbered_pitch_repr
      ~abjad.tools.pitchtools.PitchRange.PitchRange.range_string
      ~abjad.tools.pitchtools.PitchRange.PitchRange.start_pitch
      ~abjad.tools.pitchtools.PitchRange.PitchRange.start_pitch_is_included_in_range
      ~abjad.tools.pitchtools.PitchRange.PitchRange.stop_pitch
      ~abjad.tools.pitchtools.PitchRange.PitchRange.stop_pitch_is_included_in_range
      ~abjad.tools.pitchtools.PitchRange.PitchRange.voice_pitch_class
      ~abjad.tools.pitchtools.PitchRange.PitchRange.__contains__
      ~abjad.tools.pitchtools.PitchRange.PitchRange.__eq__
      ~abjad.tools.pitchtools.PitchRange.PitchRange.__format__
      ~abjad.tools.pitchtools.PitchRange.PitchRange.__ge__
      ~abjad.tools.pitchtools.PitchRange.PitchRange.__gt__
      ~abjad.tools.pitchtools.PitchRange.PitchRange.__hash__
      ~abjad.tools.pitchtools.PitchRange.PitchRange.__illustrate__
      ~abjad.tools.pitchtools.PitchRange.PitchRange.__le__
      ~abjad.tools.pitchtools.PitchRange.PitchRange.__lt__
      ~abjad.tools.pitchtools.PitchRange.PitchRange.__ne__
      ~abjad.tools.pitchtools.PitchRange.PitchRange.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.PitchRange.PitchRange.one_line_named_pitch_repr

.. autoattribute:: abjad.tools.pitchtools.PitchRange.PitchRange.one_line_numbered_pitch_repr

.. autoattribute:: abjad.tools.pitchtools.PitchRange.PitchRange.range_string

.. autoattribute:: abjad.tools.pitchtools.PitchRange.PitchRange.start_pitch

.. autoattribute:: abjad.tools.pitchtools.PitchRange.PitchRange.start_pitch_is_included_in_range

.. autoattribute:: abjad.tools.pitchtools.PitchRange.PitchRange.stop_pitch

.. autoattribute:: abjad.tools.pitchtools.PitchRange.PitchRange.stop_pitch_is_included_in_range

Methods
-------

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.list_octave_transpositions

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.voice_pitch_class

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.from_pitches

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.is_range_string

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.__contains__

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.__eq__

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.__format__

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.__ge__

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.__gt__

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.__hash__

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.__illustrate__

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.__le__

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.__lt__

.. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRange.PitchRange.__repr__
