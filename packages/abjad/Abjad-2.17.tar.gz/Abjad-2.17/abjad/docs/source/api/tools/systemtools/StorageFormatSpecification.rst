.. currentmodule:: abjad.tools.systemtools

StorageFormatSpecification
==========================

.. autoclass:: StorageFormatSpecification

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
              "abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>StorageFormatSpecification</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification";
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

      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.body_text
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.instance
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.is_bracketed
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.is_indented
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.keyword_argument_callables
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.keyword_argument_names
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.keywords_ignored_when_false
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.positional_argument_values
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.storage_format_pieces
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.tools_package_name
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.__eq__
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.__format__
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.__hash__
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.__ne__
      ~abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.body_text

.. autoattribute:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.instance

.. autoattribute:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.is_bracketed

.. autoattribute:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.is_indented

.. autoattribute:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.keyword_argument_callables

.. autoattribute:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.keyword_argument_names

.. autoattribute:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.keywords_ignored_when_false

.. autoattribute:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.positional_argument_values

.. autoattribute:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.storage_format_pieces

.. autoattribute:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.tools_package_name

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification.__repr__
