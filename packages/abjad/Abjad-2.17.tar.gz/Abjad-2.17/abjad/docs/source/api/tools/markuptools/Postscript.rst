.. currentmodule:: abjad.tools.markuptools

Postscript
==========

.. autoclass:: Postscript

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
          subgraph cluster_markuptools {
              graph [label=markuptools];
              "abjad.tools.markuptools.Postscript.Postscript" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Postscript</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.Postscript.Postscript";
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

      ~abjad.tools.markuptools.Postscript.Postscript.as_markup
      ~abjad.tools.markuptools.Postscript.Postscript.charpath
      ~abjad.tools.markuptools.Postscript.Postscript.closepath
      ~abjad.tools.markuptools.Postscript.Postscript.curveto
      ~abjad.tools.markuptools.Postscript.Postscript.fill
      ~abjad.tools.markuptools.Postscript.Postscript.findfont
      ~abjad.tools.markuptools.Postscript.Postscript.grestore
      ~abjad.tools.markuptools.Postscript.Postscript.gsave
      ~abjad.tools.markuptools.Postscript.Postscript.lineto
      ~abjad.tools.markuptools.Postscript.Postscript.moveto
      ~abjad.tools.markuptools.Postscript.Postscript.newpath
      ~abjad.tools.markuptools.Postscript.Postscript.operators
      ~abjad.tools.markuptools.Postscript.Postscript.rcurveto
      ~abjad.tools.markuptools.Postscript.Postscript.rlineto
      ~abjad.tools.markuptools.Postscript.Postscript.rmoveto
      ~abjad.tools.markuptools.Postscript.Postscript.rotate
      ~abjad.tools.markuptools.Postscript.Postscript.scale
      ~abjad.tools.markuptools.Postscript.Postscript.scalefont
      ~abjad.tools.markuptools.Postscript.Postscript.setdash
      ~abjad.tools.markuptools.Postscript.Postscript.setfont
      ~abjad.tools.markuptools.Postscript.Postscript.setgray
      ~abjad.tools.markuptools.Postscript.Postscript.setlinewidth
      ~abjad.tools.markuptools.Postscript.Postscript.setrgbcolor
      ~abjad.tools.markuptools.Postscript.Postscript.show
      ~abjad.tools.markuptools.Postscript.Postscript.stroke
      ~abjad.tools.markuptools.Postscript.Postscript.translate
      ~abjad.tools.markuptools.Postscript.Postscript.__add__
      ~abjad.tools.markuptools.Postscript.Postscript.__copy__
      ~abjad.tools.markuptools.Postscript.Postscript.__eq__
      ~abjad.tools.markuptools.Postscript.Postscript.__format__
      ~abjad.tools.markuptools.Postscript.Postscript.__hash__
      ~abjad.tools.markuptools.Postscript.Postscript.__illustrate__
      ~abjad.tools.markuptools.Postscript.Postscript.__ne__
      ~abjad.tools.markuptools.Postscript.Postscript.__repr__
      ~abjad.tools.markuptools.Postscript.Postscript.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.markuptools.Postscript.Postscript.operators

Methods
-------

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.as_markup

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.charpath

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.closepath

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.curveto

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.fill

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.findfont

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.grestore

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.gsave

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.lineto

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.moveto

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.newpath

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.rcurveto

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.rlineto

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.rmoveto

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.rotate

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.scale

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.scalefont

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.setdash

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.setfont

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.setgray

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.setlinewidth

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.setrgbcolor

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.show

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.stroke

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.translate

Special methods
---------------

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.Postscript.Postscript.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.Postscript.Postscript.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.Postscript.Postscript.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.Postscript.Postscript.__hash__

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.Postscript.Postscript.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.Postscript.Postscript.__repr__

.. automethod:: abjad.tools.markuptools.Postscript.Postscript.__str__
