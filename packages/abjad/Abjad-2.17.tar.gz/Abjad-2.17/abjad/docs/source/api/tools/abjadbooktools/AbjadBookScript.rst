.. currentmodule:: abjad.tools.abjadbooktools

AbjadBookScript
===============

.. autoclass:: AbjadBookScript

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
              "abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>AbjadBookScript</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_developerscripttools {
              graph [label=developerscripttools];
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" [color=4,
                  group=3,
                  label=DeveloperScript,
                  shape=oval,
                  style=bold];
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

- :py:class:`abjad.tools.developerscripttools.DeveloperScript`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.alias
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.argument_parser
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.colors
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.formatted_help
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.formatted_usage
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.formatted_version
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.long_description
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.process_args
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.program_name
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.scripting_group
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.setup_argument_parser
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.short_description
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.version
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__call__
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__eq__
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__format__
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__hash__
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__ne__
      ~abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.alias

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.argument_parser

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.colors

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.formatted_help

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.formatted_usage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.formatted_version

.. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.long_description

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.program_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.scripting_group

.. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.short_description

.. autoattribute:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.version

Methods
-------

.. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.process_args

.. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.setup_argument_parser

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript.__repr__
