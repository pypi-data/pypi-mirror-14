.. currentmodule:: abjad.tools.systemtools

AbjadConfiguration
==================

.. autoclass:: AbjadConfiguration

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
              "abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>AbjadConfiguration</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.Configuration.Configuration" [color=3,
                  group=2,
                  label=Configuration,
                  shape=oval,
                  style=bold];
              "abjad.tools.systemtools.Configuration.Configuration" -> "abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.Configuration.Configuration";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.systemtools.Configuration`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.abjad_boilerplate_directory
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.abjad_directory
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.abjad_experimental_directory
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.abjad_output_directory
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.abjad_root_directory
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.configuration_directory_name
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.configuration_directory_path
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.configuration_file_name
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.configuration_file_path
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_abjad_startup_string
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_abjad_version_string
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_lilypond_minimum_version_string
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_lilypond_version_string
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_python_version_string
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_tab_width
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_text_editor
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.home_directory
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.lilypond_log_file_path
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.list_package_dependency_versions
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.set_default_accidental_spelling
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.temp_directory
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__delitem__
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__eq__
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__format__
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__getitem__
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__hash__
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__iter__
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__len__
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__ne__
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__repr__
      ~abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__setitem__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.abjad_boilerplate_directory

.. autoattribute:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.abjad_directory

.. autoattribute:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.abjad_experimental_directory

.. autoattribute:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.abjad_output_directory

.. autoattribute:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.abjad_root_directory

.. autoattribute:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.configuration_directory_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.configuration_directory_path

.. autoattribute:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.configuration_file_name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.configuration_file_path

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.home_directory

.. autoattribute:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.lilypond_log_file_path

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.temp_directory

Class & static methods
----------------------

.. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_abjad_startup_string

.. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_abjad_version_string

.. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_lilypond_minimum_version_string

.. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_lilypond_version_string

.. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_python_version_string

.. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_tab_width

.. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.get_text_editor

.. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.list_package_dependency_versions

.. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.set_default_accidental_spelling

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration.__setitem__
