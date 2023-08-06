.. currentmodule:: abjad.tools.selectiontools

SelectionInventory
==================

.. autoclass:: SelectionInventory

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
          subgraph cluster_selectiontools {
              graph [label=selectiontools];
              "abjad.tools.selectiontools.SelectionInventory.SelectionInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>SelectionInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.selectiontools.SelectionInventory.SelectionInventory";
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

      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.append
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.count
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.extend
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.index
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.insert
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.item_class
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.items
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.keep_sorted
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.pop
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.remove
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.reverse
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.sort
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__contains__
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__delitem__
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__eq__
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__format__
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__getitem__
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__hash__
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__iadd__
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__iter__
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__len__
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__ne__
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__repr__
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__reversed__
      ~abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectiontools.SelectionInventory.SelectionInventory.__setitem__
