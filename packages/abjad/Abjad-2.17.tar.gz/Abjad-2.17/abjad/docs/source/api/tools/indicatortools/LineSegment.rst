.. currentmodule:: abjad.tools.indicatortools

LineSegment
===========

.. autoclass:: LineSegment

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
              "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" [color=1,
                  group=0,
                  label=AbjadValueObject,
                  shape=box];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.AbjadValueObject.AbjadValueObject";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.Arrow.Arrow" [color=3,
                  group=2,
                  label=Arrow,
                  shape=box];
              "abjad.tools.indicatortools.LineSegment.LineSegment" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LineSegment</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.indicatortools.LineSegment.LineSegment" -> "abjad.tools.indicatortools.Arrow.Arrow";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.LineSegment.LineSegment";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.indicatortools.LineSegment.LineSegment.arrow_width
      ~abjad.tools.indicatortools.LineSegment.LineSegment.dash_fraction
      ~abjad.tools.indicatortools.LineSegment.LineSegment.dash_period
      ~abjad.tools.indicatortools.LineSegment.LineSegment.default_scope
      ~abjad.tools.indicatortools.LineSegment.LineSegment.left_broken_padding
      ~abjad.tools.indicatortools.LineSegment.LineSegment.left_broken_text
      ~abjad.tools.indicatortools.LineSegment.LineSegment.left_hspace
      ~abjad.tools.indicatortools.LineSegment.LineSegment.left_padding
      ~abjad.tools.indicatortools.LineSegment.LineSegment.left_stencil_align_direction_y
      ~abjad.tools.indicatortools.LineSegment.LineSegment.right_arrow
      ~abjad.tools.indicatortools.LineSegment.LineSegment.right_broken_arrow
      ~abjad.tools.indicatortools.LineSegment.LineSegment.right_broken_padding
      ~abjad.tools.indicatortools.LineSegment.LineSegment.right_padding
      ~abjad.tools.indicatortools.LineSegment.LineSegment.right_stencil_align_direction_y
      ~abjad.tools.indicatortools.LineSegment.LineSegment.style
      ~abjad.tools.indicatortools.LineSegment.LineSegment.__copy__
      ~abjad.tools.indicatortools.LineSegment.LineSegment.__eq__
      ~abjad.tools.indicatortools.LineSegment.LineSegment.__format__
      ~abjad.tools.indicatortools.LineSegment.LineSegment.__hash__
      ~abjad.tools.indicatortools.LineSegment.LineSegment.__ne__
      ~abjad.tools.indicatortools.LineSegment.LineSegment.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.arrow_width

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.dash_fraction

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.dash_period

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.default_scope

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.left_broken_padding

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.left_broken_text

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.left_hspace

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.left_padding

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.left_stencil_align_direction_y

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.right_arrow

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.right_broken_arrow

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.right_broken_padding

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.right_padding

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.right_stencil_align_direction_y

.. autoattribute:: abjad.tools.indicatortools.LineSegment.LineSegment.style

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.LineSegment.LineSegment.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.LineSegment.LineSegment.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.LineSegment.LineSegment.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.LineSegment.LineSegment.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.LineSegment.LineSegment.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.LineSegment.LineSegment.__repr__
