.. currentmodule:: abjad.tools.rhythmtreetools

RhythmTreeLeaf
==============

.. autoclass:: RhythmTreeLeaf

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
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>RhythmTreeLeaf</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" [color=4,
                  group=3,
                  label=RhythmTreeMixin,
                  shape=oval,
                  style=bold];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf";
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
          "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf";
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

      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.depth
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.depthwise_inventory
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.duration
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.graph_order
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.improper_parentage
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.is_pitched
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.name
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.parent
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.parentage_ratios
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.preprolated_duration
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.pretty_rtm_format
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.prolation
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.prolations
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.proper_parentage
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.root
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.rtm_format
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.start_offset
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.stop_offset
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__call__
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__copy__
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__eq__
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__format__
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__graph__
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__hash__
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__ne__
      ~abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.duration

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.parentage_ratios

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.pretty_rtm_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.prolation

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.prolations

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.root

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.rtm_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.start_offset

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.stop_offset

Read/write properties
---------------------

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.is_pitched

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.preprolated_duration

Special methods
---------------

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__format__

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf.__repr__
