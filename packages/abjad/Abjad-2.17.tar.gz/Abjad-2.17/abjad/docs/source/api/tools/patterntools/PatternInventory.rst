.. currentmodule:: abjad.tools.patterntools

PatternInventory
================

.. autoclass:: PatternInventory

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
              "abjad.tools.datastructuretools.TypedTuple.TypedTuple" [color=3,
                  group=2,
                  label=TypedTuple,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedTuple.TypedTuple";
          }
          subgraph cluster_patterntools {
              graph [label=patterntools];
              "abjad.tools.patterntools.PatternInventory.PatternInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>PatternInventory</B>>,
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
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.patterntools.PatternInventory.PatternInventory";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.datastructuretools.TypedTuple`

- :py:class:`abjad.tools.datastructuretools.TypedCollection`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.patterntools.PatternInventory.PatternInventory.count
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.get_matching_pattern
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.get_matching_payload
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.index
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.item_class
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.items
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__add__
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__contains__
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__eq__
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__format__
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__getitem__
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__getslice__
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__hash__
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__iter__
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__len__
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__mul__
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__ne__
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__radd__
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__repr__
      ~abjad.tools.patterntools.PatternInventory.PatternInventory.__rmul__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.patterntools.PatternInventory.PatternInventory.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.patterntools.PatternInventory.PatternInventory.items

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.count

.. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.get_matching_pattern

.. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.get_matching_payload

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.index

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__getslice__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.PatternInventory.PatternInventory.__rmul__
