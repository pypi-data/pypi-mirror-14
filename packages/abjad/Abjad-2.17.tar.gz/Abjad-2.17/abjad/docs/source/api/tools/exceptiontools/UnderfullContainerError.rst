.. currentmodule:: abjad.tools.exceptiontools

UnderfullContainerError
=======================

.. autoclass:: UnderfullContainerError

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
              "abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>UnderfullContainerError</B>>,
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
          "builtins.Exception" -> "abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError";
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

      ~abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError.with_traceback
      ~abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError.__delattr__
      ~abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError.__new__
      ~abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError.__repr__
      ~abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError.__setattr__
      ~abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError.__str__

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError.with_traceback

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError.__delattr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError.__setattr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError.__str__
