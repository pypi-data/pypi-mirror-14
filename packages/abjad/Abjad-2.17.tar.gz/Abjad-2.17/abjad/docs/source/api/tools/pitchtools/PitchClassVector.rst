.. currentmodule:: abjad.tools.pitchtools

PitchClassVector
================

.. autoclass:: PitchClassVector

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
              "abjad.tools.pitchtools.PitchClassVector.PitchClassVector" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PitchClassVector</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.pitchtools.Vector.Vector" [color=4,
                  group=3,
                  label=Vector,
                  shape=oval,
                  style=bold];
              "abjad.tools.pitchtools.Vector.Vector" -> "abjad.tools.pitchtools.PitchClassVector.PitchClassVector";
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

      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.clear
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.copy
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.elements
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.from_selection
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.item_class
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.items
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.keys
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.most_common
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.subtract
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.update
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.values
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.viewitems
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.viewkeys
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.viewvalues
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__add__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__and__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__contains__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__delitem__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__eq__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__format__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__getitem__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__hash__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__iter__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__len__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__missing__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__ne__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__or__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__repr__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__setitem__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__str__
      ~abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__sub__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.item_class

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.clear

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.elements

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.items

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.keys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.most_common

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.subtract

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.update

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.values

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.viewitems

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.viewkeys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.viewvalues

Class & static methods
----------------------

.. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.from_selection

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__eq__

.. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__missing__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__or__

.. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__setitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__str__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassVector.PitchClassVector.__sub__
