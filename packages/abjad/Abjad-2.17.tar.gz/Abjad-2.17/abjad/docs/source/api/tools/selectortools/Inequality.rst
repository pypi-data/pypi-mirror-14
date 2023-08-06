.. currentmodule:: abjad.tools.selectortools

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_selectortools {
              graph [label=selectortools];
              "abjad.tools.selectortools.DurationInequality.DurationInequality" [color=3,
                  group=2,
                  label=DurationInequality,
                  shape=box];
              "abjad.tools.selectortools.Inequality.Inequality" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Inequality</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.selectortools.LengthInequality.LengthInequality" [color=3,
                  group=2,
                  label=LengthInequality,
                  shape=box];
              "abjad.tools.selectortools.Inequality.Inequality" -> "abjad.tools.selectortools.DurationInequality.DurationInequality";
              "abjad.tools.selectortools.Inequality.Inequality" -> "abjad.tools.selectortools.LengthInequality.LengthInequality";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.selectortools.Inequality.Inequality";
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

      ~abjad.tools.selectortools.Inequality.Inequality.operator_string
      ~abjad.tools.selectortools.Inequality.Inequality.__call__
      ~abjad.tools.selectortools.Inequality.Inequality.__copy__
      ~abjad.tools.selectortools.Inequality.Inequality.__eq__
      ~abjad.tools.selectortools.Inequality.Inequality.__format__
      ~abjad.tools.selectortools.Inequality.Inequality.__hash__
      ~abjad.tools.selectortools.Inequality.Inequality.__ne__
      ~abjad.tools.selectortools.Inequality.Inequality.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.selectortools.Inequality.Inequality.operator_string

Special methods
---------------

.. automethod:: abjad.tools.selectortools.Inequality.Inequality.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectortools.Inequality.Inequality.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectortools.Inequality.Inequality.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectortools.Inequality.Inequality.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectortools.Inequality.Inequality.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectortools.Inequality.Inequality.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.selectortools.Inequality.Inequality.__repr__
