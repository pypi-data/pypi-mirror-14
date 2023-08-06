.. currentmodule:: abjad.tools.systemtools

IOManager
=========

.. autoclass:: IOManager

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
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.IOManager.IOManager" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>IOManager</B>>,
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
          subgraph cluster_idetools {
              graph [label=idetools];
              "ide.tools.idetools.IOManager.IOManager" [color=3,
                  group=2,
                  label=IOManager,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.IOManager.IOManager";
          "abjad.tools.systemtools.IOManager.IOManager" -> "ide.tools.idetools.IOManager.IOManager";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.systemtools.IOManager.IOManager.clear_terminal
      ~abjad.tools.systemtools.IOManager.IOManager.count_function_calls
      ~abjad.tools.systemtools.IOManager.IOManager.find_executable
      ~abjad.tools.systemtools.IOManager.IOManager.get_last_output_file_name
      ~abjad.tools.systemtools.IOManager.IOManager.get_next_output_file_name
      ~abjad.tools.systemtools.IOManager.IOManager.make_subprocess
      ~abjad.tools.systemtools.IOManager.IOManager.open_file
      ~abjad.tools.systemtools.IOManager.IOManager.open_last_log
      ~abjad.tools.systemtools.IOManager.IOManager.open_last_ly
      ~abjad.tools.systemtools.IOManager.IOManager.open_last_pdf
      ~abjad.tools.systemtools.IOManager.IOManager.profile_expr
      ~abjad.tools.systemtools.IOManager.IOManager.run_lilypond
      ~abjad.tools.systemtools.IOManager.IOManager.save_last_ly_as
      ~abjad.tools.systemtools.IOManager.IOManager.save_last_pdf_as
      ~abjad.tools.systemtools.IOManager.IOManager.spawn_subprocess
      ~abjad.tools.systemtools.IOManager.IOManager.__eq__
      ~abjad.tools.systemtools.IOManager.IOManager.__format__
      ~abjad.tools.systemtools.IOManager.IOManager.__hash__
      ~abjad.tools.systemtools.IOManager.IOManager.__ne__
      ~abjad.tools.systemtools.IOManager.IOManager.__repr__

Class & static methods
----------------------

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.clear_terminal

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.count_function_calls

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.find_executable

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.get_last_output_file_name

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.get_next_output_file_name

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.make_subprocess

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.open_file

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.open_last_log

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.open_last_ly

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.open_last_pdf

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.profile_expr

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.run_lilypond

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.save_last_ly_as

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.save_last_pdf_as

.. automethod:: abjad.tools.systemtools.IOManager.IOManager.spawn_subprocess

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.IOManager.IOManager.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.IOManager.IOManager.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.IOManager.IOManager.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.IOManager.IOManager.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.IOManager.IOManager.__repr__
