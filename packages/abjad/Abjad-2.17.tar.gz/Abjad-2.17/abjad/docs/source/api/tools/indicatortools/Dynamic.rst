.. currentmodule:: abjad.tools.indicatortools

Dynamic
=======

.. autoclass:: Dynamic

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
              "abjad.tools.indicatortools.Dynamic.Dynamic" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Dynamic</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.indicatortools.Dynamic.Dynamic";
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

      ~abjad.tools.indicatortools.Dynamic.Dynamic.composite_dynamic_name_to_steady_state_dynamic_name
      ~abjad.tools.indicatortools.Dynamic.Dynamic.default_scope
      ~abjad.tools.indicatortools.Dynamic.Dynamic.dynamic_name_to_dynamic_ordinal
      ~abjad.tools.indicatortools.Dynamic.Dynamic.dynamic_ordinal_to_dynamic_name
      ~abjad.tools.indicatortools.Dynamic.Dynamic.is_dynamic_name
      ~abjad.tools.indicatortools.Dynamic.Dynamic.name
      ~abjad.tools.indicatortools.Dynamic.Dynamic.ordinal
      ~abjad.tools.indicatortools.Dynamic.Dynamic.__copy__
      ~abjad.tools.indicatortools.Dynamic.Dynamic.__eq__
      ~abjad.tools.indicatortools.Dynamic.Dynamic.__format__
      ~abjad.tools.indicatortools.Dynamic.Dynamic.__hash__
      ~abjad.tools.indicatortools.Dynamic.Dynamic.__ne__
      ~abjad.tools.indicatortools.Dynamic.Dynamic.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.indicatortools.Dynamic.Dynamic.default_scope

.. autoattribute:: abjad.tools.indicatortools.Dynamic.Dynamic.name

.. autoattribute:: abjad.tools.indicatortools.Dynamic.Dynamic.ordinal

Class & static methods
----------------------

.. automethod:: abjad.tools.indicatortools.Dynamic.Dynamic.composite_dynamic_name_to_steady_state_dynamic_name

.. automethod:: abjad.tools.indicatortools.Dynamic.Dynamic.dynamic_name_to_dynamic_ordinal

.. automethod:: abjad.tools.indicatortools.Dynamic.Dynamic.dynamic_ordinal_to_dynamic_name

.. automethod:: abjad.tools.indicatortools.Dynamic.Dynamic.is_dynamic_name

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.Dynamic.Dynamic.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.Dynamic.Dynamic.__eq__

.. automethod:: abjad.tools.indicatortools.Dynamic.Dynamic.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.Dynamic.Dynamic.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.Dynamic.Dynamic.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.indicatortools.Dynamic.Dynamic.__repr__
