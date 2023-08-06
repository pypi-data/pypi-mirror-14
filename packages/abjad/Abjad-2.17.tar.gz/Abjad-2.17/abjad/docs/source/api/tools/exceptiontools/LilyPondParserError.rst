.. currentmodule:: abjad.tools.exceptiontools

LilyPondParserError
===================

.. autoclass:: LilyPondParserError

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
          subgraph cluster_exceptiontools {
              graph [label=exceptiontools];
              "abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>LilyPondParserError</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.BaseException" [color=1,
                  group=0,
                  label=BaseException,
                  shape=box];
              "builtins.Exception" [color=1,
                  group=0,
                  label=Exception,
                  shape=box];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
              "builtins.BaseException" -> "builtins.Exception";
              "builtins.object" -> "builtins.BaseException";
          }
          "builtins.Exception" -> "abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError";
      }

Bases
-----

- :py:class:`builtins.Exception`

- :py:class:`builtins.BaseException`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError.with_traceback
      ~abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError.__delattr__
      ~abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError.__new__
      ~abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError.__repr__
      ~abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError.__setattr__
      ~abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError.__str__

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError.with_traceback

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError.__delattr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError.__setattr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError.__str__
