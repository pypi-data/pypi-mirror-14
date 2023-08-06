.. currentmodule:: abjad.tools.scoretools

Tuplet
======

.. autoclass:: Tuplet

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
              "abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet" [color=3,
                  group=2,
                  label=FixedDurationTuplet,
                  shape=box];
              "abjad.tools.scoretools.Tuplet.Tuplet" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Tuplet</B>>,
                  shape=box,
                  style="filled, rounded"];
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

- :py:class:`abjad.tools.scoretools.Container`

- :py:class:`abjad.tools.scoretools.Component`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.scoretools.Tuplet.Tuplet.append
      ~abjad.tools.scoretools.Tuplet.Tuplet.extend
      ~abjad.tools.scoretools.Tuplet.Tuplet.force_fraction
      ~abjad.tools.scoretools.Tuplet.Tuplet.force_times_command
      ~abjad.tools.scoretools.Tuplet.Tuplet.from_duration_and_ratio
      ~abjad.tools.scoretools.Tuplet.Tuplet.from_leaf_and_ratio
      ~abjad.tools.scoretools.Tuplet.Tuplet.from_nonreduced_ratio_and_nonreduced_fraction
      ~abjad.tools.scoretools.Tuplet.Tuplet.implied_prolation
      ~abjad.tools.scoretools.Tuplet.Tuplet.index
      ~abjad.tools.scoretools.Tuplet.Tuplet.insert
      ~abjad.tools.scoretools.Tuplet.Tuplet.is_augmentation
      ~abjad.tools.scoretools.Tuplet.Tuplet.is_diminution
      ~abjad.tools.scoretools.Tuplet.Tuplet.is_invisible
      ~abjad.tools.scoretools.Tuplet.Tuplet.is_redundant
      ~abjad.tools.scoretools.Tuplet.Tuplet.is_simultaneous
      ~abjad.tools.scoretools.Tuplet.Tuplet.is_trivial
      ~abjad.tools.scoretools.Tuplet.Tuplet.multiplied_duration
      ~abjad.tools.scoretools.Tuplet.Tuplet.multiplier
      ~abjad.tools.scoretools.Tuplet.Tuplet.name
      ~abjad.tools.scoretools.Tuplet.Tuplet.pop
      ~abjad.tools.scoretools.Tuplet.Tuplet.preferred_denominator
      ~abjad.tools.scoretools.Tuplet.Tuplet.remove
      ~abjad.tools.scoretools.Tuplet.Tuplet.reverse
      ~abjad.tools.scoretools.Tuplet.Tuplet.select_leaves
      ~abjad.tools.scoretools.Tuplet.Tuplet.set_minimum_denominator
      ~abjad.tools.scoretools.Tuplet.Tuplet.to_fixed_duration_tuplet
      ~abjad.tools.scoretools.Tuplet.Tuplet.toggle_prolation
      ~abjad.tools.scoretools.Tuplet.Tuplet.__contains__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__copy__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__delitem__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__eq__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__format__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__getitem__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__graph__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__hash__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__illustrate__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__iter__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__len__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__mul__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__ne__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__repr__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__rmul__
      ~abjad.tools.scoretools.Tuplet.Tuplet.__setitem__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.scoretools.Tuplet.Tuplet.implied_prolation

.. autoattribute:: abjad.tools.scoretools.Tuplet.Tuplet.is_augmentation

.. autoattribute:: abjad.tools.scoretools.Tuplet.Tuplet.is_diminution

.. autoattribute:: abjad.tools.scoretools.Tuplet.Tuplet.is_redundant

.. autoattribute:: abjad.tools.scoretools.Tuplet.Tuplet.is_trivial

.. autoattribute:: abjad.tools.scoretools.Tuplet.Tuplet.multiplied_duration

Read/write properties
---------------------

.. autoattribute:: abjad.tools.scoretools.Tuplet.Tuplet.force_fraction

.. autoattribute:: abjad.tools.scoretools.Tuplet.Tuplet.force_times_command

.. autoattribute:: abjad.tools.scoretools.Tuplet.Tuplet.is_invisible

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Tuplet.Tuplet.is_simultaneous

.. autoattribute:: abjad.tools.scoretools.Tuplet.Tuplet.multiplier

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Tuplet.Tuplet.name

.. autoattribute:: abjad.tools.scoretools.Tuplet.Tuplet.preferred_denominator

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.select_leaves

.. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.set_minimum_denominator

.. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.to_fixed_duration_tuplet

.. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.toggle_prolation

Class & static methods
----------------------

.. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.from_duration_and_ratio

.. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.from_leaf_and_ratio

.. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.from_nonreduced_ratio_and_nonreduced_fraction

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__ne__

.. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Tuplet.Tuplet.__setitem__
