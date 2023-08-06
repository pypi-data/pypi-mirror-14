.. currentmodule:: abjad.tools.indicatortools

Fermata
=======

.. autoclass:: Fermata

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
          subgraph cluster_indicatortools {
              graph [label=indicatortools];
              "abjad.tools.indicatortools.Fermata.Fermata" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Fermata</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Fermata.Fermata";
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

      ~abjad.tools.indicatortools.Fermata.Fermata.command
      ~abjad.tools.indicatortools.Fermata.Fermata.default_scope
      ~abjad.tools.indicatortools.Fermata.Fermata.list_allowable_commands
      ~abjad.tools.indicatortools.Fermata.Fermata.__copy__
      ~abjad.tools.indicatortools.Fermata.Fermata.__eq__
      ~abjad.tools.indicatortools.Fermata.Fermata.__format__
      ~abjad.tools.indicatortools.Fermata.Fermata.__hash__
      ~abjad.tools.indicatortools.Fermata.Fermata.__ne__
      ~abjad.tools.indicatortools.Fermata.Fermata.__repr__
      ~abjad.tools.indicatortools.Fermata.Fermata.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.indicatortools.Fermata.Fermata.command

.. autoattribute:: abjad.tools.indicatortools.Fermata.Fermata.default_scope

Class & static methods
----------------------

.. automethod:: abjad.tools.indicatortools.Fermata.Fermata.list_allowable_commands

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.Fermata.Fermata.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.Fermata.Fermata.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.Fermata.Fermata.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.Fermata.Fermata.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.Fermata.Fermata.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.Fermata.Fermata.__repr__

.. automethod:: abjad.tools.indicatortools.Fermata.Fermata.__str__
