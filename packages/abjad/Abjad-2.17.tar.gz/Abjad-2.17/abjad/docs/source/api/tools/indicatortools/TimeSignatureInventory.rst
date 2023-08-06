.. currentmodule:: abjad.tools.indicatortools

TimeSignatureInventory
======================

.. autoclass:: TimeSignatureInventory

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
              "abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>TimeSignatureInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory";
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

      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.append
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.count
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.extend
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.index
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.insert
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.item_class
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.items
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.keep_sorted
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.pop
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.remove
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.reverse
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.sort
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__contains__
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__delitem__
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__eq__
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__format__
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__getitem__
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__hash__
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__iadd__
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__illustrate__
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__iter__
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__len__
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__ne__
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__repr__
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__reversed__
      ~abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__iadd__

.. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.TimeSignatureInventory.TimeSignatureInventory.__setitem__
