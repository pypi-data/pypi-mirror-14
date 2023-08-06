.. currentmodule:: abjad.tools.pitchtools

Vector
======

.. autoclass:: Vector

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
              "abjad.tools.datastructuretools.TypedCounter.TypedCounter" [color=3,
                  group=2,
                  label=TypedCounter,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedCounter.TypedCounter";
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector" [color=4,
                  group=3,
                  label=IntervalClassVector,
                  shape=box];
              "abjad.tools.pitchtools.IntervalVector.IntervalVector" [color=4,
                  group=3,
                  label=IntervalVector,
                  shape=box];
              "abjad.tools.pitchtools.PitchClassVector.PitchClassVector" [color=4,
                  group=3,
                  label=PitchClassVector,
                  shape=box];
              "abjad.tools.pitchtools.PitchVector.PitchVector" [color=4,
                  group=3,
                  label=PitchVector,
                  shape=box];
              "abjad.tools.pitchtools.Vector.Vector" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>Vector</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.IntervalVector.IntervalVector";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.PitchClassVector.PitchClassVector";
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.PitchVector.PitchVector";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.datastructuretools.TypedCounter.TypedCounter" -> "abjad.tools.pitchtools.Vector.Vector";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TypedCounter`

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.Vector.Vector.clear
      ~abjad.tools.pitchtools.Vector.Vector.copy
      ~abjad.tools.pitchtools.Vector.Vector.elements
      ~abjad.tools.pitchtools.Vector.Vector.from_selection
      ~abjad.tools.pitchtools.Vector.Vector.item_class
      ~abjad.tools.pitchtools.Vector.Vector.items
      ~abjad.tools.pitchtools.Vector.Vector.keys
      ~abjad.tools.pitchtools.Vector.Vector.most_common
      ~abjad.tools.pitchtools.Vector.Vector.subtract
      ~abjad.tools.pitchtools.Vector.Vector.update
      ~abjad.tools.pitchtools.Vector.Vector.values
      ~abjad.tools.pitchtools.Vector.Vector.viewitems
      ~abjad.tools.pitchtools.Vector.Vector.viewkeys
      ~abjad.tools.pitchtools.Vector.Vector.viewvalues
      ~abjad.tools.pitchtools.Vector.Vector.__add__
      ~abjad.tools.pitchtools.Vector.Vector.__and__
      ~abjad.tools.pitchtools.Vector.Vector.__contains__
      ~abjad.tools.pitchtools.Vector.Vector.__delitem__
      ~abjad.tools.pitchtools.Vector.Vector.__eq__
      ~abjad.tools.pitchtools.Vector.Vector.__format__
      ~abjad.tools.pitchtools.Vector.Vector.__getitem__
      ~abjad.tools.pitchtools.Vector.Vector.__hash__
      ~abjad.tools.pitchtools.Vector.Vector.__iter__
      ~abjad.tools.pitchtools.Vector.Vector.__len__
      ~abjad.tools.pitchtools.Vector.Vector.__missing__
      ~abjad.tools.pitchtools.Vector.Vector.__ne__
      ~abjad.tools.pitchtools.Vector.Vector.__or__
      ~abjad.tools.pitchtools.Vector.Vector.__repr__
      ~abjad.tools.pitchtools.Vector.Vector.__setitem__
      ~abjad.tools.pitchtools.Vector.Vector.__str__
      ~abjad.tools.pitchtools.Vector.Vector.__sub__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.Vector.Vector.item_class

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.clear

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.elements

.. automethod:: abjad.tools.pitchtools.Vector.Vector.from_selection

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.items

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.keys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.most_common

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.subtract

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.update

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.values

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.viewitems

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.viewkeys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.viewvalues

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__missing__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__setitem__

.. automethod:: abjad.tools.pitchtools.Vector.Vector.__str__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Vector.Vector.__sub__
