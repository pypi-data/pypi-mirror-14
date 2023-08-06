.. currentmodule:: abjad.tools.tonalanalysistools

Scale
=====

.. autoclass:: Scale

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
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" [color=3,
                  group=2,
                  label=TypedTuple,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedTuple.TypedTuple";
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" [color=4,
                  group=3,
                  label=PitchClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.Segment.Segment" [color=4,
                  group=3,
                  label=Segment,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment";
          }
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.Scale.Scale" [color=black,
                  fontcolor=white,
                  group=4,
                  label=<<B>Scale</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.pitchtools.Segment.Segment";
          "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.tonalanalysistools.Scale.Scale";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.pitchtools.PitchClassSegment`

- :py:class:`abjad.tools.pitchtools.Segment`

- :py:class:`abjad.tools.datastructuretools.TypedTuple`

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.tonalanalysistools.Scale.Scale.alpha
      ~abjad.tools.tonalanalysistools.Scale.Scale.count
      ~abjad.tools.tonalanalysistools.Scale.Scale.create_named_pitch_set_in_pitch_range
      ~abjad.tools.tonalanalysistools.Scale.Scale.dominant
      ~abjad.tools.tonalanalysistools.Scale.Scale.from_selection
      ~abjad.tools.tonalanalysistools.Scale.Scale.has_duplicates
      ~abjad.tools.tonalanalysistools.Scale.Scale.index
      ~abjad.tools.tonalanalysistools.Scale.Scale.invert
      ~abjad.tools.tonalanalysistools.Scale.Scale.is_equivalent_under_transposition
      ~abjad.tools.tonalanalysistools.Scale.Scale.item_class
      ~abjad.tools.tonalanalysistools.Scale.Scale.items
      ~abjad.tools.tonalanalysistools.Scale.Scale.key_signature
      ~abjad.tools.tonalanalysistools.Scale.Scale.leading_tone
      ~abjad.tools.tonalanalysistools.Scale.Scale.make_notes
      ~abjad.tools.tonalanalysistools.Scale.Scale.make_score
      ~abjad.tools.tonalanalysistools.Scale.Scale.mediant
      ~abjad.tools.tonalanalysistools.Scale.Scale.multiply
      ~abjad.tools.tonalanalysistools.Scale.Scale.named_interval_class_segment
      ~abjad.tools.tonalanalysistools.Scale.Scale.named_pitch_class_to_scale_degree
      ~abjad.tools.tonalanalysistools.Scale.Scale.retrograde
      ~abjad.tools.tonalanalysistools.Scale.Scale.rotate
      ~abjad.tools.tonalanalysistools.Scale.Scale.scale_degree_to_named_pitch_class
      ~abjad.tools.tonalanalysistools.Scale.Scale.subdominant
      ~abjad.tools.tonalanalysistools.Scale.Scale.submediant
      ~abjad.tools.tonalanalysistools.Scale.Scale.superdominant
      ~abjad.tools.tonalanalysistools.Scale.Scale.tonic
      ~abjad.tools.tonalanalysistools.Scale.Scale.transpose
      ~abjad.tools.tonalanalysistools.Scale.Scale.voice_horizontally
      ~abjad.tools.tonalanalysistools.Scale.Scale.voice_scale_degrees_in_open_position
      ~abjad.tools.tonalanalysistools.Scale.Scale.voice_vertically
      ~abjad.tools.tonalanalysistools.Scale.Scale.__add__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__contains__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__eq__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__format__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__getitem__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__getslice__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__hash__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__iter__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__len__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__mul__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__ne__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__radd__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__repr__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__rmul__
      ~abjad.tools.tonalanalysistools.Scale.Scale.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.tonalanalysistools.Scale.Scale.dominant

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.tonalanalysistools.Scale.Scale.has_duplicates

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.tonalanalysistools.Scale.Scale.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.tonalanalysistools.Scale.Scale.items

.. autoattribute:: abjad.tools.tonalanalysistools.Scale.Scale.key_signature

.. autoattribute:: abjad.tools.tonalanalysistools.Scale.Scale.leading_tone

.. autoattribute:: abjad.tools.tonalanalysistools.Scale.Scale.mediant

.. autoattribute:: abjad.tools.tonalanalysistools.Scale.Scale.named_interval_class_segment

.. autoattribute:: abjad.tools.tonalanalysistools.Scale.Scale.subdominant

.. autoattribute:: abjad.tools.tonalanalysistools.Scale.Scale.submediant

.. autoattribute:: abjad.tools.tonalanalysistools.Scale.Scale.superdominant

.. autoattribute:: abjad.tools.tonalanalysistools.Scale.Scale.tonic

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.alpha

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.count

.. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.create_named_pitch_set_in_pitch_range

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.invert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.is_equivalent_under_transposition

.. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.make_notes

.. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.make_score

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.multiply

.. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.named_pitch_class_to_scale_degree

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.retrograde

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.rotate

.. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.scale_degree_to_named_pitch_class

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.transpose

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.voice_horizontally

.. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.voice_scale_degrees_in_open_position

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.voice_vertically

Class & static methods
----------------------

.. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__getslice__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.Scale.Scale.__str__
