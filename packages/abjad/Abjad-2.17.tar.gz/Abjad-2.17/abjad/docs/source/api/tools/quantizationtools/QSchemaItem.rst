.. currentmodule:: abjad.tools.quantizationtools

QSchemaItem
===========

.. autoclass:: QSchemaItem

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
              "abjad.tools.quantizationtools.BeatwiseQSchemaItem.BeatwiseQSchemaItem" [color=3,
                  group=2,
                  label=BeatwiseQSchemaItem,
                  shape=box];
              "abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem" [color=3,
                  group=2,
                  label=MeasurewiseQSchemaItem,
                  shape=box];
              "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>QSchemaItem</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem" -> "abjad.tools.quantizationtools.BeatwiseQSchemaItem.BeatwiseQSchemaItem";
              "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem" -> "abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem";
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

      ~abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.search_tree
      ~abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.tempo
      ~abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.__eq__
      ~abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.__format__
      ~abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.__hash__
      ~abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.__ne__
      ~abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.search_tree

.. autoattribute:: abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.tempo

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.__eq__

.. automethod:: abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QSchemaItem.QSchemaItem.__repr__
