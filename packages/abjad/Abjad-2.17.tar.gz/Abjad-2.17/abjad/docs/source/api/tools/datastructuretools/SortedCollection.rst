.. currentmodule:: abjad.tools.datastructuretools

SortedCollection
================

.. autoclass:: SortedCollection

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
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.SortedCollection.SortedCollection" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>SortedCollection</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
          }
          "builtins.object" -> "abjad.tools.datastructuretools.SortedCollection.SortedCollection";
      }

Bases
-----

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.clear
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.copy
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.count
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.find
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.find_ge
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.find_gt
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.find_le
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.find_lt
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.index
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.insert
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.insert_right
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.key
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.remove
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.__contains__
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.__getitem__
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.__iter__
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.__len__
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.__repr__
      ~abjad.tools.datastructuretools.SortedCollection.SortedCollection.__reversed__

Read/write properties
---------------------

.. autoattribute:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.key

Methods
-------

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.clear

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.copy

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.count

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.find

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.find_ge

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.find_gt

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.find_le

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.find_lt

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.index

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.insert

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.insert_right

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.remove

Special methods
---------------

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.__contains__

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.__getitem__

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.__iter__

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.__len__

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.__repr__

.. automethod:: abjad.tools.datastructuretools.SortedCollection.SortedCollection.__reversed__
