.. currentmodule:: abjad.tools.metertools

OffsetCounter
=============

.. autoclass:: OffsetCounter

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
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.OffsetCounter.OffsetCounter" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>OffsetCounter</B>>,
                  shape=box,
                  style="filled, rounded"];
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

      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.clear
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.copy
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.elements
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.item_class
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.items
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.keys
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.most_common
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.subtract
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.update
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.values
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.viewitems
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.viewkeys
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.viewvalues
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__add__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__and__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__contains__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__delitem__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__eq__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__format__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__getitem__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__hash__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__illustrate__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__iter__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__len__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__missing__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__ne__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__or__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__repr__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__setitem__
      ~abjad.tools.metertools.OffsetCounter.OffsetCounter.__sub__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.metertools.OffsetCounter.OffsetCounter.item_class

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.clear

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.elements

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.items

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.keys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.most_common

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.subtract

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.update

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.values

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.viewitems

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.viewkeys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.viewvalues

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__hash__

.. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__missing__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__setitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.OffsetCounter.OffsetCounter.__sub__
