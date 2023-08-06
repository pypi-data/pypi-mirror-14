.. currentmodule:: abjad.tools.lilypondnametools

LilyPondNameManager
===================

.. autoclass:: LilyPondNameManager

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
          subgraph cluster_lilypondnametools {
              graph [label=lilypondnametools];
              "abjad.tools.lilypondnametools.LilyPondGrobNameManager.LilyPondGrobNameManager" [color=3,
                  group=2,
                  label=LilyPondGrobNameManager,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LilyPondNameManager</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.lilypondnametools.LilyPondSettingNameManager.LilyPondSettingNameManager" [color=3,
                  group=2,
                  label=LilyPondSettingNameManager,
                  shape=box];
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" -> "abjad.tools.lilypondnametools.LilyPondGrobNameManager.LilyPondGrobNameManager";
              "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager" -> "abjad.tools.lilypondnametools.LilyPondSettingNameManager.LilyPondSettingNameManager";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager";
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

      ~abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__eq__
      ~abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__format__
      ~abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__hash__
      ~abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__ne__
      ~abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__repr__

Special methods
---------------

.. automethod:: abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__format__

.. automethod:: abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__ne__

.. automethod:: abjad.tools.lilypondnametools.LilyPondNameManager.LilyPondNameManager.__repr__
