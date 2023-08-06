.. currentmodule:: abjad.tools.abjadbooktools

ImageLayoutSpecifier
====================

.. autoclass:: ImageLayoutSpecifier

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
          subgraph cluster_abjadbooktools {
              graph [label=abjadbooktools];
              "abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>ImageLayoutSpecifier</B>>,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=3,
                  group=2,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier";
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

      ~abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.from_options
      ~abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.pages
      ~abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.with_columns
      ~abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.with_thumbnail
      ~abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.__copy__
      ~abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.__eq__
      ~abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.__format__
      ~abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.__hash__
      ~abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.__ne__
      ~abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.pages

.. autoattribute:: abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.with_columns

.. autoattribute:: abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.with_thumbnail

Class & static methods
----------------------

.. automethod:: abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.from_options

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ImageLayoutSpecifier.ImageLayoutSpecifier.__repr__
