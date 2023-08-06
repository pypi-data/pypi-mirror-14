.. currentmodule:: abjad.tools.developerscripttools

CountToolsScript
================

.. autoclass:: CountToolsScript

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
              "abjad.tools.developerscripttools.CountToolsScript.CountToolsScript" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>CountToolsScript</B>>,
                  shape=box,
                  style="filled, rounded"];
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
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript";
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.CountToolsScript.CountToolsScript";
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

      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.alias
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.argument_parser
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.colors
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.formatted_help
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.formatted_usage
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.formatted_version
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.long_description
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.process_args
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.program_name
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.scripting_group
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.setup_argument_parser
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.short_description
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.version
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.__call__
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.__eq__
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.__format__
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.__hash__
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.__ne__
      ~abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.alias

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.argument_parser

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.colors

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.formatted_help

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.formatted_usage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.formatted_version

.. autoattribute:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.long_description

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.program_name

.. autoattribute:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.scripting_group

.. autoattribute:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.short_description

.. autoattribute:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.version

Methods
-------

.. automethod:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.process_args

.. automethod:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.setup_argument_parser

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.CountToolsScript.CountToolsScript.__repr__
