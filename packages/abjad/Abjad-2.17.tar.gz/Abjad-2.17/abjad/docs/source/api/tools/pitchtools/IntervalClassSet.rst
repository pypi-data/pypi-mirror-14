.. currentmodule:: abjad.tools.pitchtools

IntervalClassSet
================

.. autoclass:: IntervalClassSet

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
              "abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>IntervalClassSet</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Set.Set" [color=4,
                  group=3,
                  label=Set,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet";
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

      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.copy
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.difference
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.from_selection
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.intersection
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.isdisjoint
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.issubset
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.issuperset
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.item_class
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.items
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.symmetric_difference
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.union
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__and__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__contains__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__eq__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__format__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__ge__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__gt__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__hash__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__iter__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__le__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__len__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__lt__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__ne__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__or__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__repr__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__str__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__sub__
      ~abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__xor__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.items

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.difference

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.intersection

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.isdisjoint

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.issubset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.issuperset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.symmetric_difference

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.union

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__str__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__sub__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassSet.IntervalClassSet.__xor__
