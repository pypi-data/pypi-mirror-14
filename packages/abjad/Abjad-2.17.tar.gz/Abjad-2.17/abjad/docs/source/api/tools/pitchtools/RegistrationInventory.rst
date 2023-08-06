.. currentmodule:: abjad.tools.pitchtools

RegistrationInventory
=====================

.. autoclass:: RegistrationInventory

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
              "abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>RegistrationInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory";
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

      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.append
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.count
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.extend
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.index
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.insert
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.item_class
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.items
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.keep_sorted
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.pop
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.remove
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.reverse
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.sort
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__contains__
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__delitem__
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__eq__
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__format__
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__getitem__
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__hash__
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__iadd__
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__iter__
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__len__
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__ne__
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__repr__
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__reversed__
      ~abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.RegistrationInventory.RegistrationInventory.__setitem__
