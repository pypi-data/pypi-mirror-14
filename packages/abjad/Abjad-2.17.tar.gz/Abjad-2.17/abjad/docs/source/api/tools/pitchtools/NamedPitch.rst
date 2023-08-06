.. currentmodule:: abjad.tools.pitchtools

NamedPitch
==========

.. autoclass:: NamedPitch

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
              "abjad.tools.pitchtools.NamedPitch.NamedPitch" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NamedPitch</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Pitch.Pitch" [color=3,
                  group=2,
                  label=Pitch,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Pitch.Pitch" -> "abjad.tools.pitchtools.NamedPitch.NamedPitch";
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

- :py:class:`abjad.tools.pitchtools.Pitch`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.accidental
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.accidental_spelling
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.alteration_in_semitones
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.apply_accidental
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.diatonic_pitch_class_name
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.diatonic_pitch_class_number
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.diatonic_pitch_name
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.diatonic_pitch_number
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.from_hertz
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.from_pitch_carrier
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.from_staff_position
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.hertz
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.invert
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.is_diatonic_pitch_name
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.is_diatonic_pitch_number
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.is_pitch_carrier
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.is_pitch_class_octave_number_string
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.is_pitch_name
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.is_pitch_number
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.multiply
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.named_pitch
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.named_pitch_class
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.numbered_pitch
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.numbered_pitch_class
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.octave
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.octave_number
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.pitch_class_name
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.pitch_class_number
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.pitch_class_octave_label
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.pitch_name
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.pitch_number
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.respell_with_flats
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.respell_with_sharps
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.to_staff_position
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.transpose
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__add__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__copy__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__eq__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__float__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__format__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__ge__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__gt__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__hash__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__illustrate__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__int__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__le__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__lt__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__ne__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__repr__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__str__
      ~abjad.tools.pitchtools.NamedPitch.NamedPitch.__sub__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.accidental

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.accidental_spelling

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.alteration_in_semitones

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.diatonic_pitch_class_name

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.diatonic_pitch_class_number

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.diatonic_pitch_name

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.diatonic_pitch_number

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.hertz

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.named_pitch

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.named_pitch_class

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.numbered_pitch

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.numbered_pitch_class

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.octave

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.octave_number

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.pitch_class_name

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.pitch_class_number

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.pitch_class_octave_label

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.pitch_name

.. autoattribute:: abjad.tools.pitchtools.NamedPitch.NamedPitch.pitch_number

Methods
-------

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.apply_accidental

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.invert

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.multiply

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.respell_with_flats

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.respell_with_sharps

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.to_staff_position

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.transpose

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.from_hertz

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.from_pitch_carrier

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.from_staff_position

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.is_diatonic_pitch_name

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.is_diatonic_pitch_number

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.is_pitch_carrier

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.is_pitch_class_octave_number_string

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.is_pitch_name

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.is_pitch_number

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__add__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__copy__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__eq__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__format__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__ge__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__gt__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__illustrate__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__int__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__le__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__lt__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__repr__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__str__

.. automethod:: abjad.tools.pitchtools.NamedPitch.NamedPitch.__sub__
