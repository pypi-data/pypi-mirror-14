.. currentmodule:: abjad.tools.quantizationtools

QEventSequence
==============

.. autoclass:: QEventSequence

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
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.QEventSequence.QEventSequence" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>QEventSequence</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QEventSequence.QEventSequence";
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

      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.duration_in_ms
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.from_millisecond_durations
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.from_millisecond_offsets
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.from_millisecond_pitch_pairs
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.from_tempo_scaled_durations
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.from_tempo_scaled_leaves
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.sequence
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.__contains__
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.__eq__
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.__format__
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.__getitem__
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.__hash__
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.__iter__
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.__len__
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.__ne__
      ~abjad.tools.quantizationtools.QEventSequence.QEventSequence.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.duration_in_ms

.. autoattribute:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.sequence

Class & static methods
----------------------

.. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.from_millisecond_durations

.. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.from_millisecond_offsets

.. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.from_millisecond_pitch_pairs

.. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.from_tempo_scaled_durations

.. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.from_tempo_scaled_leaves

Special methods
---------------

.. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.__contains__

.. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.__eq__

.. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.__format__

.. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.__getitem__

.. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.__hash__

.. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.__iter__

.. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QEventSequence.QEventSequence.__repr__
