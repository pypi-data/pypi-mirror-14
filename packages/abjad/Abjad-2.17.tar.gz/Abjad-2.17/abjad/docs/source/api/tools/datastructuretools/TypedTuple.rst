.. currentmodule:: abjad.tools.datastructuretools

TypedTuple
==========

.. autoclass:: TypedTuple

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
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TypedTuple</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedTuple.TypedTuple";
          }
          subgraph cluster_patterntools {
              graph [label=patterntools];
              "abjad.tools.patterntools.CompoundPattern.CompoundPattern" [color=4,
                  group=3,
                  label=CompoundPattern,
                  shape=box];
              "abjad.tools.patterntools.PatternInventory.PatternInventory" [color=4,
                  group=3,
                  label=PatternInventory,
                  shape=box];
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.IntervalClassSegment.IntervalClassSegment" [color=5,
                  group=4,
                  label=IntervalClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" [color=5,
                  group=4,
                  label=IntervalSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" [color=5,
                  group=4,
                  label=PitchClassSegment,
                  shape=box];
              "abjad.tools.pitchtools.PitchSegment.PitchSegment" [color=5,
                  group=4,
                  label=PitchSegment,
                  shape=box];
              "abjad.tools.pitchtools.Segment.Segment" [color=5,
                  group=4,
                  label=Segment,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow" [color=5,
                  group=4,
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
              "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass" [color=6,
                  group=5,
                  label=RootlessChordClass,
                  shape=box];
              "abjad.tools.tonalanalysistools.Scale.Scale" [color=6,
                  group=5,
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
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.patterntools.CompoundPattern.CompoundPattern";
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.patterntools.PatternInventory.PatternInventory";
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.pitchtools.Segment.Segment";
          "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" -> "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass";
          "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.tonalanalysistools.Scale.Scale";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.count
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.index
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.item_class
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.items
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__add__
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__contains__
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__eq__
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__format__
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__getitem__
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__getslice__
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__hash__
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__iter__
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__len__
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__mul__
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__ne__
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__radd__
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__repr__
      ~abjad.tools.datastructuretools.TypedTuple.TypedTuple.__rmul__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.items

Methods
-------

.. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.count

.. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.index

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__add__

.. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__format__

.. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__getitem__

.. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__getslice__

.. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__len__

.. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__ne__

.. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__repr__

.. automethod:: abjad.tools.datastructuretools.TypedTuple.TypedTuple.__rmul__
