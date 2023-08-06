.. currentmodule:: abjad.tools.scoretools

Chord
=====

.. autoclass:: Chord

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
              "abjad.tools.scoretools.Chord.Chord" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Chord</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.Component.Component" [color=3,
                  group=2,
                  label=Component,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.Leaf.Leaf" [color=3,
                  group=2,
                  label=Leaf,
                  shape=oval,
                  style=bold];
              "abjad.tools.scoretools.Component.Component" -> "abjad.tools.scoretools.Leaf.Leaf";
              "abjad.tools.scoretools.Leaf.Leaf" -> "abjad.tools.scoretools.Chord.Chord";
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

- :py:class:`abjad.tools.scoretools.Leaf`

- :py:class:`abjad.tools.scoretools.Component`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.scoretools.Chord.Chord.name
      ~abjad.tools.scoretools.Chord.Chord.note_heads
      ~abjad.tools.scoretools.Chord.Chord.written_duration
      ~abjad.tools.scoretools.Chord.Chord.written_pitches
      ~abjad.tools.scoretools.Chord.Chord.__copy__
      ~abjad.tools.scoretools.Chord.Chord.__eq__
      ~abjad.tools.scoretools.Chord.Chord.__format__
      ~abjad.tools.scoretools.Chord.Chord.__hash__
      ~abjad.tools.scoretools.Chord.Chord.__illustrate__
      ~abjad.tools.scoretools.Chord.Chord.__mul__
      ~abjad.tools.scoretools.Chord.Chord.__ne__
      ~abjad.tools.scoretools.Chord.Chord.__repr__
      ~abjad.tools.scoretools.Chord.Chord.__rmul__
      ~abjad.tools.scoretools.Chord.Chord.__str__

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.Chord.Chord.name

.. autoattribute:: abjad.tools.scoretools.Chord.Chord.note_heads

.. autoattribute:: abjad.tools.scoretools.Chord.Chord.written_duration

.. autoattribute:: abjad.tools.scoretools.Chord.Chord.written_pitches

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Chord.Chord.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Chord.Chord.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Chord.Chord.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Chord.Chord.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Chord.Chord.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Chord.Chord.__mul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Chord.Chord.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Chord.Chord.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Chord.Chord.__rmul__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.Chord.Chord.__str__
