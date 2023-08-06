.. currentmodule:: abjad.tools.systemtools

Configuration
=============

.. autoclass:: Configuration

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
              "abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration" [color=4,
                  group=3,
                  label=AbjadConfiguration,
                  shape=box];
              "abjad.tools.systemtools.Configuration.Configuration" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>Configuration</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.systemtools.Configuration.Configuration" -> "abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          subgraph cluster_idetools {
              graph [label=idetools];
              "ide.tools.idetools.AbjadIDEConfiguration.AbjadIDEConfiguration" [color=3,
                  group=2,
                  label=AbjadIDEConfiguration,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.Configuration.Configuration";
          "abjad.tools.systemtools.Configuration.Configuration" -> "ide.tools.idetools.AbjadIDEConfiguration.AbjadIDEConfiguration";
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

      ~abjad.tools.systemtools.Configuration.Configuration.configuration_directory_name
      ~abjad.tools.systemtools.Configuration.Configuration.configuration_directory_path
      ~abjad.tools.systemtools.Configuration.Configuration.configuration_file_name
      ~abjad.tools.systemtools.Configuration.Configuration.configuration_file_path
      ~abjad.tools.systemtools.Configuration.Configuration.home_directory
      ~abjad.tools.systemtools.Configuration.Configuration.temp_directory
      ~abjad.tools.systemtools.Configuration.Configuration.__delitem__
      ~abjad.tools.systemtools.Configuration.Configuration.__eq__
      ~abjad.tools.systemtools.Configuration.Configuration.__format__
      ~abjad.tools.systemtools.Configuration.Configuration.__getitem__
      ~abjad.tools.systemtools.Configuration.Configuration.__hash__
      ~abjad.tools.systemtools.Configuration.Configuration.__iter__
      ~abjad.tools.systemtools.Configuration.Configuration.__len__
      ~abjad.tools.systemtools.Configuration.Configuration.__ne__
      ~abjad.tools.systemtools.Configuration.Configuration.__repr__
      ~abjad.tools.systemtools.Configuration.Configuration.__setitem__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.systemtools.Configuration.Configuration.configuration_directory_name

.. autoattribute:: abjad.tools.systemtools.Configuration.Configuration.configuration_directory_path

.. autoattribute:: abjad.tools.systemtools.Configuration.Configuration.configuration_file_name

.. autoattribute:: abjad.tools.systemtools.Configuration.Configuration.configuration_file_path

.. autoattribute:: abjad.tools.systemtools.Configuration.Configuration.home_directory

.. autoattribute:: abjad.tools.systemtools.Configuration.Configuration.temp_directory

Special methods
---------------

.. automethod:: abjad.tools.systemtools.Configuration.Configuration.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Configuration.Configuration.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Configuration.Configuration.__format__

.. automethod:: abjad.tools.systemtools.Configuration.Configuration.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Configuration.Configuration.__hash__

.. automethod:: abjad.tools.systemtools.Configuration.Configuration.__iter__

.. automethod:: abjad.tools.systemtools.Configuration.Configuration.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Configuration.Configuration.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.Configuration.Configuration.__repr__

.. automethod:: abjad.tools.systemtools.Configuration.Configuration.__setitem__
