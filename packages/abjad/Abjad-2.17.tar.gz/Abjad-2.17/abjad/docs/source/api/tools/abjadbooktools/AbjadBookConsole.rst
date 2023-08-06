.. currentmodule:: abjad.tools.abjadbooktools

AbjadBookConsole
================

.. autoclass:: AbjadBookConsole

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
          subgraph cluster_abjadbooktools {
              graph [label=abjadbooktools];
              "abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole" [color=black,
                  fontcolor=white,
                  group=0,
                  label=<<B>AbjadBookConsole</B>>,
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
          subgraph cluster_code {
              graph [label=code];
              "code.InteractiveConsole" [color=3,
                  group=2,
                  label=InteractiveConsole,
                  shape=box];
              "code.InteractiveInterpreter" [color=3,
                  group=2,
                  label=InteractiveInterpreter,
                  shape=box];
              "code.InteractiveInterpreter" -> "code.InteractiveConsole";
          }
          "builtins.object" -> "code.InteractiveInterpreter";
          "code.InteractiveConsole" -> "abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole";
      }

Bases
-----

- :py:class:`code.InteractiveConsole`

- :py:class:`code.InteractiveInterpreter`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.errored
      ~abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.interact
      ~abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.push
      ~abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.raw_input
      ~abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.resetbuffer
      ~abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.restore_topleveltools_dict
      ~abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.runcode
      ~abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.runsource
      ~abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.save_topleveltools_dict
      ~abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.showsyntaxerror
      ~abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.showtraceback
      ~abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.unregister_error
      ~abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.write

Read-only properties
--------------------

.. autoattribute:: abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.errored

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.interact

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.push

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.raw_input

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.resetbuffer

.. automethod:: abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.restore_topleveltools_dict

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.runcode

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.runsource

.. automethod:: abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.save_topleveltools_dict

.. automethod:: abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.showsyntaxerror

.. automethod:: abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.showtraceback

.. automethod:: abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.unregister_error

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole.write
