.. currentmodule:: abjad.tools.pitchtools

IntervalClassVector
===================

.. autoclass:: IntervalClassVector

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
              "abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>IntervalClassVector</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Vector.Vector" [color=4,
                  group=3,
                  label=Vector,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector";
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

      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.clear
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.copy
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.elements
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.from_selection
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.item_class
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.items
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.keys
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.most_common
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.subtract
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.update
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.values
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.viewitems
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.viewkeys
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.viewvalues
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__add__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__and__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__contains__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__delitem__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__eq__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__format__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__getitem__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__hash__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__iter__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__len__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__missing__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__ne__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__or__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__repr__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__setitem__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__str__
      ~abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__sub__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.item_class

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.clear

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.elements

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.items

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.keys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.most_common

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.subtract

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.update

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.values

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.viewitems

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.viewkeys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.viewvalues

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__missing__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__or__

.. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__setitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__str__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.IntervalClassVector.IntervalClassVector.__sub__
