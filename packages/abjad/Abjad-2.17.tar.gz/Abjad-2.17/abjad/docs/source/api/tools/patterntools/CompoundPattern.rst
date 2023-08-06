.. currentmodule:: abjad.tools.patterntools

CompoundPattern
===============

.. autoclass:: CompoundPattern

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
              "abjad.tools.patterntools.CompoundPattern.CompoundPattern" [color=black,
                  fontcolor=white,
                  group=3,
                  label=<<B>CompoundPattern</B>>,
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
          "abjad.tools.datastructuretools.TypedTuple.TypedTuple" -> "abjad.tools.patterntools.CompoundPattern.CompoundPattern";
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

      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.count
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.get_boolean_vector
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.index
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.inverted
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.item_class
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.items
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.matches_index
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.operator
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.period
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.reverse
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.rotate
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__add__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__and__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__contains__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__eq__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__format__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__getitem__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__getslice__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__hash__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__invert__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__iter__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__len__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__mul__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__ne__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__or__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__radd__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__repr__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__rmul__
      ~abjad.tools.patterntools.CompoundPattern.CompoundPattern.__xor__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.inverted

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.items

.. autoattribute:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.operator

.. autoattribute:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.period

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.count

.. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.get_boolean_vector

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.index

.. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.matches_index

.. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.reverse

.. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.rotate

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__add__

.. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__and__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__getslice__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__hash__

.. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__invert__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__ne__

.. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__or__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__radd__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__rmul__

.. automethod:: abjad.tools.patterntools.CompoundPattern.CompoundPattern.__xor__
