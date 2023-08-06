.. currentmodule:: abjad.tools.instrumenttools

InstrumentInventory
===================

.. autoclass:: InstrumentInventory

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
          subgraph cluster_instrumenttools {
              graph [label=instrumenttools];
              "abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>InstrumentInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory";
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

      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.append
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.count
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.extend
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.index
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.insert
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.item_class
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.items
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.keep_sorted
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.pop
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.remove
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.reverse
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.sort
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__contains__
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__delitem__
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__eq__
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__format__
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__getitem__
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__hash__
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__iadd__
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__iter__
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__len__
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__ne__
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__repr__
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__reversed__
      ~abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__eq__

.. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__ne__

.. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory.__setitem__
