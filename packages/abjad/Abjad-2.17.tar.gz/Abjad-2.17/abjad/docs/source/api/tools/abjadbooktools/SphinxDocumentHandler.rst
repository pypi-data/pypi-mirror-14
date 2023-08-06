.. currentmodule:: abjad.tools.abjadbooktools

SphinxDocumentHandler
=====================

.. autoclass:: SphinxDocumentHandler

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
              "abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>SphinxDocumentHandler</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler";
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

      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.cleanup_graphviz_svg
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.collect_abjad_input_blocks
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.collect_python_literal_blocks
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.errored
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.find_target_file_paths
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.get_default_stylesheet
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.get_file_base_name
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.get_image_directory_paths
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.get_source_extension
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.install_lightbox_static_files
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.interpret_code_blocks
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.interpret_image_source
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.interpret_input_blocks
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.on_build_finished
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.on_builder_inited
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.on_doctree_read
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.on_env_updated
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.parse_rst
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.postprocess_image_target
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.rebuild_document
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.register_error
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.render_png_image
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.render_svg_image
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.render_thumbnails
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.setup_sphinx_extension
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.should_ignore_document
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.style_document
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.unregister_error
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_import_block
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_input_block
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_output_block_html
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_output_block_latex
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_reveal_block
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_thumbnail_block_html
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_thumbnail_block_latex
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.write_image_source
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.__eq__
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.__format__
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.__hash__
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.__ne__
      ~abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.errored

Methods
-------

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.collect_abjad_input_blocks

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.collect_python_literal_blocks

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.get_default_stylesheet

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.interpret_input_blocks

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.rebuild_document

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.register_error

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.unregister_error

Class & static methods
----------------------

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.cleanup_graphviz_svg

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.find_target_file_paths

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.get_file_base_name

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.get_image_directory_paths

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.get_source_extension

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.install_lightbox_static_files

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.interpret_code_blocks

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.interpret_image_source

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.on_build_finished

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.on_builder_inited

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.on_doctree_read

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.on_env_updated

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.parse_rst

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.postprocess_image_target

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.render_png_image

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.render_svg_image

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.render_thumbnails

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.setup_sphinx_extension

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.should_ignore_document

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.style_document

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_import_block

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_input_block

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_output_block_html

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_output_block_latex

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_reveal_block

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_thumbnail_block_html

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.visit_abjad_thumbnail_block_latex

.. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.write_image_source

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.SphinxDocumentHandler.SphinxDocumentHandler.__repr__
