.. currentmodule:: abjad.tools.systemtools

ProgressIndicator
=================

.. autoclass:: ProgressIndicator

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
              "abjad.tools.abctools.ContextManager.ContextManager" [color=1,
                  group=0,
                  label=ContextManager,
                  shape=oval,
                  style=bold];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.ContextManager.ContextManager";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.ProgressIndicator.ProgressIndicator" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ProgressIndicator</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.ProgressIndicator.ProgressIndicator";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.ContextManager`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.advance
      ~abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.is_warning
      ~abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.message
      ~abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.progress
      ~abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.total
      ~abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.verbose
      ~abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__enter__
      ~abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__eq__
      ~abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__exit__
      ~abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__format__
      ~abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__hash__
      ~abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__ne__
      ~abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.is_warning

.. autoattribute:: abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.message

.. autoattribute:: abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.progress

.. autoattribute:: abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.total

.. autoattribute:: abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.verbose

Methods
-------

.. automethod:: abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.advance

Special methods
---------------

.. automethod:: abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__enter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__eq__

.. automethod:: abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__exit__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__ne__

.. automethod:: abjad.tools.systemtools.ProgressIndicator.ProgressIndicator.__repr__
