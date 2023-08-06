.. currentmodule:: abjad.tools.sequencetools

Sequence
========

.. autoclass:: Sequence

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
          subgraph cluster_sequencetools {
              graph [label=sequencetools];
              "abjad.tools.sequencetools.Sequence.Sequence" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Sequence</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.sequencetools.Sequence.Sequence";
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

      ~abjad.tools.sequencetools.Sequence.Sequence.degree_of_rotational_symmetry
      ~abjad.tools.sequencetools.Sequence.Sequence.flatten
      ~abjad.tools.sequencetools.Sequence.Sequence.is_decreasing
      ~abjad.tools.sequencetools.Sequence.Sequence.is_increasing
      ~abjad.tools.sequencetools.Sequence.Sequence.is_permutation
      ~abjad.tools.sequencetools.Sequence.Sequence.is_repetition_free
      ~abjad.tools.sequencetools.Sequence.Sequence.is_restricted_growth_function
      ~abjad.tools.sequencetools.Sequence.Sequence.items
      ~abjad.tools.sequencetools.Sequence.Sequence.partition_by_counts
      ~abjad.tools.sequencetools.Sequence.Sequence.partition_by_ratio_of_lengths
      ~abjad.tools.sequencetools.Sequence.Sequence.period_of_rotation
      ~abjad.tools.sequencetools.Sequence.Sequence.reverse
      ~abjad.tools.sequencetools.Sequence.Sequence.rotate
      ~abjad.tools.sequencetools.Sequence.Sequence.split
      ~abjad.tools.sequencetools.Sequence.Sequence.sum
      ~abjad.tools.sequencetools.Sequence.Sequence.__add__
      ~abjad.tools.sequencetools.Sequence.Sequence.__eq__
      ~abjad.tools.sequencetools.Sequence.Sequence.__format__
      ~abjad.tools.sequencetools.Sequence.Sequence.__getitem__
      ~abjad.tools.sequencetools.Sequence.Sequence.__hash__
      ~abjad.tools.sequencetools.Sequence.Sequence.__len__
      ~abjad.tools.sequencetools.Sequence.Sequence.__ne__
      ~abjad.tools.sequencetools.Sequence.Sequence.__radd__
      ~abjad.tools.sequencetools.Sequence.Sequence.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.sequencetools.Sequence.Sequence.degree_of_rotational_symmetry

.. autoattribute:: abjad.tools.sequencetools.Sequence.Sequence.items

.. autoattribute:: abjad.tools.sequencetools.Sequence.Sequence.period_of_rotation

Methods
-------

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.flatten

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.is_decreasing

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.is_increasing

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.is_permutation

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.is_repetition_free

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.is_restricted_growth_function

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.partition_by_counts

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.partition_by_ratio_of_lengths

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.reverse

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.rotate

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.split

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.sum

Special methods
---------------

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.__add__

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.__eq__

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.__format__

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.__getitem__

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.__hash__

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.__len__

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.__ne__

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.__radd__

.. automethod:: abjad.tools.sequencetools.Sequence.Sequence.__repr__
