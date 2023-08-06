.. currentmodule:: abjad.tools.lilypondparsertools

SchemeParser
============

.. autoclass:: SchemeParser

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
              "abjad.tools.lilypondparsertools.SchemeParser.SchemeParser" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>SchemeParser</B>>,
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
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.lilypondparsertools.SchemeParser.SchemeParser";
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

      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.debug
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.lexer
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.lexer_rules_object
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.logger
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.logger_path
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.output_path
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_boolean__BOOLEAN
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_constant__boolean
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_constant__number
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_constant__string
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_data__EMPTY
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_data__data__datum
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_datum__constant
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_datum__list
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_datum__symbol
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_datum__vector
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_error
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_expression__QUOTE__datum
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_expression__constant
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_expression__variable
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_form__expression
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_forms__EMPTY
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_forms__forms__form
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_list__L_PAREN__data__R_PAREN
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_list__L_PAREN__data__datum__PERIOD__datum__R_PAREN
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_number__DECIMAL
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_number__HEXADECIMAL
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_number__INTEGER
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_program__forms
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_string__STRING
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_symbol__IDENTIFIER
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_variable__IDENTIFIER
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_vector__HASH__L_PAREN__data__R_PAREN
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.parser
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.parser_rules_object
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.pickle_path
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_BOOLEAN
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_DECIMAL
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_HASH
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_HEXADECIMAL
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_IDENTIFIER
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_INTEGER
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_L_PAREN
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_R_PAREN
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_anything
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_error
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_newline
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_quote
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_quote_440
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_quote_443
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_quote_446
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_quote_456
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_quote_error
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_whitespace
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.tokenize
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.__call__
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.__eq__
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.__format__
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.__hash__
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.__ne__
      ~abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.debug

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.lexer

.. autoattribute:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.lexer_rules_object

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.logger

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.logger_path

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.output_path

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.parser

.. autoattribute:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.parser_rules_object

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.pickle_path

Methods
-------

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_boolean__BOOLEAN

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_constant__boolean

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_constant__number

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_constant__string

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_data__EMPTY

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_data__data__datum

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_datum__constant

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_datum__list

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_datum__symbol

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_datum__vector

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_error

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_expression__QUOTE__datum

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_expression__constant

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_expression__variable

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_form__expression

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_forms__EMPTY

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_forms__forms__form

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_list__L_PAREN__data__R_PAREN

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_list__L_PAREN__data__datum__PERIOD__datum__R_PAREN

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_number__DECIMAL

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_number__HEXADECIMAL

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_number__INTEGER

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_program__forms

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_string__STRING

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_symbol__IDENTIFIER

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_variable__IDENTIFIER

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.p_vector__HASH__L_PAREN__data__R_PAREN

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_BOOLEAN

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_DECIMAL

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_HASH

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_HEXADECIMAL

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_IDENTIFIER

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_INTEGER

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_L_PAREN

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_R_PAREN

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_anything

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_error

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_newline

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_quote

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_quote_440

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_quote_443

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_quote_446

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_quote_456

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_quote_error

.. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.t_whitespace

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.tokenize

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondparsertools.SchemeParser.SchemeParser.__repr__
