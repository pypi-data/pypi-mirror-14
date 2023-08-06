.. currentmodule:: abjad.tools.lilypondfiletools

ContextBlock
============

.. autoclass:: ContextBlock

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
          subgraph cluster_lilypondfiletools {
              graph [label=lilypondfiletools];
              "abjad.tools.lilypondfiletools.Block.Block" [color=3,
                  group=2,
                  label=Block,
                  shape=box];
              "abjad.tools.lilypondfiletools.ContextBlock.ContextBlock" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ContextBlock</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondfiletools.Block.Block" -> "abjad.tools.lilypondfiletools.ContextBlock.ContextBlock";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.Block.Block";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.lilypondfiletools.Block`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.accepts_commands
      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.alias
      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.consists_commands
      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.items
      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.name
      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.remove_commands
      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.source_context_name
      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.type_
      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.__eq__
      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.__format__
      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.__getitem__
      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.__hash__
      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.__ne__
      ~abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.accepts_commands

.. autoattribute:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.alias

.. autoattribute:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.consists_commands

.. autoattribute:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.items

.. autoattribute:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.name

.. autoattribute:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.remove_commands

.. autoattribute:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.source_context_name

.. autoattribute:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.type_

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.ContextBlock.ContextBlock.__repr__
