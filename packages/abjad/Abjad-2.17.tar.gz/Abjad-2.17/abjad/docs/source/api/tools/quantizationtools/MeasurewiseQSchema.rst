.. currentmodule:: abjad.tools.quantizationtools

MeasurewiseQSchema
==================

.. autoclass:: MeasurewiseQSchema

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
              "abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>MeasurewiseQSchema</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QSchema.QSchema" [color=3,
                  group=2,
                  label=QSchema,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.QSchema.QSchema" -> "abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QSchema.QSchema";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.quantizationtools.QSchema`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.item_class
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.items
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.search_tree
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.target_class
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.target_item_class
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.tempo
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.time_signature
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.use_full_measure
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__call__
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__eq__
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__format__
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__getitem__
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__hash__
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__ne__
      ~abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.items

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.search_tree

.. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.target_class

.. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.target_item_class

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.tempo

.. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.time_signature

.. autoattribute:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.use_full_measure

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema.__repr__
