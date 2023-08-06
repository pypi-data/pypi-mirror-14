.. currentmodule:: abjad.tools.rhythmtreetools

RhythmTreeContainer
===================

.. autoclass:: RhythmTreeContainer

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
              "abjad.tools.datastructuretools.TreeContainer.TreeContainer" [color=3,
                  group=2,
                  label=TreeContainer,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" [color=3,
                  group=2,
                  label=TreeNode,
                  shape=box];
              "abjad.tools.datastructuretools.TreeNode.TreeNode" -> "abjad.tools.datastructuretools.TreeContainer.TreeContainer";
          }
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.QGridContainer.QGridContainer" [color=4,
                  group=3,
                  label=QGridContainer,
                  shape=box];
          }
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" [color=black,
                  fontcolor=white,
                  group=4,
                  label=<<B>RhythmTreeContainer</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" [color=5,
                  group=4,
                  label=RhythmTreeMixin,
                  shape=oval,
                  style=bold];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer";
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
          "abjad.tools.datastructuretools.TreeContainer.TreeContainer" -> "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer";
          "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" -> "abjad.tools.quantizationtools.QGridContainer.QGridContainer";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.rhythmtreetools.RhythmTreeMixin`

- :py:class:`abjad.tools.datastructuretools.TreeContainer`

- :py:class:`abjad.tools.datastructuretools.TreeNode`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.append
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.children
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.depth
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.depthwise_inventory
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.duration
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.extend
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.graph_order
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.improper_parentage
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.index
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.insert
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.leaves
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.name
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.nodes
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.parent
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.parentage_ratios
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.pop
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.preprolated_duration
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.pretty_rtm_format
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.prolation
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.prolations
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.proper_parentage
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.remove
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.root
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.rtm_format
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.start_offset
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.stop_offset
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__add__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__call__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__contains__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__copy__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__delitem__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__eq__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__format__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__getitem__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__graph__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__hash__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__iter__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__len__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__ne__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__repr__
      ~abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.duration

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.leaves

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.parentage_ratios

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.pretty_rtm_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.prolation

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.prolations

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.root

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.rtm_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.start_offset

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.stop_offset

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.preprolated_duration

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.remove

Special methods
---------------

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__add__

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__getitem__

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__ne__

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__repr__

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer.__setitem__
