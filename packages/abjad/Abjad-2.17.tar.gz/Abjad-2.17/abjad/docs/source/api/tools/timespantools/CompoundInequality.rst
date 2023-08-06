.. currentmodule:: abjad.tools.timespantools

CompoundInequality
==================

.. autoclass:: CompoundInequality

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
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.CompoundInequality.CompoundInequality" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>CompoundInequality</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.timespantools.CompoundInequality.CompoundInequality";
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

      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.append
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.count
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.evaluate
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.evaluate_offset_inequality
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.extend
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.get_offset_indices
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.index
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.insert
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.item_class
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.items
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.keep_sorted
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.logical_operator
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.pop
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.remove
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.reverse
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.sort
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.__contains__
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.__delitem__
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.__eq__
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.__format__
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.__getitem__
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.__hash__
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.__iadd__
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.__iter__
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.__len__
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.__ne__
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.__repr__
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.__reversed__
      ~abjad.tools.timespantools.CompoundInequality.CompoundInequality.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.items

.. autoattribute:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.logical_operator

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.count

.. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.evaluate

.. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.evaluate_offset_inequality

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.extend

.. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.get_offset_indices

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.sort

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.__iadd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.CompoundInequality.CompoundInequality.__setitem__
