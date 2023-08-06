.. currentmodule:: abjad.tools.pitchtools

PitchSet
========

.. autoclass:: PitchSet

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
              "abjad.tools.pitchtools.PitchSet.PitchSet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PitchSet</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Set.Set" [color=4,
                  group=3,
                  label=Set,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.PitchSet.PitchSet";
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

      ~abjad.tools.pitchtools.PitchSet.PitchSet.copy
      ~abjad.tools.pitchtools.PitchSet.PitchSet.difference
      ~abjad.tools.pitchtools.PitchSet.PitchSet.duplicate_pitch_classes
      ~abjad.tools.pitchtools.PitchSet.PitchSet.from_selection
      ~abjad.tools.pitchtools.PitchSet.PitchSet.hertz
      ~abjad.tools.pitchtools.PitchSet.PitchSet.intersection
      ~abjad.tools.pitchtools.PitchSet.PitchSet.invert
      ~abjad.tools.pitchtools.PitchSet.PitchSet.is_equivalent_under_transposition
      ~abjad.tools.pitchtools.PitchSet.PitchSet.is_pitch_class_unique
      ~abjad.tools.pitchtools.PitchSet.PitchSet.isdisjoint
      ~abjad.tools.pitchtools.PitchSet.PitchSet.issubset
      ~abjad.tools.pitchtools.PitchSet.PitchSet.issuperset
      ~abjad.tools.pitchtools.PitchSet.PitchSet.item_class
      ~abjad.tools.pitchtools.PitchSet.PitchSet.items
      ~abjad.tools.pitchtools.PitchSet.PitchSet.register
      ~abjad.tools.pitchtools.PitchSet.PitchSet.symmetric_difference
      ~abjad.tools.pitchtools.PitchSet.PitchSet.transpose
      ~abjad.tools.pitchtools.PitchSet.PitchSet.union
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__and__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__contains__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__eq__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__format__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__ge__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__gt__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__hash__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__iter__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__le__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__len__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__lt__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__ne__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__or__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__repr__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__str__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__sub__
      ~abjad.tools.pitchtools.PitchSet.PitchSet.__xor__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.pitchtools.PitchSet.PitchSet.duplicate_pitch_classes

.. autoattribute:: abjad.tools.pitchtools.PitchSet.PitchSet.hertz

.. autoattribute:: abjad.tools.pitchtools.PitchSet.PitchSet.is_pitch_class_unique

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchSet.PitchSet.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchSet.PitchSet.items

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.difference

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.intersection

.. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.invert

.. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.is_equivalent_under_transposition

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.isdisjoint

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.issubset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.issuperset

.. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.register

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.symmetric_difference

.. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.transpose

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.union

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__str__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__sub__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchSet.PitchSet.__xor__
