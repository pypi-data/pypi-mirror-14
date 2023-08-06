.. currentmodule:: abjad.tools.instrumenttools

PerformerInventory
==================

.. autoclass:: PerformerInventory

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
              "abjad.tools.instrumenttools.PerformerInventory.PerformerInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PerformerInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.instrumenttools.PerformerInventory.PerformerInventory";
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

      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.append
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.count
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.extend
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.get_instrument
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.index
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.insert
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.item_class
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.items
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.keep_sorted
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.pop
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.remove
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.reverse
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.sort
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__contains__
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__delitem__
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__eq__
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__format__
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__getitem__
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__hash__
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__iadd__
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__iter__
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__len__
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__ne__
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__repr__
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__reversed__
      ~abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.extend

.. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.get_instrument

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.PerformerInventory.PerformerInventory.__setitem__
