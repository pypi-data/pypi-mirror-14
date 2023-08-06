.. currentmodule:: abjad.tools.rhythmmakertools

EvenRunRhythmMaker
==================

.. autoclass:: EvenRunRhythmMaker

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
              "abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>EvenRunRhythmMaker</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" [color=3,
                  group=2,
                  label=RhythmMaker,
                  shape=box];
              "abjad.tools.rhythmmakertools.RhythmMaker.RhythmMaker" -> "abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker";
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

- :py:class:`abjad.tools.rhythmmakertools.RhythmMaker`

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.beam_specifier
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.division_masks
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.duration_spelling_specifier
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.exponent
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.logical_tie_masks
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.tie_specifier
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.tuplet_spelling_specifier
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__call__
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__copy__
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__eq__
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__format__
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__hash__
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__illustrate__
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__ne__
      ~abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.beam_specifier

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.division_masks

.. autoattribute:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.duration_spelling_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.exponent

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.logical_tie_masks

.. autoattribute:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.tie_specifier

.. autoattribute:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.tuplet_spelling_specifier

Special methods
---------------

.. automethod:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__eq__

.. automethod:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.EvenRunRhythmMaker.EvenRunRhythmMaker.__repr__
