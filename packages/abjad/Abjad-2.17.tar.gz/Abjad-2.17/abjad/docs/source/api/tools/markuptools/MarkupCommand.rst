.. currentmodule:: abjad.tools.markuptools

MarkupCommand
=============

.. autoclass:: MarkupCommand

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
          subgraph cluster_markuptools {
              graph [label=markuptools];
              "abjad.tools.markuptools.MarkupCommand.MarkupCommand" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>MarkupCommand</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.MarkupCommand.MarkupCommand";
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

      ~abjad.tools.markuptools.MarkupCommand.MarkupCommand.args
      ~abjad.tools.markuptools.MarkupCommand.MarkupCommand.combine_markup_commands
      ~abjad.tools.markuptools.MarkupCommand.MarkupCommand.command
      ~abjad.tools.markuptools.MarkupCommand.MarkupCommand.force_quotes
      ~abjad.tools.markuptools.MarkupCommand.MarkupCommand.__copy__
      ~abjad.tools.markuptools.MarkupCommand.MarkupCommand.__eq__
      ~abjad.tools.markuptools.MarkupCommand.MarkupCommand.__format__
      ~abjad.tools.markuptools.MarkupCommand.MarkupCommand.__hash__
      ~abjad.tools.markuptools.MarkupCommand.MarkupCommand.__ne__
      ~abjad.tools.markuptools.MarkupCommand.MarkupCommand.__repr__
      ~abjad.tools.markuptools.MarkupCommand.MarkupCommand.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.markuptools.MarkupCommand.MarkupCommand.args

.. autoattribute:: abjad.tools.markuptools.MarkupCommand.MarkupCommand.command

Read/write properties
---------------------

.. autoattribute:: abjad.tools.markuptools.MarkupCommand.MarkupCommand.force_quotes

Class & static methods
----------------------

.. automethod:: abjad.tools.markuptools.MarkupCommand.MarkupCommand.combine_markup_commands

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupCommand.MarkupCommand.__copy__

.. automethod:: abjad.tools.markuptools.MarkupCommand.MarkupCommand.__eq__

.. automethod:: abjad.tools.markuptools.MarkupCommand.MarkupCommand.__format__

.. automethod:: abjad.tools.markuptools.MarkupCommand.MarkupCommand.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupCommand.MarkupCommand.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.MarkupCommand.MarkupCommand.__repr__

.. automethod:: abjad.tools.markuptools.MarkupCommand.MarkupCommand.__str__
