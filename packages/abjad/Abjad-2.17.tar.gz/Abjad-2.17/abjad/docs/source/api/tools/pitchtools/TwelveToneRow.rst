.. currentmodule:: abjad.tools.pitchtools

TwelveToneRow
=============

.. autoclass:: TwelveToneRow

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
              "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>TwelveToneRow</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment" -> "abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow";
              "abjad.tools.pitchtools.Segment.Segment" -> "abjad.tools.pitchtools.PitchClassSegment.PitchClassSegment";
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

      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.alpha
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.count
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.from_selection
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.has_duplicates
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.index
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.invert
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.is_equivalent_under_transposition
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.item_class
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.items
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.make_notes
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.multiply
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.permute
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.retrograde
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.rotate
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.transpose
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.voice_horizontally
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.voice_vertically
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__add__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__contains__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__eq__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__format__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__getitem__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__getslice__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__hash__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__iter__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__len__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__mul__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__ne__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__radd__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__repr__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__rmul__
      ~abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__str__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.has_duplicates

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.items

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.alpha

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.index

.. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.invert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.is_equivalent_under_transposition

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.make_notes

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.multiply

.. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.permute

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.retrograde

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.rotate

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.transpose

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.voice_horizontally

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.voice_vertically

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__getitem__

.. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__getslice__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__len__

.. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__repr__

.. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.TwelveToneRow.TwelveToneRow.__str__
