.. currentmodule:: abjad.tools.pitchtools

PitchClass
==========

.. autoclass:: PitchClass

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
              "abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass" [color=3,
                  group=2,
                  label=NamedPitchClass,
                  shape=box];
              "abjad.tools.pitchtools.NumberedPitchClass.NumberedPitchClass" [color=3,
                  group=2,
                  label=NumberedPitchClass,
                  shape=box];
              "abjad.tools.pitchtools.PitchClass.PitchClass" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>PitchClass</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchClass.PitchClass" -> "abjad.tools.pitchtools.NamedPitchClass.NamedPitchClass";
              "abjad.tools.pitchtools.PitchClass.PitchClass" -> "abjad.tools.pitchtools.NumberedPitchClass.NumberedPitchClass";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.pitchtools.PitchClass.PitchClass";
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

      ~abjad.tools.pitchtools.PitchClass.PitchClass.accidental
      ~abjad.tools.pitchtools.PitchClass.PitchClass.accidental_spelling
      ~abjad.tools.pitchtools.PitchClass.PitchClass.alteration_in_semitones
      ~abjad.tools.pitchtools.PitchClass.PitchClass.apply_accidental
      ~abjad.tools.pitchtools.PitchClass.PitchClass.diatonic_pitch_class_name
      ~abjad.tools.pitchtools.PitchClass.PitchClass.diatonic_pitch_class_number
      ~abjad.tools.pitchtools.PitchClass.PitchClass.invert
      ~abjad.tools.pitchtools.PitchClass.PitchClass.is_diatonic_pitch_class_name
      ~abjad.tools.pitchtools.PitchClass.PitchClass.is_diatonic_pitch_class_number
      ~abjad.tools.pitchtools.PitchClass.PitchClass.is_pitch_class_name
      ~abjad.tools.pitchtools.PitchClass.PitchClass.is_pitch_class_number
      ~abjad.tools.pitchtools.PitchClass.PitchClass.multiply
      ~abjad.tools.pitchtools.PitchClass.PitchClass.named_pitch_class
      ~abjad.tools.pitchtools.PitchClass.PitchClass.numbered_pitch_class
      ~abjad.tools.pitchtools.PitchClass.PitchClass.pitch_class_label
      ~abjad.tools.pitchtools.PitchClass.PitchClass.pitch_class_name
      ~abjad.tools.pitchtools.PitchClass.PitchClass.pitch_class_number
      ~abjad.tools.pitchtools.PitchClass.PitchClass.transpose
      ~abjad.tools.pitchtools.PitchClass.PitchClass.__eq__
      ~abjad.tools.pitchtools.PitchClass.PitchClass.__format__
      ~abjad.tools.pitchtools.PitchClass.PitchClass.__hash__
      ~abjad.tools.pitchtools.PitchClass.PitchClass.__ne__
      ~abjad.tools.pitchtools.PitchClass.PitchClass.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.PitchClass.PitchClass.accidental

.. autoattribute:: abjad.tools.pitchtools.PitchClass.PitchClass.accidental_spelling

.. autoattribute:: abjad.tools.pitchtools.PitchClass.PitchClass.alteration_in_semitones

.. autoattribute:: abjad.tools.pitchtools.PitchClass.PitchClass.diatonic_pitch_class_name

.. autoattribute:: abjad.tools.pitchtools.PitchClass.PitchClass.diatonic_pitch_class_number

.. autoattribute:: abjad.tools.pitchtools.PitchClass.PitchClass.named_pitch_class

.. autoattribute:: abjad.tools.pitchtools.PitchClass.PitchClass.numbered_pitch_class

.. autoattribute:: abjad.tools.pitchtools.PitchClass.PitchClass.pitch_class_label

.. autoattribute:: abjad.tools.pitchtools.PitchClass.PitchClass.pitch_class_name

.. autoattribute:: abjad.tools.pitchtools.PitchClass.PitchClass.pitch_class_number

Methods
-------

.. automethod:: abjad.tools.pitchtools.PitchClass.PitchClass.apply_accidental

.. automethod:: abjad.tools.pitchtools.PitchClass.PitchClass.invert

.. automethod:: abjad.tools.pitchtools.PitchClass.PitchClass.multiply

.. automethod:: abjad.tools.pitchtools.PitchClass.PitchClass.transpose

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.PitchClass.PitchClass.is_diatonic_pitch_class_name

.. automethod:: abjad.tools.pitchtools.PitchClass.PitchClass.is_diatonic_pitch_class_number

.. automethod:: abjad.tools.pitchtools.PitchClass.PitchClass.is_pitch_class_name

.. automethod:: abjad.tools.pitchtools.PitchClass.PitchClass.is_pitch_class_number

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClass.PitchClass.__eq__

.. automethod:: abjad.tools.pitchtools.PitchClass.PitchClass.__format__

.. automethod:: abjad.tools.pitchtools.PitchClass.PitchClass.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClass.PitchClass.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClass.PitchClass.__repr__
