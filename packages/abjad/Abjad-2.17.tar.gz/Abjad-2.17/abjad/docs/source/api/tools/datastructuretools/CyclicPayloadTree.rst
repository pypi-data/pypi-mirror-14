.. currentmodule:: abjad.tools.datastructuretools

CyclicPayloadTree
=================

.. autoclass:: CyclicPayloadTree

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
              "abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>CyclicPayloadTree</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.PayloadTree.PayloadTree" [color=3,
                  group=2,
                  label=PayloadTree,
                  shape=box];
              "abjad.tools.datastructuretools.PayloadTree.PayloadTree" -> "abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.PayloadTree.PayloadTree";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.PayloadTree`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.children
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.depth
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.expr
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.get_manifest_payload_of_next_n_nodes_at_level
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.get_next_n_complete_nodes_at_level
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.get_next_n_nodes_at_level
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.get_node_at_position
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.get_position_of_descendant
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.improper_parentage
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.index
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.index_in_parent
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.is_at_level
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.item_class
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.iterate_at_level
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.iterate_depth_first
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.iterate_forever_depth_first
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.iterate_payload
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.level
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.manifest_payload
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.negative_level
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.payload
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.position
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.proper_parentage
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.remove_node
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.remove_to_root
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.root
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.to_nested_lists
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.width
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__contains__
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__eq__
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__format__
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__getitem__
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__graph__
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__hash__
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__iter__
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__len__
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__ne__
      ~abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.expr

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.index_in_parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.level

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.manifest_payload

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.negative_level

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.payload

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.position

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.root

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.width

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.get_manifest_payload_of_next_n_nodes_at_level

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.get_next_n_complete_nodes_at_level

.. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.get_next_n_nodes_at_level

.. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.get_node_at_position

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.get_position_of_descendant

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.is_at_level

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.iterate_at_level

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.iterate_depth_first

.. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.iterate_forever_depth_first

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.iterate_payload

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.remove_node

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.remove_to_root

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.to_nested_lists

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__eq__

.. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__hash__

.. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.CyclicPayloadTree.CyclicPayloadTree.__repr__
