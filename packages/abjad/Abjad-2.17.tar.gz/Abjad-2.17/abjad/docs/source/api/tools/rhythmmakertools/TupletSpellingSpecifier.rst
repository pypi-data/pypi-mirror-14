.. currentmodule:: abjad.tools.rhythmmakertools

TupletSpellingSpecifier
=======================

.. autoclass:: TupletSpellingSpecifier

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
              "abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TupletSpellingSpecifier</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier";
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

      ~abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.avoid_dots
      ~abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.flatten_trivial_tuplets
      ~abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.is_diminution
      ~abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.rewrite_rest_filled_tuplets
      ~abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.simplify_redundant_tuplets
      ~abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.use_note_duration_bracket
      ~abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.__copy__
      ~abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.__eq__
      ~abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.__format__
      ~abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.__hash__
      ~abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.__ne__
      ~abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.avoid_dots

.. autoattribute:: abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.flatten_trivial_tuplets

.. autoattribute:: abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.is_diminution

.. autoattribute:: abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.rewrite_rest_filled_tuplets

.. autoattribute:: abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.simplify_redundant_tuplets

.. autoattribute:: abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.use_note_duration_bracket

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.TupletSpellingSpecifier.TupletSpellingSpecifier.__repr__
