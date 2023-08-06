abjadbooktools
==============

.. automodule:: abjad.tools.abjadbooktools

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
          subgraph cluster_abjadbooktools {
              graph [label=abjadbooktools];
              "abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole" [color=black,
                  fontcolor=white,
                  group=1,
                  label=AbjadBookConsole,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.AbjadBookError.AbjadBookError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=AbjadBookError,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript" [color=black,
                  fontcolor=white,
                  group=1,
                  label=AbjadBookScript,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective" [color=black,
                  fontcolor=white,
                  group=1,
                  label=AbjadDirective,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.CodeBlock.CodeBlock" [color=black,
                  fontcolor=white,
                  group=1,
                  label=CodeBlock,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier" [color=black,
                  fontcolor=white,
                  group=1,
                  label=CodeBlockSpecifier,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.CodeOutputProxy.CodeOutputProxy" [color=black,
                  fontcolor=white,
                  group=1,
                  label=CodeOutputProxy,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.DoctestDirective.DoctestDirective" [color=black,
                  fontcolor=white,
                  group=1,
                  label=DoctestDirective,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy" [color=black,
                  fontcolor=white,
                  group=1,
                  label=GraphvizOutputProxy,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier" [color=black,
                  fontcolor=white,
                  group=1,
                  label=ImageLayoutSpecifier,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" [color=black,
                  fontcolor=white,
                  group=1,
                  label=ImageOutputProxy,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.ImageRenderSpecifier.ImageRenderSpecifier" [color=black,
                  fontcolor=white,
                  group=1,
                  label=ImageRenderSpecifier,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.ImportDirective.ImportDirective" [color=black,
                  fontcolor=white,
                  group=1,
                  label=ImportDirective,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler" [color=black,
                  fontcolor=white,
                  group=1,
                  label=LaTeXDocumentHandler,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.LilyPondOutputProxy.LilyPondOutputProxy" [color=black,
                  fontcolor=white,
                  group=1,
                  label=LilyPondOutputProxy,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.RevealDirective.RevealDirective" [color=black,
                  fontcolor=white,
                  group=1,
                  label=RevealDirective,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.ShellDirective.ShellDirective" [color=black,
                  fontcolor=white,
                  group=1,
                  label=ShellDirective,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler" [color=black,
                  fontcolor=white,
                  group=1,
                  label=SphinxDocumentHandler,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective" [color=black,
                  fontcolor=white,
                  group=1,
                  label=ThumbnailDirective,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.abjad_import_block.abjad_import_block" [color=black,
                  fontcolor=white,
                  group=1,
                  label=abjad_import_block,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.abjad_input_block.abjad_input_block" [color=black,
                  fontcolor=white,
                  group=1,
                  label=abjad_input_block,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.abjad_output_block.abjad_output_block" [color=black,
                  fontcolor=white,
                  group=1,
                  label=abjad_output_block,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.abjad_reveal_block.abjad_reveal_block" [color=black,
                  fontcolor=white,
                  group=1,
                  label=abjad_reveal_block,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.abjad_thumbnail_block.abjad_thumbnail_block" [color=black,
                  fontcolor=white,
                  group=1,
                  label=abjad_thumbnail_block,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" -> "abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy";
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" -> "abjad.tools.abjadbooktools.LilyPondOutputProxy.LilyPondOutputProxy";
          }
          subgraph cluster_developerscripttools {
              graph [label=developerscripttools];
              "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" [color=5,
                  group=4,
                  label=DeveloperScript,
                  shape=oval,
                  style=bold];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.BaseException" [color=3,
                  group=2,
                  label=BaseException,
                  shape=box];
              "builtins.Exception" [color=3,
                  group=2,
                  label=Exception,
                  shape=box];
              "builtins.object" [color=3,
                  group=2,
                  label=object,
                  shape=box];
              "builtins.BaseException" -> "builtins.Exception";
              "builtins.object" -> "builtins.BaseException";
          }
          subgraph cluster_code {
              graph [label=code];
              "code.InteractiveConsole" [color=4,
                  group=3,
                  label=InteractiveConsole,
                  shape=box];
              "code.InteractiveInterpreter" [color=4,
                  group=3,
                  label=InteractiveInterpreter,
                  shape=box];
              "code.InteractiveInterpreter" -> "code.InteractiveConsole";
          }
          subgraph cluster_docutils {
              graph [label=docutils];
              "docutils.nodes.Body" [color=6,
                  group=5,
                  label=Body,
                  shape=box];
              "docutils.nodes.Element" [color=6,
                  group=5,
                  label=Element,
                  shape=box];
              "docutils.nodes.FixedTextElement" [color=6,
                  group=5,
                  label=FixedTextElement,
                  shape=box];
              "docutils.nodes.General" [color=6,
                  group=5,
                  label=General,
                  shape=box];
              "docutils.nodes.Inline" [color=6,
                  group=5,
                  label=Inline,
                  shape=box];
              "docutils.nodes.Node" [color=6,
                  group=5,
                  label="Node",
                  shape=box];
              "docutils.nodes.TextElement" [color=6,
                  group=5,
                  label=TextElement,
                  shape=box];
              "docutils.nodes.image" [color=6,
                  group=5,
                  label=image,
                  shape=box];
              "docutils.parsers.rst.Directive" [color=6,
                  group=5,
                  label=Directive,
                  shape=box];
              "docutils.nodes.Body" -> "docutils.nodes.General";
              "docutils.nodes.Element" -> "docutils.nodes.TextElement";
              "docutils.nodes.Element" -> "docutils.nodes.image";
              "docutils.nodes.General" -> "docutils.nodes.image";
              "docutils.nodes.Inline" -> "docutils.nodes.image";
              "docutils.nodes.Node" -> "docutils.nodes.Element";
              "docutils.nodes.TextElement" -> "docutils.nodes.FixedTextElement";
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.CodeBlock.CodeBlock";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.CodeBlockSpecifier.CodeBlockSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.CodeOutputProxy.CodeOutputProxy";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy";
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.ImageRenderSpecifier.ImageRenderSpecifier";
          "abjad.tools.developerscripttools.DeveloperScript.DeveloperScript" -> "abjad.tools.abjadbooktools.AbjadBookScript.AbjadBookScript";
          "builtins.Exception" -> "abjad.tools.abjadbooktools.AbjadBookError.AbjadBookError";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
          "builtins.object" -> "code.InteractiveInterpreter";
          "builtins.object" -> "docutils.nodes.Body";
          "builtins.object" -> "docutils.nodes.Inline";
          "builtins.object" -> "docutils.nodes.Node";
          "builtins.object" -> "docutils.parsers.rst.Directive";
          "code.InteractiveConsole" -> "abjad.tools.abjadbooktools.AbjadBookConsole.AbjadBookConsole";
          "docutils.nodes.Element" -> "abjad.tools.abjadbooktools.abjad_import_block.abjad_import_block";
          "docutils.nodes.Element" -> "abjad.tools.abjadbooktools.abjad_input_block.abjad_input_block";
          "docutils.nodes.Element" -> "abjad.tools.abjadbooktools.abjad_reveal_block.abjad_reveal_block";
          "docutils.nodes.Element" -> "abjad.tools.abjadbooktools.abjad_thumbnail_block.abjad_thumbnail_block";
          "docutils.nodes.FixedTextElement" -> "abjad.tools.abjadbooktools.abjad_output_block.abjad_output_block";
          "docutils.nodes.General" -> "abjad.tools.abjadbooktools.abjad_import_block.abjad_import_block";
          "docutils.nodes.General" -> "abjad.tools.abjadbooktools.abjad_input_block.abjad_input_block";
          "docutils.nodes.General" -> "abjad.tools.abjadbooktools.abjad_output_block.abjad_output_block";
          "docutils.nodes.General" -> "abjad.tools.abjadbooktools.abjad_reveal_block.abjad_reveal_block";
          "docutils.nodes.General" -> "abjad.tools.abjadbooktools.abjad_thumbnail_block.abjad_thumbnail_block";
          "docutils.nodes.image" -> "abjad.tools.abjadbooktools.abjad_thumbnail_block.abjad_thumbnail_block";
          "docutils.parsers.rst.Directive" -> "abjad.tools.abjadbooktools.AbjadDirective.AbjadDirective";
          "docutils.parsers.rst.Directive" -> "abjad.tools.abjadbooktools.DoctestDirective.DoctestDirective";
          "docutils.parsers.rst.Directive" -> "abjad.tools.abjadbooktools.ImportDirective.ImportDirective";
          "docutils.parsers.rst.Directive" -> "abjad.tools.abjadbooktools.RevealDirective.RevealDirective";
          "docutils.parsers.rst.Directive" -> "abjad.tools.abjadbooktools.ShellDirective.ShellDirective";
          "docutils.parsers.rst.Directive" -> "abjad.tools.abjadbooktools.ThumbnailDirective.ThumbnailDirective";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   ThumbnailDirective

.. autosummary::
   :nosignatures:

   ThumbnailDirective

--------

Document Handlers
-----------------

.. toctree::
   :hidden:

   LaTeXDocumentHandler
   SphinxDocumentHandler

.. autosummary::
   :nosignatures:

   LaTeXDocumentHandler
   SphinxDocumentHandler

--------

Entry Points
------------

.. toctree::
   :hidden:

   AbjadBookScript

.. autosummary::
   :nosignatures:

   AbjadBookScript

--------

Internals
---------

.. toctree::
   :hidden:

   AbjadBookConsole
   CodeBlock
   CodeBlockSpecifier
   ImageLayoutSpecifier
   ImageRenderSpecifier

.. autosummary::
   :nosignatures:

   AbjadBookConsole
   CodeBlock
   CodeBlockSpecifier
   ImageLayoutSpecifier
   ImageRenderSpecifier

--------

Output Proxies
--------------

.. toctree::
   :hidden:

   CodeOutputProxy
   GraphvizOutputProxy
   ImageOutputProxy
   LilyPondOutputProxy

.. autosummary::
   :nosignatures:

   CodeOutputProxy
   GraphvizOutputProxy
   ImageOutputProxy
   LilyPondOutputProxy

--------

Sphinx Internals
----------------

.. toctree::
   :hidden:

   AbjadDirective
   DoctestDirective
   ImportDirective
   RevealDirective
   ShellDirective

.. autosummary::
   :nosignatures:

   AbjadDirective
   DoctestDirective
   ImportDirective
   RevealDirective
   ShellDirective

--------

Errors
------

.. toctree::
   :hidden:

   AbjadBookError

.. autosummary::
   :nosignatures:

   AbjadBookError

--------

Functions
---------

.. toctree::
   :hidden:

   example_function
   run_abjad_book

.. autosummary::
   :nosignatures:

   example_function
   run_abjad_book
