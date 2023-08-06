.. currentmodule:: abjad.tools.quantizationtools

QGridContainer
==============

.. autoclass:: QGridContainer

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
              "abjad.tools.quantizationtools.QGridContainer.QGridContainer" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>QGridContainer</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" [color=5,
                  group=4,
                  label=RhythmTreeContainer,
                  shape=box];
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

- :py:class:`abjad.tools.rhythmtreetools.RhythmTreeContainer`

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

      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.append
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.children
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.depth
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.depthwise_inventory
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.duration
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.extend
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.graph_order
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.improper_parentage
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.index
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.insert
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.leaves
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.name
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.nodes
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.parent
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.parentage_ratios
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.pop
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.preprolated_duration
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.pretty_rtm_format
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.prolation
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.prolations
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.proper_parentage
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.remove
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.root
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.rtm_format
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.start_offset
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.stop_offset
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__add__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__call__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__contains__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__copy__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__delitem__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__eq__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__format__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__getitem__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__graph__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__hash__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__iter__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__len__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__ne__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__repr__
      ~abjad.tools.quantizationtools.QGridContainer.QGridContainer.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.depthwise_inventory

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.duration

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.graph_order

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.leaves

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.nodes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.parentage_ratios

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.pretty_rtm_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.prolation

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.prolations

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.root

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.rtm_format

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.start_offset

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.stop_offset

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.preprolated_duration

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.remove

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QGridContainer.QGridContainer.__setitem__
