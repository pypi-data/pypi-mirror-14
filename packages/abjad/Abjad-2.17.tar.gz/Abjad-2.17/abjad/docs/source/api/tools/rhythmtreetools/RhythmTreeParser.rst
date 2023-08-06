.. currentmodule:: abjad.tools.rhythmtreetools

RhythmTreeParser
================

.. autoclass:: RhythmTreeParser

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
          subgraph cluster_rhythmtreetools {
              graph [label=rhythmtreetools];
              "abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>RhythmTreeParser</B>>,
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
          "abjad.tools.abctools.Parser.Parser" -> "abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser";
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

      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.debug
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.lexer
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.lexer_rules_object
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.logger
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.logger_path
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.output_path
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_container__LPAREN__DURATION__node_list_closed__RPAREN
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_error
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_leaf__INTEGER
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_node__container
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_node__leaf
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_node_list__node_list__node_list_item
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_node_list__node_list_item
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_node_list_closed__LPAREN__node_list__RPAREN
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_node_list_item__node
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_toplevel__EMPTY
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_toplevel__toplevel__node
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.parser
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.parser_rules_object
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.pickle_path
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.t_DURATION
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.t_error
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.t_newline
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.tokenize
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.__call__
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.__eq__
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.__format__
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.__hash__
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.__ne__
      ~abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.debug

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.lexer

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.lexer_rules_object

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.logger

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.logger_path

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.output_path

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.parser

.. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.parser_rules_object

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.pickle_path

Methods
-------

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_container__LPAREN__DURATION__node_list_closed__RPAREN

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_error

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_leaf__INTEGER

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_node__container

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_node__leaf

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_node_list__node_list__node_list_item

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_node_list__node_list_item

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_node_list_closed__LPAREN__node_list__RPAREN

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_node_list_item__node

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_toplevel__EMPTY

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.p_toplevel__toplevel__node

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.t_DURATION

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.t_error

.. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.t_newline

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.tokenize

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.__call__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmtreetools.RhythmTreeParser.RhythmTreeParser.__repr__
