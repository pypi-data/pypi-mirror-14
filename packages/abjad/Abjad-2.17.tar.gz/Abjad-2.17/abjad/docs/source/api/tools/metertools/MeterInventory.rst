.. currentmodule:: abjad.tools.metertools

MeterInventory
==============

.. autoclass:: MeterInventory

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
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=3,
                  group=2,
                  label=TypedList,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
          }
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.MeterInventory.MeterInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>MeterInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.metertools.MeterInventory.MeterInventory";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TypedList`

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.metertools.MeterInventory.MeterInventory.append
      ~abjad.tools.metertools.MeterInventory.MeterInventory.count
      ~abjad.tools.metertools.MeterInventory.MeterInventory.extend
      ~abjad.tools.metertools.MeterInventory.MeterInventory.index
      ~abjad.tools.metertools.MeterInventory.MeterInventory.insert
      ~abjad.tools.metertools.MeterInventory.MeterInventory.item_class
      ~abjad.tools.metertools.MeterInventory.MeterInventory.items
      ~abjad.tools.metertools.MeterInventory.MeterInventory.keep_sorted
      ~abjad.tools.metertools.MeterInventory.MeterInventory.pop
      ~abjad.tools.metertools.MeterInventory.MeterInventory.remove
      ~abjad.tools.metertools.MeterInventory.MeterInventory.reverse
      ~abjad.tools.metertools.MeterInventory.MeterInventory.sort
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__contains__
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__delitem__
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__eq__
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__format__
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__getitem__
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__hash__
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__iadd__
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__illustrate__
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__iter__
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__len__
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__ne__
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__repr__
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__reversed__
      ~abjad.tools.metertools.MeterInventory.MeterInventory.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.metertools.MeterInventory.MeterInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.metertools.MeterInventory.MeterInventory.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.metertools.MeterInventory.MeterInventory.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__iadd__

.. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MeterInventory.MeterInventory.__setitem__
