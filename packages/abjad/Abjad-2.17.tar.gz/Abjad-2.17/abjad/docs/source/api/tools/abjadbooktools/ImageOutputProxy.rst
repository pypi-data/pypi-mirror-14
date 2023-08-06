.. currentmodule:: abjad.tools.abjadbooktools

ImageOutputProxy
================

.. autoclass:: ImageOutputProxy

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
              "abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy" [color=2,
                  group=1,
                  label=GraphvizOutputProxy,
                  shape=box];
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" [color=black,
                  fontcolor=white,
                  group=1,
                  label=<<B>ImageOutputProxy</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.abjadbooktools.LilyPondOutputProxy.LilyPondOutputProxy" [color=2,
                  group=1,
                  label=LilyPondOutputProxy,
                  shape=box];
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" -> "abjad.tools.abjadbooktools.GraphvizOutputProxy.GraphvizOutputProxy";
              "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy" -> "abjad.tools.abjadbooktools.LilyPondOutputProxy.LilyPondOutputProxy";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=3,
                  group=2,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy";
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

      ~abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.as_latex
      ~abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.file_name_prefix
      ~abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.file_name_without_extension
      ~abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.image_layout_specifier
      ~abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.image_render_specifier
      ~abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.payload
      ~abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.render_for_latex
      ~abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.__copy__
      ~abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.__eq__
      ~abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.__format__
      ~abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.__hash__
      ~abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.__ne__
      ~abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.file_name_prefix

.. autoattribute:: abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.file_name_without_extension

.. autoattribute:: abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.image_layout_specifier

.. autoattribute:: abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.image_render_specifier

.. autoattribute:: abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.payload

Methods
-------

.. automethod:: abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.as_latex

.. automethod:: abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.render_for_latex

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.abjadbooktools.ImageOutputProxy.ImageOutputProxy.__repr__
