.. currentmodule:: abjad.tools.pitchtools

IntervalSet
===========

.. autoclass:: IntervalSet

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
              "abjad.tools.pitchtools.IntervalSet.IntervalSet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>IntervalSet</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Set.Set" [color=4,
                  group=3,
                  label=Set,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Set.Set" -> "abjad.tools.pitchtools.IntervalSet.IntervalSet";
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

      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.copy
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.difference
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.from_selection
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.intersection
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.isdisjoint
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.issubset
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.issuperset
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.item_class
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.items
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.symmetric_difference
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.union
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__and__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__contains__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__eq__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__format__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__ge__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__gt__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__hash__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__iter__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__le__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__len__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__lt__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__ne__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__or__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__repr__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__str__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__sub__
      ~abjad.tools.pitchtools.IntervalSet.IntervalSet.__xor__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.IntervalSet.IntervalSet.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.IntervalSet.IntervalSet.items

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.difference

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.intersection

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.isdisjoint

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.issubset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.issuperset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.symmetric_difference

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.union

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__str__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__sub__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalSet.IntervalSet.__xor__
