.. currentmodule:: abjad.tools.lilypondparsertools

LilyPondLexicalDefinition
=========================

.. autoclass:: LilyPondLexicalDefinition

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
          subgraph cluster_lilypondparsertools {
              graph [label=lilypondparsertools];
              "abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LilyPondLexicalDefinition</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition";
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

      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.push_signature
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.scan_bare_word
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.scan_escaped_word
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_651_a
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_651_b
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_661
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_666
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_ANY_165
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_643
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_646
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_210
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_214
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_214_EOF
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_216
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_218
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_220
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_222
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_227
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_353
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_notes_233
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_notes_387
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_notes_390
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_notes_396
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_notes_399
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_notes_686
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_error
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_longcomment_291
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_longcomment_293
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_longcomment_296
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_longcomment_error
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_markup_545
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_markup_548
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_markup_601
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_markup_error
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_newline
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_417
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_421
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_424
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_428
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_428b
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_433
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_error
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_quote_440
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_quote_443
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_quote_446
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_quote_456
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_quote_XXX
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_quote_error
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_scheme_error
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_version_242
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_version_278
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_version_341
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_version_error
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.__eq__
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.__format__
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.__hash__
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.__ne__
      ~abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.__repr__

Methods
-------

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.push_signature

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.scan_bare_word

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.scan_escaped_word

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_651_a

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_651_b

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_661

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_666

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_ANY_165

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_643

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_646

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_210

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_214

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_214_EOF

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_216

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_218

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_220

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_222

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_227

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_markup_notes_353

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_notes_233

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_notes_387

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_notes_390

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_notes_396

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_notes_399

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_INITIAL_notes_686

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_error

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_longcomment_291

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_longcomment_293

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_longcomment_296

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_longcomment_error

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_markup_545

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_markup_548

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_markup_601

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_markup_error

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_newline

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_417

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_421

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_424

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_428

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_428b

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_433

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_notes_error

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_quote_440

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_quote_443

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_quote_446

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_quote_456

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_quote_XXX

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_quote_error

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_scheme_error

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_version_242

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_version_278

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_version_341

.. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.t_version_error

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.LilyPondLexicalDefinition.LilyPondLexicalDefinition.__repr__
