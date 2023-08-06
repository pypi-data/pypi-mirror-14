.. currentmodule:: abjad.tools.metertools

Meter
=====

.. autoclass:: Meter

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
          subgraph cluster_metertools {
              graph [label=metertools];
              "abjad.tools.metertools.Meter.Meter" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Meter</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.metertools.Meter.Meter";
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

      ~abjad.tools.metertools.Meter.Meter.decrease_durations_monotonically
      ~abjad.tools.metertools.Meter.Meter.denominator
      ~abjad.tools.metertools.Meter.Meter.depthwise_offset_inventory
      ~abjad.tools.metertools.Meter.Meter.duration
      ~abjad.tools.metertools.Meter.Meter.fit_meters_to_expr
      ~abjad.tools.metertools.Meter.Meter.generate_offset_kernel_to_denominator
      ~abjad.tools.metertools.Meter.Meter.implied_time_signature
      ~abjad.tools.metertools.Meter.Meter.is_compound
      ~abjad.tools.metertools.Meter.Meter.is_simple
      ~abjad.tools.metertools.Meter.Meter.numerator
      ~abjad.tools.metertools.Meter.Meter.pair
      ~abjad.tools.metertools.Meter.Meter.preferred_boundary_depth
      ~abjad.tools.metertools.Meter.Meter.pretty_rtm_format
      ~abjad.tools.metertools.Meter.Meter.root_node
      ~abjad.tools.metertools.Meter.Meter.rtm_format
      ~abjad.tools.metertools.Meter.Meter.__eq__
      ~abjad.tools.metertools.Meter.Meter.__format__
      ~abjad.tools.metertools.Meter.Meter.__graph__
      ~abjad.tools.metertools.Meter.Meter.__hash__
      ~abjad.tools.metertools.Meter.Meter.__iter__
      ~abjad.tools.metertools.Meter.Meter.__ne__
      ~abjad.tools.metertools.Meter.Meter.__repr__
      ~abjad.tools.metertools.Meter.Meter.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.metertools.Meter.Meter.decrease_durations_monotonically

.. autoattribute:: abjad.tools.metertools.Meter.Meter.denominator

.. autoattribute:: abjad.tools.metertools.Meter.Meter.depthwise_offset_inventory

.. autoattribute:: abjad.tools.metertools.Meter.Meter.duration

.. autoattribute:: abjad.tools.metertools.Meter.Meter.implied_time_signature

.. autoattribute:: abjad.tools.metertools.Meter.Meter.is_compound

.. autoattribute:: abjad.tools.metertools.Meter.Meter.is_simple

.. autoattribute:: abjad.tools.metertools.Meter.Meter.numerator

.. autoattribute:: abjad.tools.metertools.Meter.Meter.pair

.. autoattribute:: abjad.tools.metertools.Meter.Meter.preferred_boundary_depth

.. autoattribute:: abjad.tools.metertools.Meter.Meter.pretty_rtm_format

.. autoattribute:: abjad.tools.metertools.Meter.Meter.root_node

.. autoattribute:: abjad.tools.metertools.Meter.Meter.rtm_format

Methods
-------

.. automethod:: abjad.tools.metertools.Meter.Meter.generate_offset_kernel_to_denominator

Class & static methods
----------------------

.. automethod:: abjad.tools.metertools.Meter.Meter.fit_meters_to_expr

Special methods
---------------

.. automethod:: abjad.tools.metertools.Meter.Meter.__eq__

.. automethod:: abjad.tools.metertools.Meter.Meter.__format__

.. automethod:: abjad.tools.metertools.Meter.Meter.__graph__

.. automethod:: abjad.tools.metertools.Meter.Meter.__hash__

.. automethod:: abjad.tools.metertools.Meter.Meter.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.Meter.Meter.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.metertools.Meter.Meter.__repr__

.. automethod:: abjad.tools.metertools.Meter.Meter.__str__
