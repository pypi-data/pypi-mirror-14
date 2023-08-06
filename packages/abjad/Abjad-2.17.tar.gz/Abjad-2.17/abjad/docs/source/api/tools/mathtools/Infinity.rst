.. currentmodule:: abjad.tools.mathtools

Infinity
========

.. autoclass:: Infinity

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
          subgraph cluster_mathtools {
              graph [label=mathtools];
              "abjad.tools.mathtools.Infinity.Infinity" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Infinity</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.mathtools.NegativeInfinity.NegativeInfinity" [color=3,
                  group=2,
                  label=NegativeInfinity,
                  shape=box];
              "abjad.tools.mathtools.Infinity.Infinity" -> "abjad.tools.mathtools.NegativeInfinity.NegativeInfinity";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.Infinity.Infinity";
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

      ~abjad.tools.mathtools.Infinity.Infinity.__eq__
      ~abjad.tools.mathtools.Infinity.Infinity.__format__
      ~abjad.tools.mathtools.Infinity.Infinity.__ge__
      ~abjad.tools.mathtools.Infinity.Infinity.__gt__
      ~abjad.tools.mathtools.Infinity.Infinity.__hash__
      ~abjad.tools.mathtools.Infinity.Infinity.__le__
      ~abjad.tools.mathtools.Infinity.Infinity.__lt__
      ~abjad.tools.mathtools.Infinity.Infinity.__ne__
      ~abjad.tools.mathtools.Infinity.Infinity.__repr__
      ~abjad.tools.mathtools.Infinity.Infinity.__sub__

Special methods
---------------

.. automethod:: abjad.tools.mathtools.Infinity.Infinity.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Infinity.Infinity.__format__

.. automethod:: abjad.tools.mathtools.Infinity.Infinity.__ge__

.. automethod:: abjad.tools.mathtools.Infinity.Infinity.__gt__

.. automethod:: abjad.tools.mathtools.Infinity.Infinity.__hash__

.. automethod:: abjad.tools.mathtools.Infinity.Infinity.__le__

.. automethod:: abjad.tools.mathtools.Infinity.Infinity.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Infinity.Infinity.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.Infinity.Infinity.__repr__

.. automethod:: abjad.tools.mathtools.Infinity.Infinity.__sub__
