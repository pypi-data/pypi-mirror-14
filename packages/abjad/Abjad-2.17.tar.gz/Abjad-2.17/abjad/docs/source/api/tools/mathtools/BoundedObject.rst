.. currentmodule:: abjad.tools.mathtools

BoundedObject
=============

.. autoclass:: BoundedObject

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
          subgraph cluster_mathtools {
              graph [label=mathtools];
              "abjad.tools.mathtools.BoundedObject.BoundedObject" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>BoundedObject</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_timespantools {
              graph [label=timespantools];
              "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan" [color=4,
                  group=3,
                  label=AnnotatedTimespan,
                  shape=box];
              "abjad.tools.timespantools.Timespan.Timespan" [color=4,
                  group=3,
                  label=Timespan,
                  shape=box];
              "abjad.tools.timespantools.Timespan.Timespan" -> "abjad.tools.timespantools.AnnotatedTimespan.AnnotatedTimespan";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.mathtools.BoundedObject.BoundedObject";
          "abjad.tools.mathtools.BoundedObject.BoundedObject" -> "abjad.tools.timespantools.Timespan.Timespan";
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

      ~abjad.tools.mathtools.BoundedObject.BoundedObject.is_closed
      ~abjad.tools.mathtools.BoundedObject.BoundedObject.is_half_closed
      ~abjad.tools.mathtools.BoundedObject.BoundedObject.is_half_open
      ~abjad.tools.mathtools.BoundedObject.BoundedObject.is_left_closed
      ~abjad.tools.mathtools.BoundedObject.BoundedObject.is_left_open
      ~abjad.tools.mathtools.BoundedObject.BoundedObject.is_open
      ~abjad.tools.mathtools.BoundedObject.BoundedObject.is_right_closed
      ~abjad.tools.mathtools.BoundedObject.BoundedObject.is_right_open
      ~abjad.tools.mathtools.BoundedObject.BoundedObject.__eq__
      ~abjad.tools.mathtools.BoundedObject.BoundedObject.__format__
      ~abjad.tools.mathtools.BoundedObject.BoundedObject.__hash__
      ~abjad.tools.mathtools.BoundedObject.BoundedObject.__ne__
      ~abjad.tools.mathtools.BoundedObject.BoundedObject.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.mathtools.BoundedObject.BoundedObject.is_closed

.. autoattribute:: abjad.tools.mathtools.BoundedObject.BoundedObject.is_half_closed

.. autoattribute:: abjad.tools.mathtools.BoundedObject.BoundedObject.is_half_open

.. autoattribute:: abjad.tools.mathtools.BoundedObject.BoundedObject.is_open

Read/write properties
---------------------

.. autoattribute:: abjad.tools.mathtools.BoundedObject.BoundedObject.is_left_closed

.. autoattribute:: abjad.tools.mathtools.BoundedObject.BoundedObject.is_left_open

.. autoattribute:: abjad.tools.mathtools.BoundedObject.BoundedObject.is_right_closed

.. autoattribute:: abjad.tools.mathtools.BoundedObject.BoundedObject.is_right_open

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.BoundedObject.BoundedObject.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.BoundedObject.BoundedObject.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.BoundedObject.BoundedObject.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.BoundedObject.BoundedObject.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.mathtools.BoundedObject.BoundedObject.__repr__
