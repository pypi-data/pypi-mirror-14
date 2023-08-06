.. currentmodule:: abjad.tools.scoretools

FixedDurationContainer
======================

.. autoclass:: FixedDurationContainer

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
              "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>FixedDurationContainer</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Measure.Measure" [color=3,
                  group=2,
                  label=Measure,
                  shape=box];
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

- :py:class:`abjad.tools.scoretools.Container`

- :py:class:`abjad.tools.scoretools.Component`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.append
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.extend
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.index
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.insert
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.is_full
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.is_misfilled
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.is_overfull
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.is_simultaneous
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.is_underfull
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.name
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.pop
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.remove
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.reverse
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.select_leaves
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.target_duration
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__contains__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__copy__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__delitem__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__eq__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__format__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__getitem__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__graph__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__hash__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__illustrate__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__iter__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__len__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__mul__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__ne__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__repr__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__rmul__
      ~abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__setitem__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.is_full

.. autoattribute:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.is_misfilled

.. autoattribute:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.is_overfull

.. autoattribute:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.is_underfull

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.is_simultaneous

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.name

.. autoattribute:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.target_duration

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.append

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.extend

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.index

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.insert

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.pop

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.remove

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.reverse

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.select_leaves

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__iter__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__ne__

.. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer.__setitem__
