.. currentmodule:: abjad.tools.indicatortools

ClefInventory
=============

.. autoclass:: ClefInventory

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
              "abjad.tools.indicatortools.ClefInventory.ClefInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>ClefInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.indicatortools.ClefInventory.ClefInventory";
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

      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.append
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.count
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.extend
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.index
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.insert
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.item_class
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.items
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.keep_sorted
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.pop
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.remove
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.reverse
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.sort
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__contains__
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__delitem__
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__eq__
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__format__
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__getitem__
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__hash__
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__iadd__
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__illustrate__
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__iter__
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__len__
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__ne__
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__repr__
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__reversed__
      ~abjad.tools.indicatortools.ClefInventory.ClefInventory.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.ClefInventory.ClefInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.ClefInventory.ClefInventory.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.ClefInventory.ClefInventory.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__iadd__

.. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.ClefInventory.ClefInventory.__setitem__
