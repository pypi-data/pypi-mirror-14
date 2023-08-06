.. currentmodule:: abjad.tools.pitchtools

PitchClassTree
==============

.. autoclass:: PitchClassTree

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
              "abjad.tools.datastructuretools.PayloadTree.PayloadTree" [color=3,
                  group=2,
                  label=PayloadTree,
                  shape=box];
          }
          subgraph cluster_pitchtools {
              graph [label=pitchtools];
              "abjad.tools.pitchtools.PitchClassTree.PitchClassTree" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PitchClassTree</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.PayloadTree.PayloadTree";
          "abjad.tools.datastructuretools.PayloadTree.PayloadTree" -> "abjad.tools.pitchtools.PitchClassTree.PitchClassTree";
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

      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.children
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.depth
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.expr
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.get_manifest_payload_of_next_n_nodes_at_level
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.get_next_n_complete_nodes_at_level
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.get_next_n_nodes_at_level
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.get_node_at_position
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.get_position_of_descendant
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.improper_parentage
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.index
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.index_in_parent
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.is_at_level
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.item_class
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.iterate_at_level
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.iterate_depth_first
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.iterate_payload
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.level
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.manifest_payload
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.negative_level
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.payload
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.position
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.proper_parentage
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.remove_node
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.remove_to_root
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.root
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.to_nested_lists
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.width
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__contains__
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__eq__
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__format__
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__getitem__
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__graph__
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__hash__
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__illustrate__
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__len__
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__ne__
      ~abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.children

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.depth

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.expr

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.improper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.index_in_parent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.level

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.manifest_payload

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.negative_level

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.payload

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.position

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.proper_parentage

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.root

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.width

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.get_manifest_payload_of_next_n_nodes_at_level

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.get_next_n_complete_nodes_at_level

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.get_next_n_nodes_at_level

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.get_node_at_position

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.get_position_of_descendant

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.is_at_level

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.iterate_at_level

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.iterate_depth_first

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.iterate_payload

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.remove_node

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.remove_to_root

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.to_nested_lists

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__hash__

.. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.pitchtools.PitchClassTree.PitchClassTree.__repr__
