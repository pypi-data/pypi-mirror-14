.. currentmodule:: abjad.tools.quantizationtools

QGridLeaf
=========

.. autoclass:: QGridLeaf

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
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=3,
                  group=2,
                  label=TreeNode,
                  shape=box];
          }
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>QGridLeaf</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" [color=5,
                  group=4,
                  label=RhythmTreeMixin,
                  shape=oval,
                  style=bold];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TreeNode.TreeNode";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin";
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf";
          "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.rhythmtreetools.RhythmTreeMixin`

- :py:class:`abjad.tools.datastructuretools.TreeNode`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.depth
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.depthwise_inventory
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.duration
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.graph_order
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.improper_parentage
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.is_divisible
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.name
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.parent
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.parentage_ratios
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.preceding_q_event_proxies
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.preprolated_duration
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.pretty_rtm_format
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.prolation
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.prolations
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.proper_parentage
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.q_event_proxies
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.root
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.rtm_format
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.start_offset
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.stop_offset
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.succeeding_q_event_proxies
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__call__
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__copy__
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__eq__
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__format__
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__graph__
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__hash__
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__ne__
      ~abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.duration

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.parentage_ratios

.. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.preceding_q_event_proxies

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.pretty_rtm_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.prolation

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.prolations

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.proper_parentage

.. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.q_event_proxies

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.root

.. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.rtm_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.start_offset

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.stop_offset

.. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.succeeding_q_event_proxies

Read/write properties
---------------------

.. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.is_divisible

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.preprolated_duration

Special methods
---------------

.. automethod:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__format__

.. automethod:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridLeaf.QGridLeaf.__repr__
