.. currentmodule:: abjad.tools.lilypondnametools

LilyPondEngraver
================

.. autoclass:: LilyPondEngraver

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
              "abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LilyPondEngraver</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver";
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

      ~abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.grobs
      ~abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.list_all_engravers
      ~abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.name
      ~abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.property_names
      ~abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__copy__
      ~abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__eq__
      ~abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__format__
      ~abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__hash__
      ~abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__ne__
      ~abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__new__
      ~abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.grobs

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.name

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.property_names

Class & static methods
----------------------

.. automethod:: abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.list_all_engravers

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__ne__

.. automethod:: abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondEngraver.LilyPondEngraver.__repr__
