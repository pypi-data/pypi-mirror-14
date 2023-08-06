.. currentmodule:: abjad.tools.datastructuretools

TypedCounter
============

.. autoclass:: TypedCounter

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
              "abjad.tools.datastructuretools.TypedCounter.TypedCounter" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TypedCounter</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedCounter.TypedCounter";
          }
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.OffsetCounter.OffsetCounter" [color=4,
                  group=3,
                  label=OffsetCounter,
                  shape=box];
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector" [color=5,
                  group=4,
                  label=IntervalClassVector,
                  shape=box];
              "abjad.tools.pitchtools.IntervalVector.IntervalVector" [color=5,
                  group=4,
                  label=IntervalVector,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassVector.PitchClassVector" [color=5,
                  group=4,
                  label=PitchClassVector,
                  shape=box];
              "abjad.tools.pitchtools.PitchVector.PitchVector" [color=5,
                  group=4,
                  label=PitchVector,
                  shape=box];
              "abjad.tools.pitchtools.Vector.Vector" [color=5,
                  group=4,
                  label=Vector,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.IntervalVector.IntervalVector";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.PitchClassVector.PitchClassVector";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.PitchVector.PitchVector";
          }
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.RotationCounter.RotationCounter" [color=6,
                  group=5,
                  label=RotationCounter,
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
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.metertools.OffsetCounter.OffsetCounter";
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.pitchtools.Vector.Vector";
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.rhythmmakertools.RotationCounter.RotationCounter";
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

      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.clear
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.copy
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.elements
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.item_class
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.items
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.keys
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.most_common
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.subtract
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.update
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.values
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.viewitems
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.viewkeys
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.viewvalues
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__add__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__and__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__contains__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__delitem__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__eq__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__format__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__getitem__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__hash__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__iter__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__len__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__missing__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__ne__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__or__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__repr__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__setitem__
      ~abjad.tools.datastructuretools.TypedCounter.TypedCounter.__sub__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.item_class

Methods
-------

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.clear

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.copy

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.elements

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.items

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.keys

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.most_common

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.subtract

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.update

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.values

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.viewitems

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.viewkeys

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.viewvalues

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__add__

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__contains__

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__format__

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__len__

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__missing__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__ne__

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__repr__

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__setitem__

.. automethod:: abjad.tools.datastructuretools.TypedCounter.TypedCounter.__sub__
