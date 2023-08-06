.. currentmodule:: abjad.tools.mathtools

Ratio
=====

.. autoclass:: Ratio

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
              "abjad.tools.mathtools.NonreducedRatio.NonreducedRatio" [color=3,
                  group=2,
                  label=NonreducedRatio,
                  shape=box];
              "abjad.tools.mathtools.Ratio.Ratio" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Ratio</B>>,
                  shape=box,
                  style="filled, rounded"];
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

- :py:class:`abjad.tools.mathtools.NonreducedRatio`

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.mathtools.Ratio.Ratio.count
      ~abjad.tools.mathtools.Ratio.Ratio.index
      ~abjad.tools.mathtools.Ratio.Ratio.multipliers
      ~abjad.tools.mathtools.Ratio.Ratio.numbers
      ~abjad.tools.mathtools.Ratio.Ratio.__contains__
      ~abjad.tools.mathtools.Ratio.Ratio.__copy__
      ~abjad.tools.mathtools.Ratio.Ratio.__eq__
      ~abjad.tools.mathtools.Ratio.Ratio.__format__
      ~abjad.tools.mathtools.Ratio.Ratio.__getitem__
      ~abjad.tools.mathtools.Ratio.Ratio.__hash__
      ~abjad.tools.mathtools.Ratio.Ratio.__iter__
      ~abjad.tools.mathtools.Ratio.Ratio.__len__
      ~abjad.tools.mathtools.Ratio.Ratio.__ne__
      ~abjad.tools.mathtools.Ratio.Ratio.__repr__
      ~abjad.tools.mathtools.Ratio.Ratio.__reversed__
      ~abjad.tools.mathtools.Ratio.Ratio.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.mathtools.Ratio.Ratio.multipliers

.. autoattribute:: abjad.tools.mathtools.Ratio.Ratio.numbers

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Ratio.Ratio.count

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Ratio.Ratio.index

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Ratio.Ratio.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Ratio.Ratio.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Ratio.Ratio.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Ratio.Ratio.__format__

.. automethod:: abjad.tools.mathtools.Ratio.Ratio.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Ratio.Ratio.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Ratio.Ratio.__iter__

.. automethod:: abjad.tools.mathtools.Ratio.Ratio.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Ratio.Ratio.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Ratio.Ratio.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Ratio.Ratio.__reversed__

.. automethod:: abjad.tools.mathtools.Ratio.Ratio.__str__
