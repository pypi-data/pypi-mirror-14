.. currentmodule:: abjad.tools.pitchtools

Pitch
=====

.. autoclass:: Pitch

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
              "abjad.tools.pitchtools.NamedPitch.NamedPitch" [color=3,
                  group=2,
                  label=NamedPitch,
                  shape=box];
              "abjad.tools.pitchtools.NumberedPitch.NumberedPitch" [color=3,
                  group=2,
                  label=NumberedPitch,
                  shape=box];
              "abjad.tools.pitchtools.Pitch.Pitch" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Pitch</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Pitch.Pitch" -> "abjad.tools.pitchtools.NamedPitch.NamedPitch";
              "abjad.tools.pitchtools.Pitch.Pitch" -> "abjad.tools.pitchtools.NumberedPitch.NumberedPitch";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.Pitch.Pitch";
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

      ~abjad.tools.pitchtools.Pitch.Pitch.accidental
      ~abjad.tools.pitchtools.Pitch.Pitch.accidental_spelling
      ~abjad.tools.pitchtools.Pitch.Pitch.alteration_in_semitones
      ~abjad.tools.pitchtools.Pitch.Pitch.apply_accidental
      ~abjad.tools.pitchtools.Pitch.Pitch.diatonic_pitch_class_name
      ~abjad.tools.pitchtools.Pitch.Pitch.diatonic_pitch_class_number
      ~abjad.tools.pitchtools.Pitch.Pitch.diatonic_pitch_name
      ~abjad.tools.pitchtools.Pitch.Pitch.diatonic_pitch_number
      ~abjad.tools.pitchtools.Pitch.Pitch.from_hertz
      ~abjad.tools.pitchtools.Pitch.Pitch.hertz
      ~abjad.tools.pitchtools.Pitch.Pitch.invert
      ~abjad.tools.pitchtools.Pitch.Pitch.is_diatonic_pitch_name
      ~abjad.tools.pitchtools.Pitch.Pitch.is_diatonic_pitch_number
      ~abjad.tools.pitchtools.Pitch.Pitch.is_pitch_carrier
      ~abjad.tools.pitchtools.Pitch.Pitch.is_pitch_class_octave_number_string
      ~abjad.tools.pitchtools.Pitch.Pitch.is_pitch_name
      ~abjad.tools.pitchtools.Pitch.Pitch.is_pitch_number
      ~abjad.tools.pitchtools.Pitch.Pitch.multiply
      ~abjad.tools.pitchtools.Pitch.Pitch.named_pitch
      ~abjad.tools.pitchtools.Pitch.Pitch.named_pitch_class
      ~abjad.tools.pitchtools.Pitch.Pitch.numbered_pitch
      ~abjad.tools.pitchtools.Pitch.Pitch.numbered_pitch_class
      ~abjad.tools.pitchtools.Pitch.Pitch.octave
      ~abjad.tools.pitchtools.Pitch.Pitch.octave_number
      ~abjad.tools.pitchtools.Pitch.Pitch.pitch_class_name
      ~abjad.tools.pitchtools.Pitch.Pitch.pitch_class_number
      ~abjad.tools.pitchtools.Pitch.Pitch.pitch_class_octave_label
      ~abjad.tools.pitchtools.Pitch.Pitch.pitch_name
      ~abjad.tools.pitchtools.Pitch.Pitch.pitch_number
      ~abjad.tools.pitchtools.Pitch.Pitch.transpose
      ~abjad.tools.pitchtools.Pitch.Pitch.__eq__
      ~abjad.tools.pitchtools.Pitch.Pitch.__float__
      ~abjad.tools.pitchtools.Pitch.Pitch.__format__
      ~abjad.tools.pitchtools.Pitch.Pitch.__hash__
      ~abjad.tools.pitchtools.Pitch.Pitch.__illustrate__
      ~abjad.tools.pitchtools.Pitch.Pitch.__int__
      ~abjad.tools.pitchtools.Pitch.Pitch.__ne__
      ~abjad.tools.pitchtools.Pitch.Pitch.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.accidental

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.accidental_spelling

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.alteration_in_semitones

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.diatonic_pitch_class_name

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.diatonic_pitch_class_number

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.diatonic_pitch_name

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.diatonic_pitch_number

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.hertz

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.named_pitch

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.named_pitch_class

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.numbered_pitch

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.numbered_pitch_class

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.octave

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.octave_number

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.pitch_class_name

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.pitch_class_number

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.pitch_class_octave_label

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.pitch_name

.. autoattribute:: abjad.tools.pitchtools.Pitch.Pitch.pitch_number

Methods
-------

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.apply_accidental

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.invert

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.multiply

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.transpose

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.from_hertz

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.is_diatonic_pitch_name

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.is_diatonic_pitch_number

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.is_pitch_carrier

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.is_pitch_class_octave_number_string

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.is_pitch_name

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.is_pitch_number

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Pitch.Pitch.__eq__

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.__float__

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.__format__

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.__hash__

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.__illustrate__

.. automethod:: abjad.tools.pitchtools.Pitch.Pitch.__int__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Pitch.Pitch.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Pitch.Pitch.__repr__
