.. currentmodule:: abjad.tools.lilypondnametools

LilyPondContext
===============

.. autoclass:: LilyPondContext

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
              "abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LilyPondContext</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext";
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

      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.accepted_by
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.accepts
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.alias
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.default_child
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.engravers
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.grobs
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.is_bottom_context
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.is_custom
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.is_global_context
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.is_score_context
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.is_staff_context
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.is_staff_group_context
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.list_all_contexts
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.name
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.property_names
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.register
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.unregister
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__copy__
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__eq__
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__format__
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__hash__
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__ne__
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__new__
      ~abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.accepted_by

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.accepts

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.alias

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.default_child

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.engravers

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.grobs

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.is_bottom_context

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.is_custom

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.is_global_context

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.is_score_context

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.is_staff_context

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.is_staff_group_context

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.name

.. autoattribute:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.property_names

Methods
-------

.. automethod:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.unregister

Class & static methods
----------------------

.. automethod:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.list_all_contexts

.. automethod:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.register

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__ne__

.. automethod:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__new__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondnametools.LilyPondContext.LilyPondContext.__repr__
