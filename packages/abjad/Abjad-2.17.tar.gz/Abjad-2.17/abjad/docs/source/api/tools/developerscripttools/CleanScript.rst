.. currentmodule:: abjad.tools.developerscripttools

CleanScript
===========

.. autoclass:: CleanScript

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
              "abjad.tools.developerscripttools.CleanScript.CleanScript" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>CleanScript</B>>,
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
              "abjad.tools.developerscripttools.DirectoryScript.DirectoryScript" -> "abjad.tools.developerscripttools.CleanScript.CleanScript";
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

      ~abjad.tools.developerscripttools.CleanScript.CleanScript.alias
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.argument_parser
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.colors
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.formatted_help
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.formatted_usage
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.formatted_version
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.long_description
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.process_args
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.program_name
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.scripting_group
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.setup_argument_parser
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.short_description
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.version
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.__call__
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.__eq__
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.__format__
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.__hash__
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.__ne__
      ~abjad.tools.developerscripttools.CleanScript.CleanScript.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.developerscripttools.CleanScript.CleanScript.alias

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.CleanScript.CleanScript.argument_parser

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.CleanScript.CleanScript.colors

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.CleanScript.CleanScript.formatted_help

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.CleanScript.CleanScript.formatted_usage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.CleanScript.CleanScript.formatted_version

.. autoattribute:: abjad.tools.developerscripttools.CleanScript.CleanScript.long_description

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.developerscripttools.CleanScript.CleanScript.program_name

.. autoattribute:: abjad.tools.developerscripttools.CleanScript.CleanScript.scripting_group

.. autoattribute:: abjad.tools.developerscripttools.CleanScript.CleanScript.short_description

.. autoattribute:: abjad.tools.developerscripttools.CleanScript.CleanScript.version

Methods
-------

.. automethod:: abjad.tools.developerscripttools.CleanScript.CleanScript.process_args

.. automethod:: abjad.tools.developerscripttools.CleanScript.CleanScript.setup_argument_parser

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.CleanScript.CleanScript.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.CleanScript.CleanScript.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.CleanScript.CleanScript.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.CleanScript.CleanScript.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.CleanScript.CleanScript.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.developerscripttools.CleanScript.CleanScript.__repr__
