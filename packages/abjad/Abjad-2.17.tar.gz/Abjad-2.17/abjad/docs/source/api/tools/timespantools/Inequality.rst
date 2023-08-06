.. currentmodule:: abjad.tools.timespantools

Inequality
==========

.. autoclass:: Inequality

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
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.Inequality.Inequality" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Inequality</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.timespantools.Inequality.Inequality";
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

      ~abjad.tools.timespantools.Inequality.Inequality.evaluate
      ~abjad.tools.timespantools.Inequality.Inequality.evaluate_offset_inequality
      ~abjad.tools.timespantools.Inequality.Inequality.get_offset_indices
      ~abjad.tools.timespantools.Inequality.Inequality.template
      ~abjad.tools.timespantools.Inequality.Inequality.__eq__
      ~abjad.tools.timespantools.Inequality.Inequality.__format__
      ~abjad.tools.timespantools.Inequality.Inequality.__hash__
      ~abjad.tools.timespantools.Inequality.Inequality.__ne__
      ~abjad.tools.timespantools.Inequality.Inequality.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.timespantools.Inequality.Inequality.template

Methods
-------

.. automethod:: abjad.tools.timespantools.Inequality.Inequality.evaluate

.. automethod:: abjad.tools.timespantools.Inequality.Inequality.evaluate_offset_inequality

.. automethod:: abjad.tools.timespantools.Inequality.Inequality.get_offset_indices

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.Inequality.Inequality.__eq__

.. automethod:: abjad.tools.timespantools.Inequality.Inequality.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.Inequality.Inequality.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.Inequality.Inequality.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.timespantools.Inequality.Inequality.__repr__
