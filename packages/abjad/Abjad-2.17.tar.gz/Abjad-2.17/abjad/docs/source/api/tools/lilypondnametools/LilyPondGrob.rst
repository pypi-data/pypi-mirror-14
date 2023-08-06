.. currentmodule:: abjad.tools.lilypondnametools

LilyPondGrob
============

.. autoclass:: LilyPondGrob

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
          subgraph cluster_lilypondnametools {
              graph [label=lilypondnametools];
              "abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LilyPondGrob</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob";
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

      ~abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.interfaces
      ~abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.list_all_grobs
      ~abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.name
      ~abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.property_names
      ~abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__copy__
      ~abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__eq__
      ~abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__format__
      ~abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__hash__
      ~abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__ne__
      ~abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__new__
      ~abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.interfaces

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.name

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.property_names

Class & static methods
----------------------

.. automethod:: abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.list_all_grobs

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__ne__

.. automethod:: abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrob.LilyPondGrob.__repr__
