.. currentmodule:: abjad.tools.systemtools

TestManager
===========

.. autoclass:: TestManager

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
              "abjad.tools.systemtools.TestManager.TestManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TestManager</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.TestManager.TestManager";
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

      ~abjad.tools.systemtools.TestManager.TestManager.apply_additional_layout
      ~abjad.tools.systemtools.TestManager.TestManager.clean_string
      ~abjad.tools.systemtools.TestManager.TestManager.compare
      ~abjad.tools.systemtools.TestManager.TestManager.compare_files
      ~abjad.tools.systemtools.TestManager.TestManager.diff
      ~abjad.tools.systemtools.TestManager.TestManager.get_current_function_name
      ~abjad.tools.systemtools.TestManager.TestManager.read_test_output
      ~abjad.tools.systemtools.TestManager.TestManager.test_function_name_to_title_lines
      ~abjad.tools.systemtools.TestManager.TestManager.write_test_output
      ~abjad.tools.systemtools.TestManager.TestManager.__eq__
      ~abjad.tools.systemtools.TestManager.TestManager.__format__
      ~abjad.tools.systemtools.TestManager.TestManager.__hash__
      ~abjad.tools.systemtools.TestManager.TestManager.__ne__
      ~abjad.tools.systemtools.TestManager.TestManager.__repr__

Class & static methods
----------------------

.. automethod:: abjad.tools.systemtools.TestManager.TestManager.apply_additional_layout

.. automethod:: abjad.tools.systemtools.TestManager.TestManager.clean_string

.. automethod:: abjad.tools.systemtools.TestManager.TestManager.compare

.. automethod:: abjad.tools.systemtools.TestManager.TestManager.compare_files

.. automethod:: abjad.tools.systemtools.TestManager.TestManager.diff

.. automethod:: abjad.tools.systemtools.TestManager.TestManager.get_current_function_name

.. automethod:: abjad.tools.systemtools.TestManager.TestManager.read_test_output

.. automethod:: abjad.tools.systemtools.TestManager.TestManager.test_function_name_to_title_lines

.. automethod:: abjad.tools.systemtools.TestManager.TestManager.write_test_output

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestManager.TestManager.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestManager.TestManager.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestManager.TestManager.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestManager.TestManager.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.TestManager.TestManager.__repr__
