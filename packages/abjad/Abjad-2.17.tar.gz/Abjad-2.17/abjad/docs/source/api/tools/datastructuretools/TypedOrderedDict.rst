.. currentmodule:: abjad.tools.datastructuretools

TypedOrderedDict
================

.. autoclass:: TypedOrderedDict

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
              "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TypedOrderedDict</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict";
          }
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.PartitionTable.PartitionTable" [color=4,
                  group=3,
                  label=PartitionTable,
                  shape=box];
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

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.clear
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.copy
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.get
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.has_key
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.item_class
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.items
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.keys
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.pop
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.popitem
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.setdefault
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.update
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.values
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__cmp__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__contains__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__delitem__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__eq__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__format__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__ge__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__getitem__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__gt__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__hash__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__iter__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__le__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__len__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__lt__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__ne__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__repr__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__reversed__
      ~abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.item_class

Methods
-------

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.clear

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.copy

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.get

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.has_key

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.items

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.keys

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.pop

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.popitem

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.setdefault

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.update

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.values

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__cmp__

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__contains__

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__format__

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__ge__

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__getitem__

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__iter__

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__len__

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__lt__

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__repr__

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__reversed__

.. automethod:: abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict.__setitem__
