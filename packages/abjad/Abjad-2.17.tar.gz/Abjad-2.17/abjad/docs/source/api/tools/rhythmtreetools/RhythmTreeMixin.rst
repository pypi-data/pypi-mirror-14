.. currentmodule:: abjad.tools.rhythmtreetools

RhythmTreeMixin
===============

.. autoclass:: RhythmTreeMixin

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
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.QGridContainer.QGridContainer" [color=3,
                  group=2,
                  label=QGridContainer,
                  shape=box];
              "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf" [color=3,
                  group=2,
                  label=QGridLeaf,
                  shape=box];
          }
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" [color=4,
                  group=3,
                  label=RhythmTreeContainer,
                  shape=box];
              "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf" [color=4,
                  group=3,
                  label=RhythmTreeLeaf,
                  shape=box];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>RhythmTreeMixin</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer";
              "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.rhythmtreetools.RhythmTreeLeaf.RhythmTreeLeaf";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin";
          "abjad.tools.rhythmtreetools.RhythmTreeContainer.RhythmTreeContainer" -> "abjad.tools.quantizationtools.QGridContainer.QGridContainer";
          "abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin" -> "abjad.tools.quantizationtools.QGridLeaf.QGridLeaf";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.duration
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.parentage_ratios
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.preprolated_duration
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.pretty_rtm_format
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.prolation
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.prolations
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.rtm_format
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.start_offset
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.stop_offset
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.__call__
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.__eq__
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.__format__
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.__hash__
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.__ne__
      ~abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.duration

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.parentage_ratios

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.pretty_rtm_format

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.prolation

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.prolations

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.rtm_format

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.start_offset

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.stop_offset

Read/write properties
---------------------

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.preprolated_duration

Special methods
---------------

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeMixin.RhythmTreeMixin.__repr__
