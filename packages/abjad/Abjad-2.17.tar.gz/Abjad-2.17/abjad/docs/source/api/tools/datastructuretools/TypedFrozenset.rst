.. currentmodule:: abjad.tools.datastructuretools

TypedFrozenset
==============

.. autoclass:: TypedFrozenset

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
              "abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TypedFrozenset</B>>,
                  shape=box,
                  style="filled, rounded"];
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
              "abjad.tools.pitchtools.Set.Set" [color=4,
                  group=3,
                  label=Set,
                  shape=oval,
                  style=bold];
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

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.copy
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.difference
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.intersection
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.isdisjoint
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.issubset
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.issuperset
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.item_class
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.items
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.symmetric_difference
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.union
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__and__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__contains__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__eq__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__format__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__ge__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__gt__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__hash__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__iter__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__le__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__len__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__lt__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__ne__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__or__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__repr__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__sub__
      ~abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__xor__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.items

Methods
-------

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.copy

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.difference

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.intersection

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.isdisjoint

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.issubset

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.issuperset

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.symmetric_difference

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.union

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__format__

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__ge__

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__gt__

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__iter__

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__len__

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__lt__

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__ne__

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__repr__

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__sub__

.. automethod:: abjad.tools.datastructuretools.TypedFrozenset.TypedFrozenset.__xor__
