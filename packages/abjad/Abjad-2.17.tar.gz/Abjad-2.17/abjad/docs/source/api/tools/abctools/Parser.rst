.. currentmodule:: abjad.tools.abctools

Parser
======

.. autoclass:: Parser

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
              "abjad.tools.abctools.Parser.Parser" [color=black,
                  fontcolor=white,
                  group=0,
                  label=<<B>Parser</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.Parser.Parser";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_lilypondparsertools {
              graph [label=lilypondparsertools];
              "abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser" [color=3,
                  group=2,
                  label=LilyPondParser,
                  shape=box];
              "abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser" [color=3,
                  group=2,
                  label=ReducedLyParser,
                  shape=box];
              "abjad.tools.lilypondparsertools.SchemeParser.SchemeParser" [color=3,
                  group=2,
                  label=SchemeParser,
                  shape=box];
          }
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser" [color=4,
                  group=3,
                  label=RhythmTreeParser,
                  shape=box];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.SchemeParser.SchemeParser";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser";
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

      ~abjad.tools.abctools.Parser.Parser.debug
      ~abjad.tools.abctools.Parser.Parser.lexer
      ~abjad.tools.abctools.Parser.Parser.lexer_rules_object
      ~abjad.tools.abctools.Parser.Parser.logger
      ~abjad.tools.abctools.Parser.Parser.logger_path
      ~abjad.tools.abctools.Parser.Parser.output_path
      ~abjad.tools.abctools.Parser.Parser.parser
      ~abjad.tools.abctools.Parser.Parser.parser_rules_object
      ~abjad.tools.abctools.Parser.Parser.pickle_path
      ~abjad.tools.abctools.Parser.Parser.tokenize
      ~abjad.tools.abctools.Parser.Parser.__call__
      ~abjad.tools.abctools.Parser.Parser.__eq__
      ~abjad.tools.abctools.Parser.Parser.__format__
      ~abjad.tools.abctools.Parser.Parser.__hash__
      ~abjad.tools.abctools.Parser.Parser.__ne__
      ~abjad.tools.abctools.Parser.Parser.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.abctools.Parser.Parser.debug

.. autoattribute:: abjad.tools.abctools.Parser.Parser.lexer

.. autoattribute:: abjad.tools.abctools.Parser.Parser.lexer_rules_object

.. autoattribute:: abjad.tools.abctools.Parser.Parser.logger

.. autoattribute:: abjad.tools.abctools.Parser.Parser.logger_path

.. autoattribute:: abjad.tools.abctools.Parser.Parser.output_path

.. autoattribute:: abjad.tools.abctools.Parser.Parser.parser

.. autoattribute:: abjad.tools.abctools.Parser.Parser.parser_rules_object

.. autoattribute:: abjad.tools.abctools.Parser.Parser.pickle_path

Methods
-------

.. automethod:: abjad.tools.abctools.Parser.Parser.tokenize

Special methods
---------------

.. automethod:: abjad.tools.abctools.Parser.Parser.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abctools.Parser.Parser.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abctools.Parser.Parser.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abctools.Parser.Parser.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abctools.Parser.Parser.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abctools.Parser.Parser.__repr__
