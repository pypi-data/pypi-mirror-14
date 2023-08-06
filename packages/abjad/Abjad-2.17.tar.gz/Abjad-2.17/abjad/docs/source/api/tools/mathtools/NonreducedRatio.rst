.. currentmodule:: abjad.tools.mathtools

NonreducedRatio
===============

.. autoclass:: NonreducedRatio

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
          subgraph cluster_mathtools {
              graph [label=mathtools];
              "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NonreducedRatio</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.Ratio.Ratio" [color=3,
                  group=2,
                  label=Ratio,
                  shape=box];
              "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio" -> "abjad.tools.mathtools.Ratio.Ratio";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio";
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

      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.count
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.index
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.multipliers
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.numbers
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__contains__
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__copy__
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__eq__
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__format__
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__getitem__
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__hash__
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__iter__
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__len__
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__ne__
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__repr__
      ~abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__reversed__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.multipliers

.. autoattribute:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.numbers

Methods
-------

.. automethod:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.count

.. automethod:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.index

Special methods
---------------

.. automethod:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__copy__

.. automethod:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__eq__

.. automethod:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__format__

.. automethod:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__getitem__

.. automethod:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__hash__

.. automethod:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__iter__

.. automethod:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__repr__

.. automethod:: abjad.tools.mathtools.NonreducedRatio.NonreducedRatio.__reversed__
