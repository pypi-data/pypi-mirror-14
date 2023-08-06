.. currentmodule:: abjad.tools.pitchtools

PitchSegment
============

.. autoclass:: PitchSegment

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
              "abjad.tools.pitchtools.PitchSegment.PitchSegment" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PitchSegment</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Segment.Segment" [color=4,
                  group=3,
                  label=Segment,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.PitchSegment.PitchSegment";
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

      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.count
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.from_selection
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.has_duplicates
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.hertz
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.index
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.inflection_point_count
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.invert
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.is_equivalent_under_transposition
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.item_class
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.items
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.local_maxima
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.local_minima
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.make_notes
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.multiply
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.retrograde
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.rotate
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.transpose
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__add__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__contains__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__eq__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__format__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__getitem__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__getslice__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__hash__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__illustrate__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__iter__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__len__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__mul__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__ne__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__radd__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__repr__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__rmul__
      ~abjad.tools.pitchtools.PitchSegment.PitchSegment.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.PitchSegment.PitchSegment.has_duplicates

.. autoattribute:: abjad.tools.pitchtools.PitchSegment.PitchSegment.hertz

.. autoattribute:: abjad.tools.pitchtools.PitchSegment.PitchSegment.inflection_point_count

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchSegment.PitchSegment.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchSegment.PitchSegment.items

.. autoattribute:: abjad.tools.pitchtools.PitchSegment.PitchSegment.local_maxima

.. autoattribute:: abjad.tools.pitchtools.PitchSegment.PitchSegment.local_minima

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.index

.. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.invert

.. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.is_equivalent_under_transposition

.. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.make_notes

.. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.multiply

.. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.retrograde

.. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.rotate

.. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.transpose

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__getslice__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__hash__

.. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSegment.PitchSegment.__str__
