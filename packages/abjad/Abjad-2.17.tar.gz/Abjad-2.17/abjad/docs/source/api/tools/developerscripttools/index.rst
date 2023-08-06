developerscripttools
====================

.. automodule:: abjad.tools.developerscripttools

--------

Lineage
-------

.. container:: graphviz

   .. graphviz::

      digraph InheritanceGraph {
          graph [bgcolor=transparent,
              color=lightslategrey,
              dpi=72,
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
              "abjad.tools.developerscripttools.AbjDevScript.AbjDevScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=AbjDevScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.AbjGrepScript.AbjGrepScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=AbjGrepScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.BuildAPIScript.BuildAPIScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BuildAPIScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.CleanScript.CleanScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=CleanScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.CountLinewidthsScript.CountLinewidthsScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=CountLinewidthsScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.CountToolsScript.CountToolsScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=CountToolsScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=DeveloperScript,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=DirectoryScript,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.NewScoreScript.NewScoreScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NewScoreScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.PyTestScript.PyTestScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PyTestScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.RenameModulesScript.RenameModulesScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=RenameModulesScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.ReplaceInFilesScript.ReplaceInFilesScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ReplaceInFilesScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.RunDoctestsScript.RunDoctestsScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=RunDoctestsScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.StatsScript.StatsScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=StatsScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.developerscripttools.TestAndRebuildScript.TestAndRebuildScript" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TestAndRebuildScript,
                  shape=box,
                  style="filled, rounded"];
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

--------

Abstract Classes
----------------

.. toctree::
   :hidden:

   DeveloperScript
   DirectoryScript

.. autosummary::
   :nosignatures:

   DeveloperScript
   DirectoryScript

--------

Classes
-------

.. toctree::
   :hidden:

   AbjDevScript
   AbjGrepScript
   BuildAPIScript
   CleanScript
   CountLinewidthsScript
   CountToolsScript
   NewScoreScript
   PyTestScript
   RenameModulesScript
   ReplaceInFilesScript
   RunDoctestsScript
   StatsScript
   TestAndRebuildScript

.. autosummary::
   :nosignatures:

   AbjDevScript
   AbjGrepScript
   BuildAPIScript
   CleanScript
   CountLinewidthsScript
   CountToolsScript
   NewScoreScript
   PyTestScript
   RenameModulesScript
   ReplaceInFilesScript
   RunDoctestsScript
   StatsScript
   TestAndRebuildScript

--------

Functions
---------

.. toctree::
   :hidden:

   get_developer_script_classes
   run_ajv

.. autosummary::
   :nosignatures:

   get_developer_script_classes
   run_ajv
