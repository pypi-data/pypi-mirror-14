.. currentmodule:: abjad.tools.rhythmmakertools

PartitionTable
==============

.. autoclass:: PartitionTable

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
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict" [color=3,
                  group=2,
                  label=TypedOrderedDict,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict";
          }
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.PartitionTable.PartitionTable" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PartitionTable</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict" -> "abjad.tools.rhythmmakertools.PartitionTable.PartitionTable";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TypedOrderedDict`

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.clear
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.copy
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.get
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.has_key
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.item_class
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.items
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.keys
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.pop
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.popitem
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.respell_division
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.setdefault
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.update
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.values
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__cmp__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__contains__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__delitem__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__eq__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__format__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__ge__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__getitem__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__gt__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__hash__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__iter__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__le__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__len__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__lt__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__ne__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__repr__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__reversed__
      ~abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.item_class

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.clear

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.copy

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.get

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.has_key

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.items

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.keys

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.popitem

.. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.respell_division

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.setdefault

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.update

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.values

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__cmp__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__reversed__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.PartitionTable.PartitionTable.__setitem__
