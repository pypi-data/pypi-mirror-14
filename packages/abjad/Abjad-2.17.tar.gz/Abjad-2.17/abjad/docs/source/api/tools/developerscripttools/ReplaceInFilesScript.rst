.. currentmodule:: abjad.tools.developerscripttools

ReplaceInFilesScript
====================

.. autoclass:: ReplaceInFilesScript

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
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" [color=3,
                  group=2,
                  label=DeveloperScript,
                  shape=oval,
                  style=bold];
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" [color=3,
                  group=2,
                  label=DirectoryScript,
                  shape=oval,
                  style=bold];
              "abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ReplaceInFilesScript</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript";
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

- :py:class:`abjad.tools.developerscripttools.DirectoryScript`

- :py:class:`abjad.tools.developerscripttools.DeveloperScript`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.alias
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.argument_parser
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.colors
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.formatted_help
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.formatted_usage
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.formatted_version
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.long_description
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.process_args
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.program_name
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.scripting_group
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.setup_argument_parser
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.short_description
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.skipped_directories
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.skipped_files
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.version
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.__call__
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.__eq__
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.__format__
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.__hash__
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.__ne__
      ~abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.alias

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.argument_parser

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.colors

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.formatted_help

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.formatted_usage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.formatted_version

.. autoattribute:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.long_description

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.program_name

.. autoattribute:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.scripting_group

.. autoattribute:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.short_description

.. autoattribute:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.skipped_directories

.. autoattribute:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.skipped_files

.. autoattribute:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.version

Methods
-------

.. automethod:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.process_args

.. automethod:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.setup_argument_parser

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript.__repr__
