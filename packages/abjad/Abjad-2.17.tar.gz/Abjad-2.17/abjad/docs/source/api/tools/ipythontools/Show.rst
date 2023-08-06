.. currentmodule:: abjad.tools.ipythontools

Show
====

.. autoclass:: Show

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
          subgraph cluster_ipythontools {
              graph [label=ipythontools];
              "abjad.tools.ipythontools.Show.Show" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>Show</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
          }
          "builtins.object" -> "abjad.tools.ipythontools.Show.Show";
      }

Bases
-----

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.ipythontools.Show.Show.__call__

Special methods
---------------

.. automethod:: abjad.tools.ipythontools.Show.Show.__call__
