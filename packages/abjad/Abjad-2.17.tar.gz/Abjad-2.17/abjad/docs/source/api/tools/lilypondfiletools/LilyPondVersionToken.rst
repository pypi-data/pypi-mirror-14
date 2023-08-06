.. currentmodule:: abjad.tools.lilypondfiletools

LilyPondVersionToken
====================

.. autoclass:: LilyPondVersionToken

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
              "abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LilyPondVersionToken</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken";
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

      ~abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken.version_string
      ~abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken.__eq__
      ~abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken.__format__
      ~abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken.__hash__
      ~abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken.__ne__
      ~abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken.version_string

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken.__eq__

.. automethod:: abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken.__ne__

.. automethod:: abjad.tools.lilypondfiletools.LilyPondVersionToken.LilyPondVersionToken.__repr__
