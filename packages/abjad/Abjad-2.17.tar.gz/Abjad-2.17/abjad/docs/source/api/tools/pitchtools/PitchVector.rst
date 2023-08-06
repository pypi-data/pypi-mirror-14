.. currentmodule:: abjad.tools.pitchtools

PitchVector
===========

.. autoclass:: PitchVector

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
              "abjad.tools.pitchtools.PitchVector.PitchVector" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PitchVector</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Vector.Vector" [color=4,
                  group=3,
                  label=Vector,
                  shape=oval,
                  style=bold];
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

      ~abjad.tools.pitchtools.PitchVector.PitchVector.clear
      ~abjad.tools.pitchtools.PitchVector.PitchVector.copy
      ~abjad.tools.pitchtools.PitchVector.PitchVector.elements
      ~abjad.tools.pitchtools.PitchVector.PitchVector.from_selection
      ~abjad.tools.pitchtools.PitchVector.PitchVector.item_class
      ~abjad.tools.pitchtools.PitchVector.PitchVector.items
      ~abjad.tools.pitchtools.PitchVector.PitchVector.keys
      ~abjad.tools.pitchtools.PitchVector.PitchVector.most_common
      ~abjad.tools.pitchtools.PitchVector.PitchVector.subtract
      ~abjad.tools.pitchtools.PitchVector.PitchVector.update
      ~abjad.tools.pitchtools.PitchVector.PitchVector.values
      ~abjad.tools.pitchtools.PitchVector.PitchVector.viewitems
      ~abjad.tools.pitchtools.PitchVector.PitchVector.viewkeys
      ~abjad.tools.pitchtools.PitchVector.PitchVector.viewvalues
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__add__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__and__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__contains__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__delitem__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__eq__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__format__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__getitem__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__hash__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__iter__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__len__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__missing__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__ne__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__or__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__repr__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__setitem__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__str__
      ~abjad.tools.pitchtools.PitchVector.PitchVector.__sub__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchVector.PitchVector.item_class

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.clear

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.elements

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.items

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.keys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.most_common

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.subtract

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.update

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.values

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.viewitems

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.viewkeys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.viewvalues

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__missing__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__or__

.. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__setitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__str__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchVector.PitchVector.__sub__
