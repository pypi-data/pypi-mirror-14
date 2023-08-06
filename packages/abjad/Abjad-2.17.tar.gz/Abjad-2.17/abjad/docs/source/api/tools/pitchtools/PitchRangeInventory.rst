.. currentmodule:: abjad.tools.pitchtools

PitchRangeInventory
===================

.. autoclass:: PitchRangeInventory

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
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PitchRangeInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory";
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

      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.append
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.count
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.extend
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.index
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.insert
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.item_class
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.items
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.keep_sorted
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.pop
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.remove
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.reverse
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.sort
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__contains__
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__delitem__
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__eq__
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__format__
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__getitem__
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__hash__
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__iadd__
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__illustrate__
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__iter__
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__len__
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__ne__
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__repr__
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__reversed__
      ~abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__iadd__

.. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchRangeInventory.PitchRangeInventory.__setitem__
