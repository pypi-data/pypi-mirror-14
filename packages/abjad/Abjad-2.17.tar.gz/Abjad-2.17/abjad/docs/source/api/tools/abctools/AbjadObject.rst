.. currentmodule:: abjad.tools.abctools

AbjadObject
===========

.. autoclass:: AbjadObject

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
              "abjad.tools.abctools.AbjadObject.AbjadObject" [color=black,
                  fontcolor=white,
                  group=0,
                  label=<<B>AbjadObject</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abctools.AbjadObject.AbstractBase" [color=1,
                  group=0,
                  label=AbstractBase,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.abctools.AbjadObject.AbjadObject.__eq__
      ~abjad.tools.abctools.AbjadObject.AbjadObject.__format__
      ~abjad.tools.abctools.AbjadObject.AbjadObject.__hash__
      ~abjad.tools.abctools.AbjadObject.AbjadObject.__ne__
      ~abjad.tools.abctools.AbjadObject.AbjadObject.__repr__

Special methods
---------------

.. automethod:: abjad.tools.abctools.AbjadObject.AbjadObject.__eq__

.. automethod:: abjad.tools.abctools.AbjadObject.AbjadObject.__format__

.. automethod:: abjad.tools.abctools.AbjadObject.AbjadObject.__hash__

.. automethod:: abjad.tools.abctools.AbjadObject.AbjadObject.__ne__

.. automethod:: abjad.tools.abctools.AbjadObject.AbjadObject.__repr__
