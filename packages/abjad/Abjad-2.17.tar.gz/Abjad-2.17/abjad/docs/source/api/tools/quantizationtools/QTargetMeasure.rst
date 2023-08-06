.. currentmodule:: abjad.tools.quantizationtools

QTargetMeasure
==============

.. autoclass:: QTargetMeasure

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
              "abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>QTargetMeasure</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure";
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

      ~abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.beats
      ~abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.duration_in_ms
      ~abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.offset_in_ms
      ~abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.search_tree
      ~abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.tempo
      ~abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.time_signature
      ~abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.use_full_measure
      ~abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.__eq__
      ~abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.__format__
      ~abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.__hash__
      ~abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.__ne__
      ~abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.beats

.. autoattribute:: abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.duration_in_ms

.. autoattribute:: abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.offset_in_ms

.. autoattribute:: abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.search_tree

.. autoattribute:: abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.tempo

.. autoattribute:: abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.time_signature

.. autoattribute:: abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.use_full_measure

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.__eq__

.. automethod:: abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QTargetMeasure.QTargetMeasure.__repr__
