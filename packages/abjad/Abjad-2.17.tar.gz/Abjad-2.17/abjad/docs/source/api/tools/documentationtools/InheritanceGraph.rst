.. currentmodule:: abjad.tools.documentationtools

InheritanceGraph
================

.. autoclass:: InheritanceGraph

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
              "abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>InheritanceGraph</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph";
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

      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.addresses
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.child_parents_mapping
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.immediate_classes
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.lineage_addresses
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.lineage_classes
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.lineage_distance_mapping
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.lineage_prune_distance
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.parent_children_mapping
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.recurse_into_submodules
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.root_addresses
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.root_classes
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.use_clusters
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.use_groups
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.__eq__
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.__format__
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.__graph__
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.__hash__
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.__ne__
      ~abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.addresses

.. autoattribute:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.child_parents_mapping

.. autoattribute:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.immediate_classes

.. autoattribute:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.lineage_addresses

.. autoattribute:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.lineage_classes

.. autoattribute:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.lineage_distance_mapping

.. autoattribute:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.lineage_prune_distance

.. autoattribute:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.parent_children_mapping

.. autoattribute:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.recurse_into_submodules

.. autoattribute:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.root_addresses

.. autoattribute:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.root_classes

.. autoattribute:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.use_clusters

.. autoattribute:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.use_groups

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.__format__

.. automethod:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.documentationtools.InheritanceGraph.InheritanceGraph.__repr__
