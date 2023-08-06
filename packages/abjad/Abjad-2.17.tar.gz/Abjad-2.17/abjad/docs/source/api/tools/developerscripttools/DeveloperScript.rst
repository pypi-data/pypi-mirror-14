.. currentmodule:: abjad.tools.developerscripttools

DeveloperScript
===============

.. autoclass:: DeveloperScript

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
          subgraph cluster_abjadbooktools {
              graph [label=abjadbooktools];
              "abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript" [color=2,
                  group=1,
                  label=AbjadBookScript,
                  shape=box];
          }
          subgraph cluster_developerscripttools {
              graph [label=developerscripttools];
              "abjad.tools.developerscripttools.AbjDevScript.AbjDevScript" [color=4,
                  group=3,
                  label=AbjDevScript,
                  shape=box];
              "abjad.tools.developerscripttools.AbjGrepScript.AbjGrepScript" [color=4,
                  group=3,
                  label=AbjGrepScript,
                  shape=box];
              "abjad.tools.developerscripttools.BuildAPIScript.BuildAPIScript" [color=4,
                  group=3,
                  label=BuildAPIScript,
                  shape=box];
              "abjad.tools.developerscripttools.CleanScript.CleanScript" [color=4,
                  group=3,
                  label=CleanScript,
                  shape=box];
              "abjad.tools.developerscripttools.CountLinewidthsScript.CountLinewidthsScript" [color=4,
                  group=3,
                  label=CountLinewidthsScript,
                  shape=box];
              "abjad.tools.developerscripttools.CountToolsScript.CountToolsScript" [color=4,
                  group=3,
                  label=CountToolsScript,
                  shape=box];
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>DeveloperScript</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" [color=4,
                  group=3,
                  label=DirectoryScript,
                  shape=oval,
                  style=bold];
              "abjad.tools.developerscripttools.NewScoreScript.NewScoreScript" [color=4,
                  group=3,
                  label=NewScoreScript,
                  shape=box];
              "abjad.tools.developerscripttools.PyTestScript.PyTestScript" [color=4,
                  group=3,
                  label=PyTestScript,
                  shape=box];
              "abjad.tools.developerscripttools.RenameModulesScript.RenameModulesScript" [color=4,
                  group=3,
                  label=RenameModulesScript,
                  shape=box];
              "abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript" [color=4,
                  group=3,
                  label=ReplaceInFilesScript,
                  shape=box];
              "abjad.tools.developerscripttools.RunDoctestsScript.RunDoctestsScript" [color=4,
                  group=3,
                  label=RunDoctestsScript,
                  shape=box];
              "abjad.tools.developerscripttools.StatsScript.StatsScript" [color=4,
                  group=3,
                  label=StatsScript,
                  shape=box];
              "abjad.tools.developerscripttools.TestAndRebuildScript.TestAndRebuildScript" [color=4,
                  group=3,
                  label=TestAndRebuildScript,
                  shape=box];
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.AbjDevScript.AbjDevScript";
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.BuildAPIScript.BuildAPIScript";
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript";
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.RenameModulesScript.RenameModulesScript";
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.TestAndRebuildScript.TestAndRebuildScript";
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
              "builtins.object" [color=3,
                  group=2,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript";
          "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript";
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

      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.alias
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.argument_parser
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.colors
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.formatted_help
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.formatted_usage
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.formatted_version
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.long_description
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.process_args
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.program_name
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.scripting_group
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.setup_argument_parser
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.short_description
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.version
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.__call__
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.__eq__
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.__format__
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.__hash__
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.__ne__
      ~abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.alias

.. autoattribute:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.argument_parser

.. autoattribute:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.colors

.. autoattribute:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.formatted_help

.. autoattribute:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.formatted_usage

.. autoattribute:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.formatted_version

.. autoattribute:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.long_description

.. autoattribute:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.program_name

.. autoattribute:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.scripting_group

.. autoattribute:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.short_description

.. autoattribute:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.version

Methods
-------

.. automethod:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.process_args

.. automethod:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.setup_argument_parser

Special methods
---------------

.. automethod:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.DeveloperScript.DeveloperScript.__repr__
