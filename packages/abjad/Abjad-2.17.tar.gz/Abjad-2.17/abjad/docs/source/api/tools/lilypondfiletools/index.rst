lilypondfiletools
=================

.. automodule:: abjad.tools.lilypondfiletools

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_lilypondfiletools {
              graph [label=lilypondfiletools];
              "abjad.tools.lilypondfiletools.Block.Block" [color=black,
                  fontcolor=white,
                  group=2,
                  label=Block,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondfiletools.ContextBlock.ContextBlock" [color=black,
                  fontcolor=white,
                  group=2,
                  label=ContextBlock,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondfiletools.DateTimeToken.DateTimeToken" [color=black,
                  fontcolor=white,
                  group=2,
                  label=DateTimeToken,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondfiletools.LilyPondDimension.LilyPondDimension" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondDimension,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondFile,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondfiletools.LilyPondLanguageToken.LilyPondLanguageToken" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondLanguageToken,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken" [color=black,
                  fontcolor=white,
                  group=2,
                  label=LilyPondVersionToken,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondfiletools.PackageGitCommitToken.PackageGitCommitToken" [color=black,
                  fontcolor=white,
                  group=2,
                  label=PackageGitCommitToken,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondfiletools.Block.Block" -> "abjad.tools.lilypondfiletools.ContextBlock.ContextBlock";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.Block.Block";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.DateTimeToken.DateTimeToken";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.LilyPondDimension.LilyPondDimension";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondfiletools.LilyPondLanguageToken.LilyPondLanguageToken";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondfiletools.PackageGitCommitToken.PackageGitCommitToken";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   Block
   ContextBlock
   DateTimeToken
   LilyPondDimension
   LilyPondFile
   LilyPondLanguageToken
   LilyPondVersionToken
   PackageGitCommitToken

.. autosummary::
   :nosignatures:

   Block
   ContextBlock
   DateTimeToken
   LilyPondDimension
   LilyPondFile
   LilyPondLanguageToken
   LilyPondVersionToken
   PackageGitCommitToken

--------

Functions
---------

.. toctree::
   :hidden:

   make_basic_lilypond_file
   make_floating_time_signature_lilypond_file

.. autosummary::
   :nosignatures:

   make_basic_lilypond_file
   make_floating_time_signature_lilypond_file
