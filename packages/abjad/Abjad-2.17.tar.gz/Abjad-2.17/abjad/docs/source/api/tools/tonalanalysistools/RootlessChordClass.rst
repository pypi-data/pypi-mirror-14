.. currentmodule:: abjad.tools.tonalanalysistools

RootlessChordClass
==================

.. autoclass:: RootlessChordClass

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
              "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" [color=4,
                  group=3,
                  label=IntervalSegment,
                  shape=box];
              "abjad.tools.pitchtools.Segment.Segment" [color=4,
                  group=3,
                  label=Segment,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.IntervalSegment.IntervalSegment";
          }
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass" [color=black,
                  fontcolor=white,
                  group=4,
                  label=<<B>RootlessChordClass</B>>,
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
          "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" -> "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.pitchtools.IntervalSegment`

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

      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.cardinality
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.count
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.extent
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.extent_name
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.from_interval_class_segment
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.from_selection
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.has_duplicates
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.index
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.inversion
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.item_class
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.items
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.position
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.quality_string
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.rotate
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.rotation
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.slope
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.spread
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__add__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__contains__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__eq__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__format__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__getitem__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__getslice__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__hash__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__iter__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__len__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__mul__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__ne__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__radd__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__repr__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__rmul__
      ~abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.cardinality

.. autoattribute:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.extent

.. autoattribute:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.extent_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.has_duplicates

.. autoattribute:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.inversion

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.items

.. autoattribute:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.position

.. autoattribute:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.quality_string

.. autoattribute:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.rotation

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.slope

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.spread

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.rotate

Class & static methods
----------------------

.. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.from_interval_class_segment

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__getslice__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__radd__

.. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass.__str__
