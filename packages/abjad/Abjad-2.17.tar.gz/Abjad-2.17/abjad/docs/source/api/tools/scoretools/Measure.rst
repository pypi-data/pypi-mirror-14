.. currentmodule:: abjad.tools.scoretools

Measure
=======

.. autoclass:: Measure

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
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.Component.Component" [color=3,
                  group=2,
                  label=Component,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.Container.Container" [color=3,
                  group=2,
                  label=Container,
                  shape=box];
              "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer" [color=3,
                  group=2,
                  label=FixedDurationContainer,
                  shape=box];
              "abjad.tools.scoretools.Measure.Measure" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Measure</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer";
              "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer" -> "abjad.tools.scoretools.Measure.Measure";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.Component.Component";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.scoretools.FixedDurationContainer`

- :py:class:`abjad.tools.scoretools.Container`

- :py:class:`abjad.tools.scoretools.Component`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.scoretools.Measure.Measure.always_format_time_signature
      ~abjad.tools.scoretools.Measure.Measure.append
      ~abjad.tools.scoretools.Measure.Measure.automatically_adjust_time_signature
      ~abjad.tools.scoretools.Measure.Measure.extend
      ~abjad.tools.scoretools.Measure.Measure.from_selections
      ~abjad.tools.scoretools.Measure.Measure.has_non_power_of_two_denominator
      ~abjad.tools.scoretools.Measure.Measure.has_power_of_two_denominator
      ~abjad.tools.scoretools.Measure.Measure.implicit_scaling
      ~abjad.tools.scoretools.Measure.Measure.implied_prolation
      ~abjad.tools.scoretools.Measure.Measure.index
      ~abjad.tools.scoretools.Measure.Measure.insert
      ~abjad.tools.scoretools.Measure.Measure.is_full
      ~abjad.tools.scoretools.Measure.Measure.is_misfilled
      ~abjad.tools.scoretools.Measure.Measure.is_overfull
      ~abjad.tools.scoretools.Measure.Measure.is_simultaneous
      ~abjad.tools.scoretools.Measure.Measure.is_underfull
      ~abjad.tools.scoretools.Measure.Measure.measure_number
      ~abjad.tools.scoretools.Measure.Measure.name
      ~abjad.tools.scoretools.Measure.Measure.pop
      ~abjad.tools.scoretools.Measure.Measure.remove
      ~abjad.tools.scoretools.Measure.Measure.reverse
      ~abjad.tools.scoretools.Measure.Measure.scale_and_adjust_time_signature
      ~abjad.tools.scoretools.Measure.Measure.select_leaves
      ~abjad.tools.scoretools.Measure.Measure.target_duration
      ~abjad.tools.scoretools.Measure.Measure.time_signature
      ~abjad.tools.scoretools.Measure.Measure.__contains__
      ~abjad.tools.scoretools.Measure.Measure.__copy__
      ~abjad.tools.scoretools.Measure.Measure.__delitem__
      ~abjad.tools.scoretools.Measure.Measure.__eq__
      ~abjad.tools.scoretools.Measure.Measure.__format__
      ~abjad.tools.scoretools.Measure.Measure.__getitem__
      ~abjad.tools.scoretools.Measure.Measure.__graph__
      ~abjad.tools.scoretools.Measure.Measure.__hash__
      ~abjad.tools.scoretools.Measure.Measure.__illustrate__
      ~abjad.tools.scoretools.Measure.Measure.__iter__
      ~abjad.tools.scoretools.Measure.Measure.__len__
      ~abjad.tools.scoretools.Measure.Measure.__mul__
      ~abjad.tools.scoretools.Measure.Measure.__ne__
      ~abjad.tools.scoretools.Measure.Measure.__repr__
      ~abjad.tools.scoretools.Measure.Measure.__rmul__
      ~abjad.tools.scoretools.Measure.Measure.__setitem__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.scoretools.Measure.Measure.has_non_power_of_two_denominator

.. autoattribute:: abjad.tools.scoretools.Measure.Measure.has_power_of_two_denominator

.. autoattribute:: abjad.tools.scoretools.Measure.Measure.implied_prolation

.. autoattribute:: abjad.tools.scoretools.Measure.Measure.is_full

.. autoattribute:: abjad.tools.scoretools.Measure.Measure.is_misfilled

.. autoattribute:: abjad.tools.scoretools.Measure.Measure.is_overfull

.. autoattribute:: abjad.tools.scoretools.Measure.Measure.is_underfull

.. autoattribute:: abjad.tools.scoretools.Measure.Measure.measure_number

.. autoattribute:: abjad.tools.scoretools.Measure.Measure.target_duration

.. autoattribute:: abjad.tools.scoretools.Measure.Measure.time_signature

Read/write properties
---------------------

.. autoattribute:: abjad.tools.scoretools.Measure.Measure.always_format_time_signature

.. autoattribute:: abjad.tools.scoretools.Measure.Measure.automatically_adjust_time_signature

.. autoattribute:: abjad.tools.scoretools.Measure.Measure.implicit_scaling

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Measure.Measure.is_simultaneous

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Measure.Measure.name

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.reverse

.. automethod:: abjad.tools.scoretools.Measure.Measure.scale_and_adjust_time_signature

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.select_leaves

Class & static methods
----------------------

.. automethod:: abjad.tools.scoretools.Measure.Measure.from_selections

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.__copy__

.. automethod:: abjad.tools.scoretools.Measure.Measure.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.__ne__

.. automethod:: abjad.tools.scoretools.Measure.Measure.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Measure.Measure.__rmul__

.. automethod:: abjad.tools.scoretools.Measure.Measure.__setitem__
