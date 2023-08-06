.. currentmodule:: abjad.tools.pitchtools

IntervalVector
==============

.. autoclass:: IntervalVector

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
              "abjad.tools.pitchtools.IntervalVector.IntervalVector" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>IntervalVector</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Vector.Vector" [color=4,
                  group=3,
                  label=Vector,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.IntervalVector.IntervalVector";
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

- :py:class:`abjad.tools.pitchtools.Vector`

- :py:class:`abjad.tools.datastructuretools.TypedCounter`

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.clear
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.copy
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.elements
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.from_selection
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.item_class
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.items
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.keys
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.most_common
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.subtract
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.update
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.values
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.viewitems
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.viewkeys
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.viewvalues
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__add__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__and__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__contains__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__delitem__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__eq__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__format__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__getitem__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__hash__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__iter__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__len__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__missing__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__ne__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__or__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__repr__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__setitem__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__str__
      ~abjad.tools.pitchtools.IntervalVector.IntervalVector.__sub__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.IntervalVector.IntervalVector.item_class

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.clear

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.elements

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.items

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.keys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.most_common

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.subtract

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.update

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.values

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.viewitems

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.viewkeys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.viewvalues

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__missing__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__or__

.. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__setitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__str__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalVector.IntervalVector.__sub__
