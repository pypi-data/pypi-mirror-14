.. currentmodule:: abjad.tools.scoretools

Component
=========

.. autoclass:: Component

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
              "abjad.tools.scoretools.Chord.Chord" [color=3,
                  group=2,
                  label=Chord,
                  shape=box];
              "abjad.tools.scoretools.Cluster.Cluster" [color=3,
                  group=2,
                  label=Cluster,
                  shape=box];
              "abjad.tools.scoretools.Component.Component" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Component</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Container.Container" [color=3,
                  group=2,
                  label=Container,
                  shape=box];
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
              "abjad.tools.scoretools.Leaf.Leaf" [color=3,
                  group=2,
                  label=Leaf,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.Measure.Measure" [color=3,
                  group=2,
                  label=Measure,
                  shape=box];
              "abjad.tools.scoretools.MultimeasureRest.MultimeasureRest" [color=3,
                  group=2,
                  label=MultimeasureRest,
                  shape=box];
              "abjad.tools.scoretools.Note.Note" [color=3,
                  group=2,
                  label=Note,
                  shape=box];
              "abjad.tools.scoretools.Rest.Rest" [color=3,
                  group=2,
                  label=Rest,
                  shape=box];
              "abjad.tools.scoretools.Score.Score" [color=3,
                  group=2,
                  label=Score,
                  shape=box];
              "abjad.tools.scoretools.Skip.Skip" [color=3,
                  group=2,
                  label=Skip,
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
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Leaf.Leaf";
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
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Chord.Chord";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.MultimeasureRest.MultimeasureRest";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Note.Note";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Rest.Rest";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Skip.Skip";
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

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.scoretools.Component.Component.name
      ~abjad.tools.scoretools.Component.Component.__copy__
      ~abjad.tools.scoretools.Component.Component.__eq__
      ~abjad.tools.scoretools.Component.Component.__format__
      ~abjad.tools.scoretools.Component.Component.__hash__
      ~abjad.tools.scoretools.Component.Component.__illustrate__
      ~abjad.tools.scoretools.Component.Component.__mul__
      ~abjad.tools.scoretools.Component.Component.__ne__
      ~abjad.tools.scoretools.Component.Component.__repr__
      ~abjad.tools.scoretools.Component.Component.__rmul__

Read/write properties
---------------------

.. autoattribute:: abjad.tools.scoretools.Component.Component.name

Special methods
---------------

.. automethod:: abjad.tools.scoretools.Component.Component.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Component.Component.__eq__

.. automethod:: abjad.tools.scoretools.Component.Component.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Component.Component.__hash__

.. automethod:: abjad.tools.scoretools.Component.Component.__illustrate__

.. automethod:: abjad.tools.scoretools.Component.Component.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Component.Component.__ne__

.. automethod:: abjad.tools.scoretools.Component.Component.__repr__

.. automethod:: abjad.tools.scoretools.Component.Component.__rmul__
