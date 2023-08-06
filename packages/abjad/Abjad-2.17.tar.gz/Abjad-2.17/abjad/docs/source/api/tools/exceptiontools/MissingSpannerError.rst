.. currentmodule:: abjad.tools.exceptiontools

MissingSpannerError
===================

.. autoclass:: MissingSpannerError

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
              "abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>MissingSpannerError</B>>,
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
          "builtins.Exception" -> "abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError";
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

      ~abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError.with_traceback
      ~abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError.__delattr__
      ~abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError.__new__
      ~abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError.__repr__
      ~abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError.__setattr__
      ~abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError.__str__

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError.with_traceback

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError.__delattr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError.__setattr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError.__str__
