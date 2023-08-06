.. currentmodule:: abjad.tools.rhythmmakertools

DurationSpellingSpecifier
=========================

.. autoclass:: DurationSpellingSpecifier

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
              "abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>DurationSpellingSpecifier</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier";
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

      ~abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.decrease_durations_monotonically
      ~abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.forbid_meter_rewriting
      ~abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.forbidden_written_duration
      ~abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.rewrite_meter
      ~abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.spell_metrically
      ~abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.__copy__
      ~abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.__eq__
      ~abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.__format__
      ~abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.__hash__
      ~abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.__ne__
      ~abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.decrease_durations_monotonically

.. autoattribute:: abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.forbid_meter_rewriting

.. autoattribute:: abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.forbidden_written_duration

.. autoattribute:: abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.rewrite_meter

.. autoattribute:: abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.spell_metrically

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.__eq__

.. automethod:: abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.__ne__

.. automethod:: abjad.tools.rhythmmakertools.DurationSpellingSpecifier.DurationSpellingSpecifier.__repr__
