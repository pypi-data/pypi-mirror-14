.. currentmodule:: abjad.tools.pitchtools

IntervalSegment
===============

.. autoclass:: IntervalSegment

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
              "abjad.tools.pitchtools.IntervalSegment.IntervalSegment" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>IntervalSegment</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Segment.Segment" [color=4,
                  group=3,
                  label=Segment,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.IntervalSegment.IntervalSegment";
          }
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.RootlessChordClass.RootlessChordClass" [color=5,
                  group=4,
                  label=RootlessChordClass,
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

      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.count
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.from_selection
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.has_duplicates
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.index
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.item_class
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.items
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.rotate
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.slope
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.spread
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__add__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__contains__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__eq__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__format__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__getitem__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__getslice__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__hash__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__iter__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__len__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__mul__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__ne__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__radd__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__repr__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__rmul__
      ~abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.has_duplicates

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.items

.. autoattribute:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.slope

.. autoattribute:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.spread

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.index

.. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.rotate

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__getslice__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSegment.IntervalSegment.__str__
