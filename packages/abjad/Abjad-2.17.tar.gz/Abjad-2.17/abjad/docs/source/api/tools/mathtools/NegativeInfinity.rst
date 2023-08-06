.. currentmodule:: abjad.tools.mathtools

NegativeInfinity
================

.. autoclass:: NegativeInfinity

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
              "abjad.tools.mathtools.Infinity.Infinity" [color=3,
                  group=2,
                  label=Infinity,
                  shape=box];
              "abjad.tools.mathtools.NegativeInfinity.NegativeInfinity" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NegativeInfinity</B>>,
                  shape=box,
                  style="filled, rounded"];
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

- :py:class:`abjad.tools.mathtools.Infinity`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__eq__
      ~abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__format__
      ~abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__ge__
      ~abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__gt__
      ~abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__hash__
      ~abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__le__
      ~abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__lt__
      ~abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__ne__
      ~abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__repr__
      ~abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__sub__

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.NegativeInfinity.NegativeInfinity.__sub__
