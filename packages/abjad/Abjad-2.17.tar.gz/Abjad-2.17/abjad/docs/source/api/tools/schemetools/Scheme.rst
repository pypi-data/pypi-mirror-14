.. currentmodule:: abjad.tools.schemetools

Scheme
======

.. autoclass:: Scheme

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
          subgraph cluster_schemetools {
              graph [label=schemetools];
              "abjad.tools.schemetools.Scheme.Scheme" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Scheme</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.schemetools.SchemeAssociativeList.SchemeAssociativeList" [color=3,
                  group=2,
                  label=SchemeAssociativeList,
                  shape=box];
              "abjad.tools.schemetools.SchemeColor.SchemeColor" [color=3,
                  group=2,
                  label=SchemeColor,
                  shape=box];
              "abjad.tools.schemetools.SchemeMoment.SchemeMoment" [color=3,
                  group=2,
                  label=SchemeMoment,
                  shape=box];
              "abjad.tools.schemetools.SchemePair.SchemePair" [color=3,
                  group=2,
                  label=SchemePair,
                  shape=box];
              "abjad.tools.schemetools.SchemeSymbol.SchemeSymbol" [color=3,
                  group=2,
                  label=SchemeSymbol,
                  shape=box];
              "abjad.tools.schemetools.SchemeVector.SchemeVector" [color=3,
                  group=2,
                  label=SchemeVector,
                  shape=box];
              "abjad.tools.schemetools.SchemeVectorConstant.SchemeVectorConstant" [color=3,
                  group=2,
                  label=SchemeVectorConstant,
                  shape=box];
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeAssociativeList.SchemeAssociativeList";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeColor.SchemeColor";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeMoment.SchemeMoment";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemePair.SchemePair";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeSymbol.SchemeSymbol";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeVector.SchemeVector";
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeVectorConstant.SchemeVectorConstant";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.schemetools.Scheme.Scheme";
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

      ~abjad.tools.schemetools.Scheme.Scheme.force_quotes
      ~abjad.tools.schemetools.Scheme.Scheme.format_embedded_scheme_value
      ~abjad.tools.schemetools.Scheme.Scheme.format_scheme_value
      ~abjad.tools.schemetools.Scheme.Scheme.quoting
      ~abjad.tools.schemetools.Scheme.Scheme.verbatim
      ~abjad.tools.schemetools.Scheme.Scheme.__copy__
      ~abjad.tools.schemetools.Scheme.Scheme.__eq__
      ~abjad.tools.schemetools.Scheme.Scheme.__format__
      ~abjad.tools.schemetools.Scheme.Scheme.__hash__
      ~abjad.tools.schemetools.Scheme.Scheme.__ne__
      ~abjad.tools.schemetools.Scheme.Scheme.__repr__
      ~abjad.tools.schemetools.Scheme.Scheme.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.schemetools.Scheme.Scheme.force_quotes

.. autoattribute:: abjad.tools.schemetools.Scheme.Scheme.quoting

.. autoattribute:: abjad.tools.schemetools.Scheme.Scheme.verbatim

Class & static methods
----------------------

.. automethod:: abjad.tools.schemetools.Scheme.Scheme.format_embedded_scheme_value

.. automethod:: abjad.tools.schemetools.Scheme.Scheme.format_scheme_value

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.Scheme.Scheme.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.Scheme.Scheme.__eq__

.. automethod:: abjad.tools.schemetools.Scheme.Scheme.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.Scheme.Scheme.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.Scheme.Scheme.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.Scheme.Scheme.__repr__

.. automethod:: abjad.tools.schemetools.Scheme.Scheme.__str__
