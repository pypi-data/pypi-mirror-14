.. currentmodule:: abjad.tools.scoretools

Leaf
====

.. autoclass:: Leaf

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
              "abjad.tools.scoretools.Component.Component" [color=3,
                  group=2,
                  label=Component,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.Leaf.Leaf" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Leaf</B>>,
                  shape=oval,
                  style="filled, rounded"];
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
              "abjad.tools.scoretools.Skip.Skip" [color=3,
                  group=2,
                  label=Skip,
                  shape=box];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Leaf.Leaf";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Chord.Chord";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.MultimeasureRest.MultimeasureRest";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Note.Note";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Rest.Rest";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Skip.Skip";
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

      ~abjad.tools.scoretools.Leaf.Leaf.name
      ~abjad.tools.scoretools.Leaf.Leaf.written_duration
      ~abjad.tools.scoretools.Leaf.Leaf.__copy__
      ~abjad.tools.scoretools.Leaf.Leaf.__eq__
      ~abjad.tools.scoretools.Leaf.Leaf.__format__
      ~abjad.tools.scoretools.Leaf.Leaf.__hash__
      ~abjad.tools.scoretools.Leaf.Leaf.__illustrate__
      ~abjad.tools.scoretools.Leaf.Leaf.__mul__
      ~abjad.tools.scoretools.Leaf.Leaf.__ne__
      ~abjad.tools.scoretools.Leaf.Leaf.__repr__
      ~abjad.tools.scoretools.Leaf.Leaf.__rmul__
      ~abjad.tools.scoretools.Leaf.Leaf.__str__

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Leaf.Leaf.name

.. autoattribute:: abjad.tools.scoretools.Leaf.Leaf.written_duration

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Leaf.Leaf.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Leaf.Leaf.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Leaf.Leaf.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Leaf.Leaf.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Leaf.Leaf.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Leaf.Leaf.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Leaf.Leaf.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Leaf.Leaf.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Leaf.Leaf.__rmul__

.. automethod:: abjad.tools.scoretools.Leaf.Leaf.__str__
