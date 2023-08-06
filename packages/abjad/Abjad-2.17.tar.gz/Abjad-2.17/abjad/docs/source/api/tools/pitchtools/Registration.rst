.. currentmodule:: abjad.tools.pitchtools

Registration
============

.. autoclass:: Registration

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
              "abjad.tools.pitchtools.Registration.Registration" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>Registration</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.pitchtools.Registration.Registration";
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

      ~abjad.tools.pitchtools.Registration.Registration.append
      ~abjad.tools.pitchtools.Registration.Registration.count
      ~abjad.tools.pitchtools.Registration.Registration.extend
      ~abjad.tools.pitchtools.Registration.Registration.index
      ~abjad.tools.pitchtools.Registration.Registration.insert
      ~abjad.tools.pitchtools.Registration.Registration.item_class
      ~abjad.tools.pitchtools.Registration.Registration.items
      ~abjad.tools.pitchtools.Registration.Registration.keep_sorted
      ~abjad.tools.pitchtools.Registration.Registration.pop
      ~abjad.tools.pitchtools.Registration.Registration.remove
      ~abjad.tools.pitchtools.Registration.Registration.reverse
      ~abjad.tools.pitchtools.Registration.Registration.sort
      ~abjad.tools.pitchtools.Registration.Registration.__call__
      ~abjad.tools.pitchtools.Registration.Registration.__contains__
      ~abjad.tools.pitchtools.Registration.Registration.__delitem__
      ~abjad.tools.pitchtools.Registration.Registration.__eq__
      ~abjad.tools.pitchtools.Registration.Registration.__format__
      ~abjad.tools.pitchtools.Registration.Registration.__getitem__
      ~abjad.tools.pitchtools.Registration.Registration.__hash__
      ~abjad.tools.pitchtools.Registration.Registration.__iadd__
      ~abjad.tools.pitchtools.Registration.Registration.__iter__
      ~abjad.tools.pitchtools.Registration.Registration.__len__
      ~abjad.tools.pitchtools.Registration.Registration.__ne__
      ~abjad.tools.pitchtools.Registration.Registration.__repr__
      ~abjad.tools.pitchtools.Registration.Registration.__reversed__
      ~abjad.tools.pitchtools.Registration.Registration.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.Registration.Registration.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.Registration.Registration.items

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.Registration.Registration.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.sort

Special methods
---------------

.. automethod:: abjad.tools.pitchtools.Registration.Registration.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.__eq__

.. automethod:: abjad.tools.pitchtools.Registration.Registration.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.Registration.Registration.__setitem__
