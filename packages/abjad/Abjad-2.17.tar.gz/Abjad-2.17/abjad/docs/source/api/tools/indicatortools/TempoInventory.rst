.. currentmodule:: abjad.tools.indicatortools

TempoInventory
==============

.. autoclass:: TempoInventory

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
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.TempoInventory.TempoInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>TempoInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.indicatortools.TempoInventory.TempoInventory";
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

      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.append
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.count
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.extend
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.index
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.insert
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.item_class
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.items
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.keep_sorted
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.pop
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.remove
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.reverse
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.sort
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__contains__
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__delitem__
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__eq__
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__format__
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__getitem__
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__hash__
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__iadd__
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__illustrate__
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__iter__
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__len__
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__ne__
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__repr__
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__reversed__
      ~abjad.tools.indicatortools.TempoInventory.TempoInventory.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.TempoInventory.TempoInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.TempoInventory.TempoInventory.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.TempoInventory.TempoInventory.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__iadd__

.. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TempoInventory.TempoInventory.__setitem__
