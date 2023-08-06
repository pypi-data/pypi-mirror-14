.. currentmodule:: abjad.tools.pitchtools

PitchClassSet
=============

.. autoclass:: PitchClassSet

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
              "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PitchClassSet</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Set.Set" [color=4,
                  group=3,
                  label=Set,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.PitchClassSet.PitchClassSet";
          }
          subgraph cluster_tonalanalysistools {
              graph [label=tonalanalysistools];
              "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass" [color=5,
                  group=4,
                  label=RootedChordClass,
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
          "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" -> "abjad.tools.pitchtools.Set.Set";
          "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" -> "abjad.tools.tonalanalysistools.RootedChordClass.RootedChordClass";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

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

      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.copy
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.difference
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.from_selection
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.intersection
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.invert
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.is_transposed_subset
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.is_transposed_superset
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.isdisjoint
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.issubset
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.issuperset
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.item_class
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.items
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.multiply
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.order_by
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.symmetric_difference
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.transpose
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.union
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__and__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__contains__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__eq__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__format__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__ge__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__gt__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__hash__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__iter__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__le__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__len__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__lt__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__ne__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__or__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__repr__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__str__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__sub__
      ~abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__xor__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.items

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.difference

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.intersection

.. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.invert

.. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.is_transposed_subset

.. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.is_transposed_superset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.isdisjoint

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.issubset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.issuperset

.. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.multiply

.. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.order_by

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.symmetric_difference

.. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.transpose

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.union

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__gt__

.. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__str__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__sub__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassSet.PitchClassSet.__xor__
