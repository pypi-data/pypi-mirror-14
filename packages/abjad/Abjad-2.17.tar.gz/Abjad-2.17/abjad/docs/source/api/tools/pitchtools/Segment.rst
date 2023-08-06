.. currentmodule:: abjad.tools.pitchtools

Segment
=======

.. autoclass:: Segment

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
              "abjad.tools.pitchtools.IntervalClassSegment.IntervalClassSegment" [color=4,
                  group=3,
                  label=IntervalClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" [color=4,
                  group=3,
                  label=IntervalSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" [color=4,
                  group=3,
                  label=PitchClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchSegment.PitchSegment" [color=4,
                  group=3,
                  label=PitchSegment,
                  shape=box];
              "abjad.tools.pitchtools.Segment.Segment" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>Segment</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow" [color=4,
                  group=3,
                  label=TwelveToneRow,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.IntervalClassSegment.IntervalClassSegment";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.IntervalSegment.IntervalSegment";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.PitchSegment.PitchSegment";
          }
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass" [color=5,
                  group=4,
                  label=RootlessChordClass,
                  shape=box];
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
          "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" -> "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass";
          "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.tonalanalysistools.Scale.Scale";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TypedTuple`

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.Segment.Segment.count
      ~abjad.tools.pitchtools.Segment.Segment.from_selection
      ~abjad.tools.pitchtools.Segment.Segment.has_duplicates
      ~abjad.tools.pitchtools.Segment.Segment.index
      ~abjad.tools.pitchtools.Segment.Segment.item_class
      ~abjad.tools.pitchtools.Segment.Segment.items
      ~abjad.tools.pitchtools.Segment.Segment.__add__
      ~abjad.tools.pitchtools.Segment.Segment.__contains__
      ~abjad.tools.pitchtools.Segment.Segment.__eq__
      ~abjad.tools.pitchtools.Segment.Segment.__format__
      ~abjad.tools.pitchtools.Segment.Segment.__getitem__
      ~abjad.tools.pitchtools.Segment.Segment.__getslice__
      ~abjad.tools.pitchtools.Segment.Segment.__hash__
      ~abjad.tools.pitchtools.Segment.Segment.__iter__
      ~abjad.tools.pitchtools.Segment.Segment.__len__
      ~abjad.tools.pitchtools.Segment.Segment.__mul__
      ~abjad.tools.pitchtools.Segment.Segment.__ne__
      ~abjad.tools.pitchtools.Segment.Segment.__radd__
      ~abjad.tools.pitchtools.Segment.Segment.__repr__
      ~abjad.tools.pitchtools.Segment.Segment.__rmul__
      ~abjad.tools.pitchtools.Segment.Segment.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.Segment.Segment.has_duplicates

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.Segment.Segment.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.Segment.Segment.items

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.count

.. automethod:: abjad.tools.pitchtools.Segment.Segment.from_selection

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.index

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__getslice__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Segment.Segment.__rmul__

.. automethod:: abjad.tools.pitchtools.Segment.Segment.__str__
