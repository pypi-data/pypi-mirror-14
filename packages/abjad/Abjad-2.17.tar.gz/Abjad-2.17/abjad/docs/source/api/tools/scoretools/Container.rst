.. currentmodule:: abjad.tools.scoretools

Container
=========

.. autoclass:: Container

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
              "abjad.tools.scoretools.Cluster.Cluster" [color=3,
                  group=2,
                  label=Cluster,
                  shape=box];
              "abjad.tools.scoretools.Component.Component" [color=3,
                  group=2,
                  label=Component,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.Container.Container" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Container</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Context.Context" [color=3,
                  group=2,
                  label=Context,
                  shape=box];
              "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer" [color=3,
                  group=2,
                  label=FixedDurationContainer,
                  shape=box];
              "abjad.tools.scoretools.FixedDurationTuplet.FixedDurationTuplet" [color=3,
                  group=2,
                  label=FixedDurationTuplet,
                  shape=box];
              "abjad.tools.scoretools.GraceContainer.GraceContainer" [color=3,
                  group=2,
                  label=GraceContainer,
                  shape=box];
              "abjad.tools.scoretools.Measure.Measure" [color=3,
                  group=2,
                  label=Measure,
                  shape=box];
              "abjad.tools.scoretools.Score.Score" [color=3,
                  group=2,
                  label=Score,
                  shape=box];
              "abjad.tools.scoretools.Staff.Staff" [color=3,
                  group=2,
                  label=Staff,
                  shape=box];
              "abjad.tools.scoretools.StaffGroup.StaffGroup" [color=3,
                  group=2,
                  label=StaffGroup,
                  shape=box];
              "abjad.tools.scoretools.Tuplet.Tuplet" [color=3,
                  group=2,
                  label=Tuplet,
                  shape=box];
              "abjad.tools.scoretools.Voice.Voice" [color=3,
                  group=2,
                  label=Voice,
                  shape=box];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Container.Container";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Cluster.Cluster";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Context.Context";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.GraceContainer.GraceContainer";
              "abjad.tools.scoretools.Container.Container" -> "abjad.tools.scoretools.Tuplet.Tuplet";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Score.Score";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Staff.Staff";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.StaffGroup.StaffGroup";
              "abjad.tools.scoretools.Context.Context" -> "abjad.tools.scoretools.Voice.Voice";
              "abjad.tools.scoretools.FixedDurationContainer.FixedDurationContainer" -> "abjad.tools.scoretools.Measure.Measure";
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

- :py:class:`abjad.tools.scoretools.Component`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.scoretools.Container.Container.append
      ~abjad.tools.scoretools.Container.Container.extend
      ~abjad.tools.scoretools.Container.Container.index
      ~abjad.tools.scoretools.Container.Container.insert
      ~abjad.tools.scoretools.Container.Container.is_simultaneous
      ~abjad.tools.scoretools.Container.Container.name
      ~abjad.tools.scoretools.Container.Container.pop
      ~abjad.tools.scoretools.Container.Container.remove
      ~abjad.tools.scoretools.Container.Container.reverse
      ~abjad.tools.scoretools.Container.Container.select_leaves
      ~abjad.tools.scoretools.Container.Container.__contains__
      ~abjad.tools.scoretools.Container.Container.__copy__
      ~abjad.tools.scoretools.Container.Container.__delitem__
      ~abjad.tools.scoretools.Container.Container.__eq__
      ~abjad.tools.scoretools.Container.Container.__format__
      ~abjad.tools.scoretools.Container.Container.__getitem__
      ~abjad.tools.scoretools.Container.Container.__graph__
      ~abjad.tools.scoretools.Container.Container.__hash__
      ~abjad.tools.scoretools.Container.Container.__illustrate__
      ~abjad.tools.scoretools.Container.Container.__iter__
      ~abjad.tools.scoretools.Container.Container.__len__
      ~abjad.tools.scoretools.Container.Container.__mul__
      ~abjad.tools.scoretools.Container.Container.__ne__
      ~abjad.tools.scoretools.Container.Container.__repr__
      ~abjad.tools.scoretools.Container.Container.__rmul__
      ~abjad.tools.scoretools.Container.Container.__setitem__

Read/write properties
---------------------

.. autoattribute:: abjad.tools.scoretools.Container.Container.is_simultaneous

.. autoattribute:: abjad.tools.scoretools.Container.Container.name

Methods
-------

.. automethod:: abjad.tools.scoretools.Container.Container.append

.. automethod:: abjad.tools.scoretools.Container.Container.extend

.. automethod:: abjad.tools.scoretools.Container.Container.index

.. automethod:: abjad.tools.scoretools.Container.Container.insert

.. automethod:: abjad.tools.scoretools.Container.Container.pop

.. automethod:: abjad.tools.scoretools.Container.Container.remove

.. automethod:: abjad.tools.scoretools.Container.Container.reverse

.. automethod:: abjad.tools.scoretools.Container.Container.select_leaves

Special methods
---------------

.. automethod:: abjad.tools.scoretools.Container.Container.__contains__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Container.Container.__copy__

.. automethod:: abjad.tools.scoretools.Container.Container.__delitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Container.Container.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Container.Container.__format__

.. automethod:: abjad.tools.scoretools.Container.Container.__getitem__

.. automethod:: abjad.tools.scoretools.Container.Container.__graph__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Container.Container.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Container.Container.__illustrate__

.. automethod:: abjad.tools.scoretools.Container.Container.__iter__

.. automethod:: abjad.tools.scoretools.Container.Container.__len__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Container.Container.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Container.Container.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Container.Container.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Container.Container.__rmul__

.. automethod:: abjad.tools.scoretools.Container.Container.__setitem__
