.. currentmodule:: abjad.tools.markuptools

MarkupInventory
===============

.. autoclass:: MarkupInventory

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
          subgraph cluster_markuptools {
              graph [label=markuptools];
              "abjad.tools.markuptools.MarkupInventory.MarkupInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>MarkupInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.markuptools.MarkupInventory.MarkupInventory";
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

      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.append
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.count
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.extend
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.index
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.insert
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.item_class
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.items
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.keep_sorted
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.pop
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.remove
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.reverse
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.sort
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__contains__
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__delitem__
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__eq__
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__format__
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__getitem__
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__hash__
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__iadd__
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__illustrate__
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__iter__
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__len__
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__ne__
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__repr__
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__reversed__
      ~abjad.tools.markuptools.MarkupInventory.MarkupInventory.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__iadd__

.. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupInventory.MarkupInventory.__setitem__
