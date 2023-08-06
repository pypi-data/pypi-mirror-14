.. currentmodule:: abjad.tools.developerscripttools

DirectoryScript
===============

.. autoclass:: DirectoryScript

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
              "abjad.tools.developerscripttools.AbjGrepScript.AbjGrepScript" [color=3,
                  group=2,
                  label=AbjGrepScript,
                  shape=box];
              "abjad.tools.developerscripttools.CleanScript.CleanScript" [color=3,
                  group=2,
                  label=CleanScript,
                  shape=box];
              "abjad.tools.developerscripttools.CountLinewidthsScript.CountLinewidthsScript" [color=3,
                  group=2,
                  label=CountLinewidthsScript,
                  shape=box];
              "abjad.tools.developerscripttools.CountToolsScript.CountToolsScript" [color=3,
                  group=2,
                  label=CountToolsScript,
                  shape=box];
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" [color=3,
                  group=2,
                  label=DeveloperScript,
                  shape=oval,
                  style=bold];
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>DirectoryScript</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.NewScoreScript.NewScoreScript" [color=3,
                  group=2,
                  label=NewScoreScript,
                  shape=box];
              "abjad.tools.developerscripttools.PyTestScript.PyTestScript" [color=3,
                  group=2,
                  label=PyTestScript,
                  shape=box];
              "abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript" [color=3,
                  group=2,
                  label=ReplaceInFilesScript,
                  shape=box];
              "abjad.tools.developerscripttools.RunDoctestsScript.RunDoctestsScript" [color=3,
                  group=2,
                  label=RunDoctestsScript,
                  shape=box];
              "abjad.tools.developerscripttools.StatsScript.StatsScript" [color=3,
                  group=2,
                  label=StatsScript,
                  shape=box];
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.AbjGrepScript.AbjGrepScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.CleanScript.CleanScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.CountLinewidthsScript.CountLinewidthsScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.CountToolsScript.CountToolsScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.NewScoreScript.NewScoreScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.PyTestScript.PyTestScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.RunDoctestsScript.RunDoctestsScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.StatsScript.StatsScript";
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

      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.alias
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.argument_parser
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.colors
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.formatted_help
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.formatted_usage
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.formatted_version
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.long_description
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.process_args
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.program_name
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.scripting_group
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.setup_argument_parser
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.short_description
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.version
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.__call__
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.__eq__
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.__format__
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.__hash__
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.__ne__
      ~abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.alias

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.argument_parser

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.colors

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.formatted_help

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.formatted_usage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.formatted_version

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.long_description

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.program_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.scripting_group

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.short_description

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.version

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.process_args

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.setup_argument_parser

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.DirectoryScript.DirectoryScript.__repr__
