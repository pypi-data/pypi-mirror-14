.. currentmodule:: abjad.tools.pitchtools

PitchClassSegment
=================

.. autoclass:: PitchClassSegment

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
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PitchClassSegment</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Segment.Segment" [color=4,
                  group=3,
                  label=Segment,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow" [color=4,
                  group=3,
                  label=TwelveToneRow,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment";
          }
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.Scale.Scale" [color=5,
                  group=4,
                  label=Scale,
                  shape=box];
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

      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.alpha
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.count
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.from_selection
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.has_duplicates
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.index
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.invert
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.is_equivalent_under_transposition
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.item_class
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.items
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.make_notes
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.multiply
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.retrograde
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.rotate
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.transpose
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.voice_horizontally
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.voice_vertically
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__add__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__contains__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__eq__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__format__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__getitem__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__getslice__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__hash__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__iter__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__len__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__mul__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__ne__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__radd__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__repr__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__rmul__
      ~abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.has_duplicates

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.items

Methods
-------

.. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.alpha

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.index

.. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.invert

.. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.is_equivalent_under_transposition

.. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.make_notes

.. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.multiply

.. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.retrograde

.. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.rotate

.. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.transpose

.. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.voice_horizontally

.. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.voice_vertically

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__getslice__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment.__str__
