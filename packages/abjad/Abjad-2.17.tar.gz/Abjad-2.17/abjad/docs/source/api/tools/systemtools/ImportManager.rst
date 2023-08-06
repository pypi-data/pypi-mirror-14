.. currentmodule:: abjad.tools.systemtools

ImportManager
=============

.. autoclass:: ImportManager

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
              "abjad.tools.systemtools.ImportManager.ImportManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ImportManager</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.ImportManager.ImportManager";
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

      ~abjad.tools.systemtools.ImportManager.ImportManager.import_material_packages
      ~abjad.tools.systemtools.ImportManager.ImportManager.import_nominative_modules
      ~abjad.tools.systemtools.ImportManager.ImportManager.import_public_names_from_path_into_namespace
      ~abjad.tools.systemtools.ImportManager.ImportManager.import_structured_package
      ~abjad.tools.systemtools.ImportManager.ImportManager.__eq__
      ~abjad.tools.systemtools.ImportManager.ImportManager.__format__
      ~abjad.tools.systemtools.ImportManager.ImportManager.__hash__
      ~abjad.tools.systemtools.ImportManager.ImportManager.__ne__
      ~abjad.tools.systemtools.ImportManager.ImportManager.__repr__

Class & static methods
----------------------

.. automethod:: abjad.tools.systemtools.ImportManager.ImportManager.import_material_packages

.. automethod:: abjad.tools.systemtools.ImportManager.ImportManager.import_nominative_modules

.. automethod:: abjad.tools.systemtools.ImportManager.ImportManager.import_public_names_from_path_into_namespace

.. automethod:: abjad.tools.systemtools.ImportManager.ImportManager.import_structured_package

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ImportManager.ImportManager.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ImportManager.ImportManager.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ImportManager.ImportManager.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ImportManager.ImportManager.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.ImportManager.ImportManager.__repr__
