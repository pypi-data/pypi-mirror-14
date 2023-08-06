.. currentmodule:: abjad.tools.systemtools

StorageFormatManager
====================

.. autoclass:: StorageFormatManager

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
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.StorageFormatManager.StorageFormatManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>StorageFormatManager</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.StorageFormatManager.StorageFormatManager";
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

      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.accepts_kwargs
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.compare
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.format_one_value
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_format_pieces
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_hash_values
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_import_statements
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_indentation_strings
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_input_argument_values
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_keyword_argument_dictionary
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_keyword_argument_names
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_keyword_argument_values
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_positional_argument_dictionary
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_positional_argument_names
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_positional_argument_values
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_repr_format
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_root_package_name
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_signature_keyword_argument_names
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_signature_positional_argument_names
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_storage_format
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_tools_package_name
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_tools_package_qualified_class_name
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_types
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_unique_python_path_parts
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.is_instance
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.__eq__
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.__format__
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.__hash__
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.__ne__
      ~abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.__repr__

Class & static methods
----------------------

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.accepts_kwargs

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.compare

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.format_one_value

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_format_pieces

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_hash_values

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_import_statements

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_indentation_strings

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_input_argument_values

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_keyword_argument_dictionary

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_keyword_argument_names

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_keyword_argument_values

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_positional_argument_dictionary

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_positional_argument_names

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_positional_argument_values

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_repr_format

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_root_package_name

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_signature_keyword_argument_names

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_signature_positional_argument_names

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_storage_format

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_tools_package_name

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_tools_package_qualified_class_name

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_types

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.get_unique_python_path_parts

.. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.is_instance

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatManager.StorageFormatManager.__repr__
