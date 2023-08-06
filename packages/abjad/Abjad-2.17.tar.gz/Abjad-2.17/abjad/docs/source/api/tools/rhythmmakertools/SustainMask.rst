.. currentmodule:: abjad.tools.rhythmmakertools

SustainMask
===========

.. autoclass:: SustainMask

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
          subgraph cluster_rhythmmakertools {
              graph [label=rhythmmakertools];
              "abjad.tools.rhythmmakertools.SustainMask.SustainMask" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>SustainMask</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.rhythmmakertools.SustainMask.SustainMask";
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

      ~abjad.tools.rhythmmakertools.SustainMask.SustainMask.pattern
      ~abjad.tools.rhythmmakertools.SustainMask.SustainMask.__copy__
      ~abjad.tools.rhythmmakertools.SustainMask.SustainMask.__eq__
      ~abjad.tools.rhythmmakertools.SustainMask.SustainMask.__format__
      ~abjad.tools.rhythmmakertools.SustainMask.SustainMask.__hash__
      ~abjad.tools.rhythmmakertools.SustainMask.SustainMask.__ne__
      ~abjad.tools.rhythmmakertools.SustainMask.SustainMask.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.rhythmmakertools.SustainMask.SustainMask.pattern

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.SustainMask.SustainMask.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.SustainMask.SustainMask.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.SustainMask.SustainMask.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.SustainMask.SustainMask.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.SustainMask.SustainMask.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.rhythmmakertools.SustainMask.SustainMask.__repr__
