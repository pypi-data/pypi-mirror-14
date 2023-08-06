.. currentmodule:: abjad.tools.scoretools

FixedDurationTuplet
===================

.. autoclass:: FixedDurationTuplet

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
              "abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>FixedDurationTuplet</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Tuplet.Tuplet" [color=3,
                  group=2,
                  label=Tuplet,
                  shape=box];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Tuplet.Tuplet";
              "abjad.tools.scoretools.Tuplet.Tuplet" -> "abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet";
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

- :py:class:`abjad.tools.scoretools.Tuplet`

- :py:class:`abjad.tools.scoretools.Container`

- :py:class:`abjad.tools.scoretools.Component`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.append
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.extend
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.force_fraction
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.force_times_command
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.from_duration_and_ratio
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.from_leaf_and_ratio
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.from_nonreduced_ratio_and_nonreduced_fraction
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.implied_prolation
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.index
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.insert
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.is_augmentation
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.is_diminution
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.is_invisible
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.is_redundant
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.is_simultaneous
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.is_trivial
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.multiplied_duration
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.multiplier
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.name
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.pop
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.preferred_denominator
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.remove
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.reverse
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.select_leaves
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.set_minimum_denominator
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.target_duration
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.to_fixed_duration_tuplet
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.to_fixed_multiplier
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.toggle_prolation
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.trim
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__contains__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__copy__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__delitem__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__eq__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__format__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__getitem__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__graph__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__hash__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__illustrate__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__iter__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__len__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__mul__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__ne__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__repr__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__rmul__
      ~abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__setitem__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.implied_prolation

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.is_augmentation

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.is_diminution

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.is_redundant

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.is_trivial

.. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.multiplied_duration

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.force_fraction

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.force_times_command

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.is_invisible

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.is_simultaneous

.. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.multiplier

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.name

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.preferred_denominator

.. autoattribute:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.target_duration

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.select_leaves

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.set_minimum_denominator

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.to_fixed_duration_tuplet

.. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.to_fixed_multiplier

.. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.toggle_prolation

.. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.trim

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.from_duration_and_ratio

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.from_leaf_and_ratio

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.from_nonreduced_ratio_and_nonreduced_fraction

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__ne__

.. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet.__setitem__
