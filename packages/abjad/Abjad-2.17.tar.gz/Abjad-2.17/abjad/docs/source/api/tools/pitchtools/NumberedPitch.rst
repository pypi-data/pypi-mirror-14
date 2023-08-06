.. currentmodule:: abjad.tools.pitchtools

NumberedPitch
=============

.. autoclass:: NumberedPitch

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
              "abjad.tools.pitchtools.NumberedPitch.NumberedPitch" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NumberedPitch</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Pitch.Pitch" [color=3,
                  group=2,
                  label=Pitch,
                  shape=oval,
                  style=bold];
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

- :py:class:`abjad.tools.pitchtools.Pitch`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.accidental
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.accidental_spelling
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.alteration_in_semitones
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.apply_accidental
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.diatonic_pitch_class_name
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.diatonic_pitch_class_number
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.diatonic_pitch_name
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.diatonic_pitch_number
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.from_hertz
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.hertz
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.interpolate
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.invert
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.is_diatonic_pitch_name
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.is_diatonic_pitch_number
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.is_pitch_carrier
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.is_pitch_class_octave_number_string
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.is_pitch_name
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.is_pitch_number
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.multiply
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.named_pitch
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.named_pitch_class
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.numbered_pitch
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.numbered_pitch_class
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.octave
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.octave_number
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.pitch_class_name
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.pitch_class_number
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.pitch_class_octave_label
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.pitch_name
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.pitch_number
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.transpose
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__add__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__eq__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__float__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__format__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__ge__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__gt__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__hash__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__illustrate__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__int__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__le__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__lt__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__ne__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__neg__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__repr__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__str__
      ~abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__sub__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.accidental

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.accidental_spelling

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.alteration_in_semitones

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.diatonic_pitch_class_name

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.diatonic_pitch_class_number

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.diatonic_pitch_name

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.diatonic_pitch_number

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.hertz

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.named_pitch

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.named_pitch_class

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.numbered_pitch

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.numbered_pitch_class

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.octave

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.octave_number

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.pitch_class_name

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.pitch_class_number

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.pitch_class_octave_label

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.pitch_name

.. autoattribute:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.pitch_number

Methods
-------

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.apply_accidental

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.interpolate

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.invert

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.multiply

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.transpose

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.from_hertz

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.is_diatonic_pitch_name

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.is_diatonic_pitch_number

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.is_pitch_carrier

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.is_pitch_class_octave_number_string

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.is_pitch_name

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.is_pitch_number

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__add__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__eq__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__float__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__format__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__ge__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__gt__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__illustrate__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__int__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__le__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__ne__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__neg__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__repr__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__str__

.. automethod:: abjad.tools.pitchtools.NumberedPitch.NumberedPitch.__sub__
