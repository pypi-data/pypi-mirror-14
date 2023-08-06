.. currentmodule:: abjad.tools.lilypondnametools

LilyPondContextSetting
======================

.. autoclass:: LilyPondContextSetting

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
              "abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LilyPondContextSetting</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting";
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

      ~abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.context_name
      ~abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.context_property
      ~abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.format_pieces
      ~abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.is_unset
      ~abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.value
      ~abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.__eq__
      ~abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.__format__
      ~abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.__hash__
      ~abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.__ne__
      ~abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.context_name

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.context_property

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.format_pieces

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.is_unset

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.value

Special methods
---------------

.. automethod:: abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.__format__

.. automethod:: abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondContextSetting.LilyPondContextSetting.__repr__
