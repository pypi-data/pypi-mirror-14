.. currentmodule:: abjad.tools.timespantools

TimespanInventory
=================

.. autoclass:: TimespanInventory

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
              "abjad.tools.timespantools.TimespanInventory.TimespanInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>TimespanInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.timespantools.TimespanInventory.TimespanInventory";
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

      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.all_are_contiguous
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.all_are_nonoverlapping
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.all_are_well_formed
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.append
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.axis
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.clip_timespan_durations
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.compute_logical_and
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.compute_logical_or
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.compute_logical_xor
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.compute_overlap_factor
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.compute_overlap_factor_mapping
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.count
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.count_offsets
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.duration
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.explode
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.extend
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.get_timespan_that_satisfies_time_relation
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.get_timespans_that_satisfy_time_relation
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.has_timespan_that_satisfies_time_relation
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.index
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.insert
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.is_sorted
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.item_class
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.items
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.keep_sorted
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.partition
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.pop
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.reflect
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.remove
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.remove_degenerate_timespans
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.repeat_to_stop_offset
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.reverse
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.rotate
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.round_offsets
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.scale
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.sort
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.split_at_offset
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.split_at_offsets
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.start_offset
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.stop_offset
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.stretch
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.timespan
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.translate
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.translate_offsets
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__and__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__contains__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__delitem__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__eq__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__format__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__getitem__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__hash__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__iadd__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__illustrate__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__iter__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__len__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__ne__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__repr__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__reversed__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__setitem__
      ~abjad.tools.timespantools.TimespanInventory.TimespanInventory.__sub__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.all_are_contiguous

.. autoattribute:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.all_are_nonoverlapping

.. autoattribute:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.all_are_well_formed

.. autoattribute:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.axis

.. autoattribute:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.duration

.. autoattribute:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.is_sorted

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.items

.. autoattribute:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.start_offset

.. autoattribute:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.stop_offset

.. autoattribute:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.timespan

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.keep_sorted

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.append

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.clip_timespan_durations

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.compute_logical_and

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.compute_logical_or

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.compute_logical_xor

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.compute_overlap_factor

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.compute_overlap_factor_mapping

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.count

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.count_offsets

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.explode

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.extend

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.get_timespan_that_satisfies_time_relation

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.get_timespans_that_satisfy_time_relation

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.has_timespan_that_satisfies_time_relation

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.insert

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.partition

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.pop

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.reflect

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.remove

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.remove_degenerate_timespans

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.repeat_to_stop_offset

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.reverse

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.rotate

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.round_offsets

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.scale

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.sort

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.split_at_offset

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.split_at_offsets

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.stretch

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.translate

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.translate_offsets

Special methods
---------------

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__iadd__

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__setitem__

.. automethod:: abjad.tools.timespantools.TimespanInventory.TimespanInventory.__sub__
