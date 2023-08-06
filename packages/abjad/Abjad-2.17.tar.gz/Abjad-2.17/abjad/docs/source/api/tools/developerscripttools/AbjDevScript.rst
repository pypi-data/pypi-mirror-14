.. currentmodule:: abjad.tools.developerscripttools

AbjDevScript
============

.. autoclass:: AbjDevScript

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
          subgraph cluster_developerscripttools {
              graph [label=developerscripttools];
              "abjad.tools.developerscripttools.AbjDevScript.AbjDevScript" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>AbjDevScript</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" [color=3,
                  group=2,
                  label=DeveloperScript,
                  shape=oval,
                  style=bold];
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.AbjDevScript.AbjDevScript";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.developerscripttools.DeveloperScript`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.alias
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.argument_parser
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.colors
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.developer_script_aliases
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.developer_script_classes
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.developer_script_program_names
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.formatted_help
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.formatted_usage
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.formatted_version
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.long_description
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.process_args
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.program_name
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.scripting_group
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.setup_argument_parser
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.short_description
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.version
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.__call__
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.__eq__
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.__format__
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.__hash__
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.__ne__
      ~abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.alias

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.argument_parser

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.colors

.. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.developer_script_aliases

.. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.developer_script_classes

.. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.developer_script_program_names

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.formatted_help

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.formatted_usage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.formatted_version

.. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.long_description

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.program_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.scripting_group

.. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.short_description

.. autoattribute:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.version

Methods
-------

.. automethod:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.process_args

.. automethod:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.setup_argument_parser

Special methods
---------------

.. automethod:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.AbjDevScript.AbjDevScript.__repr__
