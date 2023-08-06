.. currentmodule:: abjad.tools.lilypondnametools

LilyPondGrobOverride
====================

.. autoclass:: LilyPondGrobOverride

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
              "abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LilyPondGrobOverride</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride";
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

      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.context_name
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.grob_name
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.is_once
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.is_revert
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.override_format_pieces
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.override_string
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.property_path
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.revert_format_pieces
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.revert_string
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.value
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.__eq__
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.__format__
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.__hash__
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.__ne__
      ~abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.context_name

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.grob_name

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.is_once

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.is_revert

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.override_format_pieces

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.override_string

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.property_path

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.revert_format_pieces

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.revert_string

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.value

Special methods
---------------

.. automethod:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.__format__

.. automethod:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrobOverride.LilyPondGrobOverride.__repr__
