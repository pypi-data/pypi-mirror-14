lilypondparsertools
===================

.. automodule:: abjad.tools.lilypondparsertools

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
              "abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic" [color=black,
                  fontcolor=white,
                  group=2,
                  label=ContextSpeccedMusic,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.GuileProxy.GuileProxy" [color=black,
                  fontcolor=white,
                  group=2,
                  label=GuileProxy,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.LilyPondDuration.LilyPondDuration" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondDuration,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.LilyPondEvent.LilyPondEvent" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondEvent,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.LilyPondFraction.LilyPondFraction" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondFraction,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.LilyPondGrammarGenerator.LilyPondGrammarGenerator" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondGrammarGenerator,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondLexicalDefinition,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondParser,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.LilyPondSyntacticalDefinition.LilyPondSyntacticalDefinition" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondSyntacticalDefinition,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.Music.Music" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Music,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser" [color=black,
                  fontcolor=white,
                  group=2,
                  label=ReducedLyParser,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.SchemeParser.SchemeParser" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SchemeParser,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.SequentialMusic.SequentialMusic" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SequentialMusic,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.SimultaneousMusic.SimultaneousMusic" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SimultaneousMusic,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode" [color=black,
                  fontcolor=white,
                  group=2,
                  label=SyntaxNode,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondparsertools.Music.Music" -> "abjad.tools.lilypondparsertools.ContextSpeccedMusic.ContextSpeccedMusic";
              "abjad.tools.lilypondparsertools.Music.Music" -> "abjad.tools.lilypondparsertools.SequentialMusic.SequentialMusic";
              "abjad.tools.lilypondparsertools.Music.Music" -> "abjad.tools.lilypondparsertools.SimultaneousMusic.SimultaneousMusic";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.GuileProxy.GuileProxy";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondDuration.LilyPondDuration";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondEvent.LilyPondEvent";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondFraction.LilyPondFraction";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondGrammarGenerator.LilyPondGrammarGenerator";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondSyntacticalDefinition.LilyPondSyntacticalDefinition";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.Music.Music";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.SyntaxNode.SyntaxNode";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.LilyPondParser.LilyPondParser";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser";
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.SchemeParser.SchemeParser";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Abstract Classes
----------------

.. toctree::
   :hidden:

   Music
   SimultaneousMusic

.. autosummary::
   :nosignatures:

   Music
   SimultaneousMusic

--------

Classes
-------

.. toctree::
   :hidden:

   ContextSpeccedMusic
   GuileProxy
   LilyPondDuration
   LilyPondEvent
   LilyPondFraction
   LilyPondGrammarGenerator
   LilyPondLexicalDefinition
   LilyPondParser
   LilyPondSyntacticalDefinition
   ReducedLyParser
   SchemeParser
   SequentialMusic
   SyntaxNode

.. autosummary::
   :nosignatures:

   ContextSpeccedMusic
   GuileProxy
   LilyPondDuration
   LilyPondEvent
   LilyPondFraction
   LilyPondGrammarGenerator
   LilyPondLexicalDefinition
   LilyPondParser
   LilyPondSyntacticalDefinition
   ReducedLyParser
   SchemeParser
   SequentialMusic
   SyntaxNode

--------

Functions
---------

.. toctree::
   :hidden:

   parse_reduced_ly_syntax

.. autosummary::
   :nosignatures:

   parse_reduced_ly_syntax
