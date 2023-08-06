.. currentmodule:: abjad.tools.pitchtools

PitchArrayInventory
===================

.. autoclass:: PitchArrayInventory

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
              "abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PitchArrayInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory";
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

      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.append
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.count
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.extend
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.index
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.insert
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.item_class
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.items
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.keep_sorted
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.pop
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.remove
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.reverse
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.sort
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.to_score
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__contains__
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__delitem__
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__eq__
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__format__
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__getitem__
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__hash__
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__iadd__
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__iter__
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__len__
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__ne__
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__repr__
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__reversed__
      ~abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.sort

.. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.to_score

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchArrayInventory.PitchArrayInventory.__setitem__
