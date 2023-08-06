.. currentmodule:: abjad.tools.lilypondfiletools

Block
=====

.. autoclass:: Block

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
              "abjad.tools.lilypondfiletools.Block.Block" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Block</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondfiletools.ContextBlock.ContextBlock" [color=3,
                  group=2,
                  label=ContextBlock,
                  shape=box];
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

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.lilypondfiletools.Block.Block.items
      ~abjad.tools.lilypondfiletools.Block.Block.name
      ~abjad.tools.lilypondfiletools.Block.Block.__eq__
      ~abjad.tools.lilypondfiletools.Block.Block.__format__
      ~abjad.tools.lilypondfiletools.Block.Block.__getitem__
      ~abjad.tools.lilypondfiletools.Block.Block.__hash__
      ~abjad.tools.lilypondfiletools.Block.Block.__ne__
      ~abjad.tools.lilypondfiletools.Block.Block.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.lilypondfiletools.Block.Block.items

.. autoattribute:: abjad.tools.lilypondfiletools.Block.Block.name

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.Block.Block.__eq__

.. automethod:: abjad.tools.lilypondfiletools.Block.Block.__format__

.. automethod:: abjad.tools.lilypondfiletools.Block.Block.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.Block.Block.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.Block.Block.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.Block.Block.__repr__
