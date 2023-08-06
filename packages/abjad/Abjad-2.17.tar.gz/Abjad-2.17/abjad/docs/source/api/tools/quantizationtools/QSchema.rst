.. currentmodule:: abjad.tools.quantizationtools

QSchema
=======

.. autoclass:: QSchema

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
              "abjad.tools.quantizationtools.BeatwiseQSchema.BeatwiseQSchema" [color=3,
                  group=2,
                  label=BeatwiseQSchema,
                  shape=box];
              "abjad.tools.quantizationtools.MeasurewiseQSchema.MeasurewiseQSchema" [color=3,
                  group=2,
                  label=MeasurewiseQSchema,
                  shape=box];
              "abjad.tools.quantizationtools.QSchema.QSchema" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>QSchema</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QSchema.QSchema" -> "abjad.tools.quantizationtools.BeatwiseQSchema.BeatwiseQSchema";
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

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.quantizationtools.QSchema.QSchema.item_class
      ~abjad.tools.quantizationtools.QSchema.QSchema.items
      ~abjad.tools.quantizationtools.QSchema.QSchema.search_tree
      ~abjad.tools.quantizationtools.QSchema.QSchema.target_class
      ~abjad.tools.quantizationtools.QSchema.QSchema.target_item_class
      ~abjad.tools.quantizationtools.QSchema.QSchema.tempo
      ~abjad.tools.quantizationtools.QSchema.QSchema.__call__
      ~abjad.tools.quantizationtools.QSchema.QSchema.__eq__
      ~abjad.tools.quantizationtools.QSchema.QSchema.__format__
      ~abjad.tools.quantizationtools.QSchema.QSchema.__getitem__
      ~abjad.tools.quantizationtools.QSchema.QSchema.__hash__
      ~abjad.tools.quantizationtools.QSchema.QSchema.__ne__
      ~abjad.tools.quantizationtools.QSchema.QSchema.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.quantizationtools.QSchema.QSchema.item_class

.. autoattribute:: abjad.tools.quantizationtools.QSchema.QSchema.items

.. autoattribute:: abjad.tools.quantizationtools.QSchema.QSchema.search_tree

.. autoattribute:: abjad.tools.quantizationtools.QSchema.QSchema.target_class

.. autoattribute:: abjad.tools.quantizationtools.QSchema.QSchema.target_item_class

.. autoattribute:: abjad.tools.quantizationtools.QSchema.QSchema.tempo

Special methods
---------------

.. automethod:: abjad.tools.quantizationtools.QSchema.QSchema.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QSchema.QSchema.__eq__

.. automethod:: abjad.tools.quantizationtools.QSchema.QSchema.__format__

.. automethod:: abjad.tools.quantizationtools.QSchema.QSchema.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QSchema.QSchema.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QSchema.QSchema.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QSchema.QSchema.__repr__
