.. currentmodule:: abjad.tools.schemetools

SchemeVector
============

.. autoclass:: SchemeVector

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
              "abjad.tools.schemetools.Scheme.Scheme" [color=3,
                  group=2,
                  label=Scheme,
                  shape=box];
              "abjad.tools.schemetools.SchemeVector.SchemeVector" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>SchemeVector</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.schemetools.Scheme.Scheme" -> "abjad.tools.schemetools.SchemeVector.SchemeVector";
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

- :py:class:`abjad.tools.schemetools.Scheme`

- :py:class:`abjad.tools.abctools.AbjadValueObject`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.schemetools.SchemeVector.SchemeVector.force_quotes
      ~abjad.tools.schemetools.SchemeVector.SchemeVector.format_embedded_scheme_value
      ~abjad.tools.schemetools.SchemeVector.SchemeVector.format_scheme_value
      ~abjad.tools.schemetools.SchemeVector.SchemeVector.quoting
      ~abjad.tools.schemetools.SchemeVector.SchemeVector.verbatim
      ~abjad.tools.schemetools.SchemeVector.SchemeVector.__copy__
      ~abjad.tools.schemetools.SchemeVector.SchemeVector.__eq__
      ~abjad.tools.schemetools.SchemeVector.SchemeVector.__format__
      ~abjad.tools.schemetools.SchemeVector.SchemeVector.__hash__
      ~abjad.tools.schemetools.SchemeVector.SchemeVector.__ne__
      ~abjad.tools.schemetools.SchemeVector.SchemeVector.__repr__
      ~abjad.tools.schemetools.SchemeVector.SchemeVector.__str__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.schemetools.SchemeVector.SchemeVector.force_quotes

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.schemetools.SchemeVector.SchemeVector.quoting

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.schemetools.SchemeVector.SchemeVector.verbatim

Class & static methods
----------------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.SchemeVector.SchemeVector.format_embedded_scheme_value

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.SchemeVector.SchemeVector.format_scheme_value

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.SchemeVector.SchemeVector.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.SchemeVector.SchemeVector.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.SchemeVector.SchemeVector.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.SchemeVector.SchemeVector.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.SchemeVector.SchemeVector.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.SchemeVector.SchemeVector.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.schemetools.SchemeVector.SchemeVector.__str__
