.. currentmodule:: abjad.tools.metertools

MetricAccentKernel
==================

.. autoclass:: MetricAccentKernel

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>MetricAccentKernel</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.count_offsets_in_expr
      ~abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.duration
      ~abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.from_meter
      ~abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.kernel
      ~abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__call__
      ~abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__copy__
      ~abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__eq__
      ~abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__format__
      ~abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__hash__
      ~abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__ne__
      ~abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.duration

.. autoattribute:: abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.kernel

Class & static methods
----------------------

.. automethod:: abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.count_offsets_in_expr

.. automethod:: abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.from_meter

Special methods
---------------

.. automethod:: abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__copy__

.. automethod:: abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__format__

.. automethod:: abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.MetricAccentKernel.MetricAccentKernel.__repr__
