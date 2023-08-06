.. currentmodule:: abjad.tools.datastructuretools

Enumeration
===========

.. autoclass:: Enumeration

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
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.Enumeration.Enumeration" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>Enumeration</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.int" [color=1,
                  group=0,
                  label=int,
                  shape=box];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
              "builtins.object" -> "builtins.int";
          }
          subgraph cluster_enum {
              graph [label=enum];
              "enum.Enum" [color=3,
                  group=2,
                  label=Enum,
                  shape=box];
              "enum.IntEnum" [color=3,
                  group=2,
                  label=IntEnum,
                  shape=box];
              "enum.Enum" -> "enum.IntEnum";
          }
          "builtins.int" -> "enum.IntEnum";
          "builtins.object" -> "enum.Enum";
          "enum.IntEnum" -> "abjad.tools.datastructuretools.Enumeration.Enumeration";
      }

Bases
-----

- :py:class:`enum.IntEnum`

- :py:class:`builtins.int`

- :py:class:`enum.Enum`

- :py:class:`builtins.object`
