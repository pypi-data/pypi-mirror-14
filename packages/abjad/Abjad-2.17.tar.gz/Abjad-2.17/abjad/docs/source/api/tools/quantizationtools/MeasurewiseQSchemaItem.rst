.. currentmodule:: abjad.tools.quantizationtools

MeasurewiseQSchemaItem
======================

.. autoclass:: MeasurewiseQSchemaItem

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
              "abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>MeasurewiseQSchemaItem</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QSchemaItem.QSchemaItem" [color=3,
                  group=2,
                  label=QSchemaItem,
                  shape=oval,
                  style=bold];
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

- :py:class:`abjad.tools.quantizationtools.QSchemaItem`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.beatspan
      ~abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.search_tree
      ~abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.tempo
      ~abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.time_signature
      ~abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.use_full_measure
      ~abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.__eq__
      ~abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.__format__
      ~abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.__hash__
      ~abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.__ne__
      ~abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.beatspan

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.search_tree

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.tempo

.. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.time_signature

.. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.use_full_measure

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQSchemaItem.MeasurewiseQSchemaItem.__repr__
