.. currentmodule:: abjad.tools.abjadbooktools

CodeBlock
=========

.. autoclass:: CodeBlock

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_abjadbooktools {
              graph [label=abjadbooktools];
              "abjad.tools.abjadbooktools.CodeBlock.CodeBlock" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>CodeBlock</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=3,
                  group=2,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.CodeBlock.CodeBlock";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.as_docutils
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.as_latex
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.code_block_specifier
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.current_lines
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.document_source
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.executed_lines
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.filter_output_proxies
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.flush
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.from_docutils_abjad_import_block
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.from_docutils_abjad_input_block
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.from_docutils_literal_block
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.from_latex_abjad_block
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.from_latex_abjadextract_block
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.graph
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.image_layout_specifier
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.image_render_specifier
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.input_file_contents
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.interpret
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.output_proxies
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.play
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.print
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.push_asset_output_proxy
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.push_code_output_proxy
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.push_line_to_console
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.quit
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.setup_capture_hooks
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.show
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.starting_line_number
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.write
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.__copy__
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.__eq__
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.__format__
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.__hash__
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.__ne__
      ~abjad.tools.abjadbooktools.CodeBlock.CodeBlock.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.code_block_specifier

.. autoattribute:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.current_lines

.. autoattribute:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.document_source

.. autoattribute:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.executed_lines

.. autoattribute:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.image_layout_specifier

.. autoattribute:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.image_render_specifier

.. autoattribute:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.input_file_contents

.. autoattribute:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.output_proxies

.. autoattribute:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.starting_line_number

Methods
-------

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.as_docutils

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.as_latex

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.filter_output_proxies

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.flush

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.graph

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.interpret

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.play

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.print

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.push_asset_output_proxy

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.push_code_output_proxy

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.push_line_to_console

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.quit

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.setup_capture_hooks

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.show

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.write

Class & static methods
----------------------

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.from_docutils_abjad_import_block

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.from_docutils_abjad_input_block

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.from_docutils_literal_block

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.from_latex_abjad_block

.. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.from_latex_abjadextract_block

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.CodeBlock.CodeBlock.__repr__
