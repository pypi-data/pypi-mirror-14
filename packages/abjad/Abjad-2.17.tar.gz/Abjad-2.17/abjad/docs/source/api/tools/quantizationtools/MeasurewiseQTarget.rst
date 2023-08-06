.. currentmodule:: abjad.tools.quantizationtools

MeasurewiseQTarget
==================

.. autoclass:: MeasurewiseQTarget

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
              "abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>MeasurewiseQTarget</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QTarget.QTarget" [color=3,
                  group=2,
                  label=QTarget,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.QTarget.QTarget" -> "abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QTarget.QTarget";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.quantizationtools.QTarget`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.beats
      ~abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.duration_in_ms
      ~abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.item_class
      ~abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.items
      ~abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.__call__
      ~abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.__eq__
      ~abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.__format__
      ~abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.__hash__
      ~abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.__ne__
      ~abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.beats

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.duration_in_ms

.. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.items

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQTarget.MeasurewiseQTarget.__repr__
