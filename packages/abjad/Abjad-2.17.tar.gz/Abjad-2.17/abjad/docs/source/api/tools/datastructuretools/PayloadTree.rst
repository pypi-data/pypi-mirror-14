.. currentmodule:: abjad.tools.datastructuretools

PayloadTree
===========

.. autoclass:: PayloadTree

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
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree" [color=3,
                  group=2,
                  label=CyclicPayloadTree,
                  shape=box];
              "abjad.tools.datastructuretools.PayloadTree.PayloadTree" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>PayloadTree</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.PayloadTree.PayloadTree" -> "abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree";
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.PitchClassTree.PitchClassTree" [color=4,
                  group=3,
                  label=PitchClassTree,
                  shape=box];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.PayloadTree.PayloadTree";
          "abjad.tools.datastructuretools.PayloadTree.PayloadTree" -> "abjad.tools.pitchtools.PitchClassTree.PitchClassTree";
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

      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.children
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.depth
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.expr
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.get_manifest_payload_of_next_n_nodes_at_level
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.get_next_n_complete_nodes_at_level
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.get_next_n_nodes_at_level
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.get_node_at_position
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.get_position_of_descendant
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.improper_parentage
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.index
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.index_in_parent
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.is_at_level
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.item_class
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.iterate_at_level
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.iterate_depth_first
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.iterate_payload
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.level
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.manifest_payload
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.negative_level
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.payload
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.position
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.proper_parentage
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.remove_node
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.remove_to_root
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.root
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.to_nested_lists
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.width
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.__contains__
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.__eq__
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.__format__
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.__getitem__
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.__graph__
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.__hash__
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.__len__
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.__ne__
      ~abjad.tools.datastructuretools.PayloadTree.PayloadTree.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.children

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.depth

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.expr

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.improper_parentage

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.index_in_parent

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.item_class

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.level

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.manifest_payload

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.negative_level

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.payload

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.position

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.proper_parentage

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.root

.. autoattribute:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.width

Methods
-------

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.get_manifest_payload_of_next_n_nodes_at_level

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.get_next_n_complete_nodes_at_level

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.get_next_n_nodes_at_level

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.get_node_at_position

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.get_position_of_descendant

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.index

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.is_at_level

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.iterate_at_level

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.iterate_depth_first

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.iterate_payload

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.remove_node

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.remove_to_root

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.to_nested_lists

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.__contains__

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.__eq__

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.__format__

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.__getitem__

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.__graph__

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.__hash__

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.__ne__

.. automethod:: abjad.tools.datastructuretools.PayloadTree.PayloadTree.__repr__
