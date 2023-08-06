.. currentmodule:: abjad.tools.quantizationtools

JobHandler
==========

.. autoclass:: JobHandler

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
              "abjad.tools.quantizationtools.JobHandler.JobHandler" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>JobHandler</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.ParallelJobHandler.ParallelJobHandler" [color=3,
                  group=2,
                  label=ParallelJobHandler,
                  shape=box];
              "abjad.tools.quantizationtools.SerialJobHandler.SerialJobHandler" [color=3,
                  group=2,
                  label=SerialJobHandler,
                  shape=box];
              "abjad.tools.quantizationtools.JobHandler.JobHandler" -> "abjad.tools.quantizationtools.ParallelJobHandler.ParallelJobHandler";
              "abjad.tools.quantizationtools.JobHandler.JobHandler" -> "abjad.tools.quantizationtools.SerialJobHandler.SerialJobHandler";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.JobHandler.JobHandler";
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

      ~abjad.tools.quantizationtools.JobHandler.JobHandler.__call__
      ~abjad.tools.quantizationtools.JobHandler.JobHandler.__eq__
      ~abjad.tools.quantizationtools.JobHandler.JobHandler.__format__
      ~abjad.tools.quantizationtools.JobHandler.JobHandler.__hash__
      ~abjad.tools.quantizationtools.JobHandler.JobHandler.__ne__
      ~abjad.tools.quantizationtools.JobHandler.JobHandler.__repr__

Special methods
---------------

.. automethod:: abjad.tools.quantizationtools.JobHandler.JobHandler.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.JobHandler.JobHandler.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.JobHandler.JobHandler.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.JobHandler.JobHandler.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.JobHandler.JobHandler.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.JobHandler.JobHandler.__repr__
