.. currentmodule:: abjad.tools.lilypondparsertools

LilyPondParser
==============

.. autoclass:: LilyPondParser

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
              "abjad.tools.abctools.Parser.Parser" [color=1,
                  group=0,
                  label=Parser,
                  shape=oval,
                  style=bold];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.Parser.Parser";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_lilypondparsertools {
              graph [label=lilypondparsertools];
              "abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LilyPondParser</B>>,
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
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.Parser`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.available_languages
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.debug
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.default_language
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.lexer
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.lexer_rules_object
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.list_known_contexts
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.list_known_dynamics
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.list_known_grobs
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.list_known_languages
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.list_known_markup_functions
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.list_known_music_functions
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.logger
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.logger_path
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.output_path
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.parser
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.parser_rules_object
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.pickle_path
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.register_markup_function
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.tokenize
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.__call__
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.__eq__
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.__format__
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.__hash__
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.__ne__
      ~abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.available_languages

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.debug

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.lexer

.. autoattribute:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.lexer_rules_object

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.logger

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.logger_path

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.output_path

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.parser

.. autoattribute:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.parser_rules_object

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.pickle_path

Read/write properties
---------------------

.. autoattribute:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.default_language

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.tokenize

Class & static methods
----------------------

.. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.list_known_contexts

.. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.list_known_dynamics

.. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.list_known_grobs

.. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.list_known_languages

.. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.list_known_markup_functions

.. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.list_known_music_functions

.. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.register_markup_function

Special methods
---------------

.. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser.__repr__
