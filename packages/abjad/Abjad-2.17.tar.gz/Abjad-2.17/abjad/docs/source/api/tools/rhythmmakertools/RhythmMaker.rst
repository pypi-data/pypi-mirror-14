.. currentmodule:: abjad.tools.rhythmmakertools

RhythmMaker
===========

.. autoclass:: RhythmMaker

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
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker" [color=3,
                  group=2,
                  label=AccelerandoRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.EvenDivisionRhythmMaker.EvenDivisionRhythmMaker" [color=3,
                  group=2,
                  label=EvenDivisionRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker" [color=3,
                  group=2,
                  label=EvenRunRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker" [color=3,
                  group=2,
                  label=IncisedRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.NoteRhythmMaker.NoteRhythmMaker" [color=3,
                  group=2,
                  label=NoteRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>RhythmMaker</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker" [color=3,
                  group=2,
                  label=SkipRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker" [color=3,
                  group=2,
                  label=TaleaRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.TupletRhythmMaker.TupletRhythmMaker" [color=3,
                  group=2,
                  label=TupletRhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.AccelerandoRhythmMaker.AccelerandoRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.EvenDivisionRhythmMaker.EvenDivisionRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.IncisedRhythmMaker.IncisedRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.NoteRhythmMaker.NoteRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.SkipRhythmMaker.SkipRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.TaleaRhythmMaker.TaleaRhythmMaker";
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.TupletRhythmMaker.TupletRhythmMaker";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker";
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

      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.beam_specifier
      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.division_masks
      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.duration_spelling_specifier
      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.logical_tie_masks
      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.tie_specifier
      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.tuplet_spelling_specifier
      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__call__
      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__copy__
      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__eq__
      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__format__
      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__hash__
      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__illustrate__
      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__ne__
      ~abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.beam_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.division_masks

.. autoattribute:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.duration_spelling_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.logical_tie_masks

.. autoattribute:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.tie_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.tuplet_spelling_specifier

Special methods
---------------

.. automethod:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__copy__

.. automethod:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__eq__

.. automethod:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__format__

.. automethod:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__hash__

.. automethod:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker.__repr__
