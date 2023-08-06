ipythontools
============

.. automodule:: abjad.tools.ipythontools

--------

Lineage
-------

.. container:: graphviz

   .. graphviz::

      digraph InheritanceGraph {
          graph [bgcolor=transparent,
              color=lightslategrey,
              dpi=72,
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
              "abjad.tools.ipythontools.Play.Play" [color=black,
                  fontcolor=white,
                  group=1,
                  label=Play,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.ipythontools.Show.Show" [color=black,
                  fontcolor=white,
                  group=1,
                  label=Show,
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
          "builtins.object" -> "abjad.tools.ipythontools.Play.Play";
          "builtins.object" -> "abjad.tools.ipythontools.Show.Show";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   Play
   Show

.. autosummary::
   :nosignatures:

   Play
   Show
