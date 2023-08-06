.. currentmodule:: abjad.tools.tonalanalysistools

RootedChordClass
================

.. autoclass:: RootedChordClass

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
              "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" [color=3,
                  group=2,
                  label=TypedFrozenset,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset";
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" [color=4,
                  group=3,
                  label=PitchClassSet,
                  shape=box];
              "abjad.tools.pitchtools.Set.Set" [color=4,
                  group=3,
                  label=Set,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.PitchClassSet.PitchClassSet";
          }
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass" [color=black,
                  fontcolor=white,
                  group=4,
                  label=<<B>RootedChordClass</B>>,
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
          "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" -> "abjad.tools.pitchtools.Set.Set";
          "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" -> "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.pitchtools.PitchClassSet`

- :py:class:`abjad.tools.pitchtools.Set`

- :py:class:`abjad.tools.datastructuretools.TypedFrozenset`

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.bass
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.cardinality
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.cardinality_to_extent
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.chord_quality
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.copy
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.difference
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.extent
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.extent_to_cardinality
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.extent_to_extent_name
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.figured_bass
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.from_selection
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.intersection
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.inversion
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.invert
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.is_transposed_subset
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.is_transposed_superset
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.isdisjoint
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.issubset
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.issuperset
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.item_class
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.items
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.markup
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.multiply
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.order_by
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.quality_pair
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.root
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.root_string
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.symmetric_difference
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.transpose
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.union
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__and__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__contains__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__eq__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__format__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__ge__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__gt__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__hash__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__iter__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__le__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__len__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__lt__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__ne__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__or__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__repr__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__str__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__sub__
      ~abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__xor__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.bass

.. autoattribute:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.cardinality

.. autoattribute:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.chord_quality

.. autoattribute:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.extent

.. autoattribute:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.figured_bass

.. autoattribute:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.inversion

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.items

.. autoattribute:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.markup

.. autoattribute:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.quality_pair

.. autoattribute:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.root

.. autoattribute:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.root_string

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.difference

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.intersection

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.invert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.is_transposed_subset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.is_transposed_superset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.isdisjoint

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.issubset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.issuperset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.multiply

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.order_by

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.symmetric_difference

.. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.transpose

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.union

Class & static methods
----------------------

.. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.cardinality_to_extent

.. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.extent_to_cardinality

.. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.extent_to_extent_name

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__contains__

.. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__gt__

.. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__lt__

.. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__or__

.. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__str__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__sub__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass.__xor__
