.. currentmodule:: abjad.tools.lilypondparsertools

ReducedLyParser
===============

.. autoclass:: ReducedLyParser

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
              "abjad.tools.abctools.Parser.Parser" [color=1,
                  group=0,
                  label=Parser,
                  shape=oval,
                  style=bold];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.Parser.Parser";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_lilypondparsertools {
              graph [label=lilypondparsertools];
              "abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ReducedLyParser</B>>,
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
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.abctools.Parser`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.debug
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.lexer
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.lexer_rules_object
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.logger
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.logger_path
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.output_path
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_apostrophes__APOSTROPHE
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_apostrophes__apostrophes__APOSTROPHE
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_beam__BRACKET_L
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_beam__BRACKET_R
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_chord_body__chord_pitches
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_chord_body__chord_pitches__positive_leaf_duration
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_chord_pitches__CARAT_L__pitches__CARAT_R
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_commas__COMMA
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_commas__commas__commas
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_component__container
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_component__fixed_duration_container
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_component__leaf
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_component__tuplet
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_component_list__EMPTY
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_component_list__component_list__component
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_container__BRACE_L__component_list__BRACE_R
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_dots__EMPTY
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_dots__dots__DOT
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_error
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_fixed_duration_container__BRACE_L__FRACTION__BRACE_R
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_leaf__leaf_body__post_events
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_leaf_body__chord_body
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_leaf_body__note_body
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_leaf_body__rest_body
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_measure__PIPE__FRACTION__component_list__PIPE
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_negative_leaf_duration__INTEGER_N__dots
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_note_body__pitch
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_note_body__pitch__positive_leaf_duration
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_note_body__positive_leaf_duration
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_pitch__PITCHNAME
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_pitch__PITCHNAME__apostrophes
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_pitch__PITCHNAME__commas
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_pitches__pitch
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_pitches__pitches__pitch
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_positive_leaf_duration__INTEGER_P__dots
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_post_event__beam
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_post_event__slur
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_post_event__tie
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_post_events__EMPTY
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_post_events__post_events__post_event
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_rest_body__RESTNAME
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_rest_body__RESTNAME__positive_leaf_duration
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_rest_body__negative_leaf_duration
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_slur__PAREN_L
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_slur__PAREN_R
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_start__EMPTY
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_start__start__component
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_start__start__measure
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_tie__TILDE
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_tuplet__FRACTION__container
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.parser
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.parser_rules_object
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.pickle_path
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.t_FRACTION
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.t_INTEGER_N
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.t_INTEGER_P
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.t_PITCHNAME
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.t_error
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.t_newline
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.tokenize
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.__call__
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.__eq__
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.__format__
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.__hash__
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.__ne__
      ~abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.debug

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.lexer

.. autoattribute:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.lexer_rules_object

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.logger

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.logger_path

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.output_path

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.parser

.. autoattribute:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.parser_rules_object

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.pickle_path

Methods
-------

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_apostrophes__APOSTROPHE

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_apostrophes__apostrophes__APOSTROPHE

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_beam__BRACKET_L

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_beam__BRACKET_R

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_chord_body__chord_pitches

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_chord_body__chord_pitches__positive_leaf_duration

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_chord_pitches__CARAT_L__pitches__CARAT_R

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_commas__COMMA

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_commas__commas__commas

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_component__container

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_component__fixed_duration_container

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_component__leaf

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_component__tuplet

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_component_list__EMPTY

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_component_list__component_list__component

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_container__BRACE_L__component_list__BRACE_R

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_dots__EMPTY

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_dots__dots__DOT

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_error

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_fixed_duration_container__BRACE_L__FRACTION__BRACE_R

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_leaf__leaf_body__post_events

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_leaf_body__chord_body

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_leaf_body__note_body

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_leaf_body__rest_body

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_measure__PIPE__FRACTION__component_list__PIPE

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_negative_leaf_duration__INTEGER_N__dots

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_note_body__pitch

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_note_body__pitch__positive_leaf_duration

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_note_body__positive_leaf_duration

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_pitch__PITCHNAME

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_pitch__PITCHNAME__apostrophes

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_pitch__PITCHNAME__commas

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_pitches__pitch

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_pitches__pitches__pitch

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_positive_leaf_duration__INTEGER_P__dots

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_post_event__beam

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_post_event__slur

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_post_event__tie

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_post_events__EMPTY

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_post_events__post_events__post_event

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_rest_body__RESTNAME

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_rest_body__RESTNAME__positive_leaf_duration

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_rest_body__negative_leaf_duration

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_slur__PAREN_L

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_slur__PAREN_R

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_start__EMPTY

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_start__start__component

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_start__start__measure

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_tie__TILDE

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.p_tuplet__FRACTION__container

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.t_FRACTION

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.t_INTEGER_N

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.t_INTEGER_P

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.t_PITCHNAME

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.t_error

.. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.t_newline

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.tokenize

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.ReducedLyParser.ReducedLyParser.__repr__
