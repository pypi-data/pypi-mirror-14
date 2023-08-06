.. currentmodule:: abjad.tools.abjadbooktools

LaTeXDocumentHandler
====================

.. autoclass:: LaTeXDocumentHandler

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
              "abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>LaTeXDocumentHandler</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler";
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

      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.assets_directory
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.collect_asset_output_proxies
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.collect_input_blocks
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.collect_output_blocks
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.console
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.errored
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.extract_code_block_options
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.from_path
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.get_default_stylesheet
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.input_directory
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.input_file_contents
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.input_file_path
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.interpret_input_blocks
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.latex_assets_prefix
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.latex_root_directory
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.rebuild_source
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.register_error
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.render_asset_output_proxies
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.report
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.unregister_error
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.write_rebuilt_source
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.__call__
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.__eq__
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.__format__
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.__hash__
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.__ne__
      ~abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.assets_directory

.. autoattribute:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.console

.. autoattribute:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.errored

.. autoattribute:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.input_directory

.. autoattribute:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.input_file_contents

.. autoattribute:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.input_file_path

.. autoattribute:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.latex_assets_prefix

.. autoattribute:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.latex_root_directory

Methods
-------

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.collect_asset_output_proxies

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.collect_input_blocks

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.collect_output_blocks

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.get_default_stylesheet

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.interpret_input_blocks

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.rebuild_source

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.register_error

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.render_asset_output_proxies

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.report

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.unregister_error

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.write_rebuilt_source

Class & static methods
----------------------

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.extract_code_block_options

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.from_path

Special methods
---------------

.. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.LaTeXDocumentHandler.LaTeXDocumentHandler.__repr__
