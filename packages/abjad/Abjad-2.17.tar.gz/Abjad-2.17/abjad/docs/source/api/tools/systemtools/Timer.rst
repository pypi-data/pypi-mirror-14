.. currentmodule:: abjad.tools.systemtools

Timer
=====

.. autoclass:: Timer

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
              "abjad.tools.systemtools.Timer.Timer" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Timer</B>>,
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
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.Timer.Timer";
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

      ~abjad.tools.systemtools.Timer.Timer.elapsed_time
      ~abjad.tools.systemtools.Timer.Timer.enter_message
      ~abjad.tools.systemtools.Timer.Timer.exit_message
      ~abjad.tools.systemtools.Timer.Timer.print_continuously_from_background
      ~abjad.tools.systemtools.Timer.Timer.start_time
      ~abjad.tools.systemtools.Timer.Timer.stop_time
      ~abjad.tools.systemtools.Timer.Timer.total_time_message
      ~abjad.tools.systemtools.Timer.Timer.verbose
      ~abjad.tools.systemtools.Timer.Timer.__enter__
      ~abjad.tools.systemtools.Timer.Timer.__eq__
      ~abjad.tools.systemtools.Timer.Timer.__exit__
      ~abjad.tools.systemtools.Timer.Timer.__format__
      ~abjad.tools.systemtools.Timer.Timer.__hash__
      ~abjad.tools.systemtools.Timer.Timer.__ne__
      ~abjad.tools.systemtools.Timer.Timer.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.systemtools.Timer.Timer.elapsed_time

.. autoattribute:: abjad.tools.systemtools.Timer.Timer.enter_message

.. autoattribute:: abjad.tools.systemtools.Timer.Timer.exit_message

.. autoattribute:: abjad.tools.systemtools.Timer.Timer.print_continuously_from_background

.. autoattribute:: abjad.tools.systemtools.Timer.Timer.start_time

.. autoattribute:: abjad.tools.systemtools.Timer.Timer.stop_time

.. autoattribute:: abjad.tools.systemtools.Timer.Timer.total_time_message

.. autoattribute:: abjad.tools.systemtools.Timer.Timer.verbose

Special methods
---------------

.. automethod:: abjad.tools.systemtools.Timer.Timer.__enter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Timer.Timer.__eq__

.. automethod:: abjad.tools.systemtools.Timer.Timer.__exit__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Timer.Timer.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Timer.Timer.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Timer.Timer.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Timer.Timer.__repr__
