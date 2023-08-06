.. currentmodule:: abjad.tools.pitchtools

Set
===

.. autoclass:: Set

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
              "abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet" [color=4,
                  group=3,
                  label=IntervalClassSet,
                  shape=box];
              "abjad.tools.pitchtools.IntervalSet.IntervalSet" [color=4,
                  group=3,
                  label=IntervalSet,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassSet.PitchClassSet" [color=4,
                  group=3,
                  label=PitchClassSet,
                  shape=box];
              "abjad.tools.pitchtools.PitchSet.PitchSet" [color=4,
                  group=3,
                  label=PitchSet,
                  shape=box];
              "abjad.tools.pitchtools.Set.Set" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>Set</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet";
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.IntervalSet.IntervalSet";
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.PitchClassSet.PitchClassSet";
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.PitchSet.PitchSet";
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

- :py:class:`abjad.tools.datastructuretools.TypedFrozenset`

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.Set.Set.copy
      ~abjad.tools.pitchtools.Set.Set.difference
      ~abjad.tools.pitchtools.Set.Set.from_selection
      ~abjad.tools.pitchtools.Set.Set.intersection
      ~abjad.tools.pitchtools.Set.Set.isdisjoint
      ~abjad.tools.pitchtools.Set.Set.issubset
      ~abjad.tools.pitchtools.Set.Set.issuperset
      ~abjad.tools.pitchtools.Set.Set.item_class
      ~abjad.tools.pitchtools.Set.Set.items
      ~abjad.tools.pitchtools.Set.Set.symmetric_difference
      ~abjad.tools.pitchtools.Set.Set.union
      ~abjad.tools.pitchtools.Set.Set.__and__
      ~abjad.tools.pitchtools.Set.Set.__contains__
      ~abjad.tools.pitchtools.Set.Set.__eq__
      ~abjad.tools.pitchtools.Set.Set.__format__
      ~abjad.tools.pitchtools.Set.Set.__ge__
      ~abjad.tools.pitchtools.Set.Set.__gt__
      ~abjad.tools.pitchtools.Set.Set.__hash__
      ~abjad.tools.pitchtools.Set.Set.__iter__
      ~abjad.tools.pitchtools.Set.Set.__le__
      ~abjad.tools.pitchtools.Set.Set.__len__
      ~abjad.tools.pitchtools.Set.Set.__lt__
      ~abjad.tools.pitchtools.Set.Set.__ne__
      ~abjad.tools.pitchtools.Set.Set.__or__
      ~abjad.tools.pitchtools.Set.Set.__repr__
      ~abjad.tools.pitchtools.Set.Set.__str__
      ~abjad.tools.pitchtools.Set.Set.__sub__
      ~abjad.tools.pitchtools.Set.Set.__xor__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.Set.Set.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.Set.Set.items

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.difference

.. automethod:: abjad.tools.pitchtools.Set.Set.from_selection

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.intersection

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.isdisjoint

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.issubset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.issuperset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.symmetric_difference

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.union

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__repr__

.. automethod:: abjad.tools.pitchtools.Set.Set.__str__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__sub__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Set.Set.__xor__
