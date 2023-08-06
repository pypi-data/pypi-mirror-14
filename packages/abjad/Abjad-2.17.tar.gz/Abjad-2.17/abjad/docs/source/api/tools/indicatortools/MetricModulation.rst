.. currentmodule:: abjad.tools.indicatortools

MetricModulation
================

.. autoclass:: MetricModulation

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
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.MetricModulation.MetricModulation" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>MetricModulation</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.indicatortools.MetricModulation.MetricModulation";
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

      ~abjad.tools.indicatortools.MetricModulation.MetricModulation.default_scope
      ~abjad.tools.indicatortools.MetricModulation.MetricModulation.left_markup
      ~abjad.tools.indicatortools.MetricModulation.MetricModulation.left_rhythm
      ~abjad.tools.indicatortools.MetricModulation.MetricModulation.ratio
      ~abjad.tools.indicatortools.MetricModulation.MetricModulation.right_markup
      ~abjad.tools.indicatortools.MetricModulation.MetricModulation.right_rhythm
      ~abjad.tools.indicatortools.MetricModulation.MetricModulation.__eq__
      ~abjad.tools.indicatortools.MetricModulation.MetricModulation.__format__
      ~abjad.tools.indicatortools.MetricModulation.MetricModulation.__hash__
      ~abjad.tools.indicatortools.MetricModulation.MetricModulation.__illustrate__
      ~abjad.tools.indicatortools.MetricModulation.MetricModulation.__ne__
      ~abjad.tools.indicatortools.MetricModulation.MetricModulation.__repr__
      ~abjad.tools.indicatortools.MetricModulation.MetricModulation.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.indicatortools.MetricModulation.MetricModulation.default_scope

.. autoattribute:: abjad.tools.indicatortools.MetricModulation.MetricModulation.left_markup

.. autoattribute:: abjad.tools.indicatortools.MetricModulation.MetricModulation.left_rhythm

.. autoattribute:: abjad.tools.indicatortools.MetricModulation.MetricModulation.ratio

.. autoattribute:: abjad.tools.indicatortools.MetricModulation.MetricModulation.right_markup

.. autoattribute:: abjad.tools.indicatortools.MetricModulation.MetricModulation.right_rhythm

Special methods
---------------

.. automethod:: abjad.tools.indicatortools.MetricModulation.MetricModulation.__eq__

.. automethod:: abjad.tools.indicatortools.MetricModulation.MetricModulation.__format__

.. automethod:: abjad.tools.indicatortools.MetricModulation.MetricModulation.__hash__

.. automethod:: abjad.tools.indicatortools.MetricModulation.MetricModulation.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetricModulation.MetricModulation.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.MetricModulation.MetricModulation.__repr__

.. automethod:: abjad.tools.indicatortools.MetricModulation.MetricModulation.__str__
