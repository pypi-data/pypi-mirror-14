.. currentmodule:: abjad.tools.systemtools

LilyPondFormatBundle
====================

.. autoclass:: LilyPondFormatBundle

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
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LilyPondFormatBundle</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle";
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

      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.after
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.alphabetize
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.before
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.closing
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.context_settings
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.get
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.grob_overrides
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.grob_reverts
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.make_immutable
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.opening
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.right
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.update
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.__eq__
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.__format__
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.__hash__
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.__ne__
      ~abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.after

.. autoattribute:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.before

.. autoattribute:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.closing

.. autoattribute:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.context_settings

.. autoattribute:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.grob_overrides

.. autoattribute:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.grob_reverts

.. autoattribute:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.opening

.. autoattribute:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.right

Methods
-------

.. automethod:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.alphabetize

.. automethod:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.get

.. automethod:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.make_immutable

.. automethod:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.update

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle.__repr__
