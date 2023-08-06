.. currentmodule:: abjad.tools.documentationtools

DocumentationManager
====================

.. autoclass:: DocumentationManager

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
          subgraph cluster_documentationtools {
              graph [label=documentationtools];
              "abjad.tools.documentationtools.DocumentationManager.DocumentationManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>DocumentationManager</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.documentationtools.DocumentationManager.DocumentationManager";
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

      ~abjad.tools.documentationtools.DocumentationManager.DocumentationManager.execute
      ~abjad.tools.documentationtools.DocumentationManager.DocumentationManager.make_readme
      ~abjad.tools.documentationtools.DocumentationManager.DocumentationManager.prefix_ignored
      ~abjad.tools.documentationtools.DocumentationManager.DocumentationManager.prefix_preserved
      ~abjad.tools.documentationtools.DocumentationManager.DocumentationManager.prefix_pruned
      ~abjad.tools.documentationtools.DocumentationManager.DocumentationManager.prefix_rewrote
      ~abjad.tools.documentationtools.DocumentationManager.DocumentationManager.prefix_wrote
      ~abjad.tools.documentationtools.DocumentationManager.DocumentationManager.__eq__
      ~abjad.tools.documentationtools.DocumentationManager.DocumentationManager.__format__
      ~abjad.tools.documentationtools.DocumentationManager.DocumentationManager.__hash__
      ~abjad.tools.documentationtools.DocumentationManager.DocumentationManager.__ne__
      ~abjad.tools.documentationtools.DocumentationManager.DocumentationManager.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.documentationtools.DocumentationManager.DocumentationManager.prefix_ignored

.. autoattribute:: abjad.tools.documentationtools.DocumentationManager.DocumentationManager.prefix_preserved

.. autoattribute:: abjad.tools.documentationtools.DocumentationManager.DocumentationManager.prefix_pruned

.. autoattribute:: abjad.tools.documentationtools.DocumentationManager.DocumentationManager.prefix_rewrote

.. autoattribute:: abjad.tools.documentationtools.DocumentationManager.DocumentationManager.prefix_wrote

Methods
-------

.. automethod:: abjad.tools.documentationtools.DocumentationManager.DocumentationManager.execute

Class & static methods
----------------------

.. automethod:: abjad.tools.documentationtools.DocumentationManager.DocumentationManager.make_readme

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.DocumentationManager.DocumentationManager.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.DocumentationManager.DocumentationManager.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.DocumentationManager.DocumentationManager.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.DocumentationManager.DocumentationManager.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.DocumentationManager.DocumentationManager.__repr__
