.. currentmodule:: abjad.tools.scoretools

NoteHeadInventory
=================

.. autoclass:: NoteHeadInventory

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
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>NoteHeadInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory";
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

      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.append
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.client
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.count
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.extend
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.get
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.index
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.insert
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.item_class
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.items
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.keep_sorted
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.pop
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.remove
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.reverse
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.sort
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__contains__
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__delitem__
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__eq__
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__format__
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__getitem__
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__hash__
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__iadd__
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__iter__
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__len__
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__ne__
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__repr__
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__reversed__
      ~abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__setitem__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.client

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.extend

.. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.get

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHeadInventory.NoteHeadInventory.__setitem__
