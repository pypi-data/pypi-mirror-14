.. currentmodule:: abjad.tools.quantizationtools

QuantizationJob
===============

.. autoclass:: QuantizationJob

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
              "abjad.tools.quantizationtools.QuantizationJob.QuantizationJob" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>QuantizationJob</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QuantizationJob.QuantizationJob";
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

      ~abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.job_id
      ~abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.q_event_proxies
      ~abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.q_grids
      ~abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.search_tree
      ~abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.__call__
      ~abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.__eq__
      ~abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.__format__
      ~abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.__hash__
      ~abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.__ne__
      ~abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.job_id

.. autoattribute:: abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.q_event_proxies

.. autoattribute:: abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.q_grids

.. autoattribute:: abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.search_tree

Special methods
---------------

.. automethod:: abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.__call__

.. automethod:: abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.__format__

.. automethod:: abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QuantizationJob.QuantizationJob.__repr__
