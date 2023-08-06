.. currentmodule:: abjad.tools.lilypondnametools

LilyPondGrobInterface
=====================

.. autoclass:: LilyPondGrobInterface

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
              "abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LilyPondGrobInterface</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface";
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

      ~abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.list_all_interfaces
      ~abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.name
      ~abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.property_names
      ~abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__copy__
      ~abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__eq__
      ~abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__format__
      ~abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__hash__
      ~abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__ne__
      ~abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__new__
      ~abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.name

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.property_names

Class & static methods
----------------------

.. automethod:: abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.list_all_interfaces

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__ne__

.. automethod:: abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondGrobInterface.LilyPondGrobInterface.__repr__
