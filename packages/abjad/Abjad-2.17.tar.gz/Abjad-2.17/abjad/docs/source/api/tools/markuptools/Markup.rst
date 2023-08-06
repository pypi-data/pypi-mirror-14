.. currentmodule:: abjad.tools.markuptools

Markup
======

.. autoclass:: Markup

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
              "abjad.tools.markuptools.Markup.Markup" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Markup</B>>,
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
          "abjad.tools.abctools.AbjadValueObject.AbjadValueObject" -> "abjad.tools.markuptools.Markup.Markup";
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

      ~abjad.tools.markuptools.Markup.Markup.bold
      ~abjad.tools.markuptools.Markup.Markup.box
      ~abjad.tools.markuptools.Markup.Markup.caps
      ~abjad.tools.markuptools.Markup.Markup.center_align
      ~abjad.tools.markuptools.Markup.Markup.center_column
      ~abjad.tools.markuptools.Markup.Markup.circle
      ~abjad.tools.markuptools.Markup.Markup.column
      ~abjad.tools.markuptools.Markup.Markup.combine
      ~abjad.tools.markuptools.Markup.Markup.concat
      ~abjad.tools.markuptools.Markup.Markup.contents
      ~abjad.tools.markuptools.Markup.Markup.direction
      ~abjad.tools.markuptools.Markup.Markup.draw_line
      ~abjad.tools.markuptools.Markup.Markup.dynamic
      ~abjad.tools.markuptools.Markup.Markup.filled_box
      ~abjad.tools.markuptools.Markup.Markup.finger
      ~abjad.tools.markuptools.Markup.Markup.flat
      ~abjad.tools.markuptools.Markup.Markup.fontsize
      ~abjad.tools.markuptools.Markup.Markup.fraction
      ~abjad.tools.markuptools.Markup.Markup.general_align
      ~abjad.tools.markuptools.Markup.Markup.halign
      ~abjad.tools.markuptools.Markup.Markup.hcenter_in
      ~abjad.tools.markuptools.Markup.Markup.hspace
      ~abjad.tools.markuptools.Markup.Markup.huge
      ~abjad.tools.markuptools.Markup.Markup.italic
      ~abjad.tools.markuptools.Markup.Markup.larger
      ~abjad.tools.markuptools.Markup.Markup.left_column
      ~abjad.tools.markuptools.Markup.Markup.line
      ~abjad.tools.markuptools.Markup.Markup.make_big_centered_page_number_markup
      ~abjad.tools.markuptools.Markup.Markup.make_blank_line_markup
      ~abjad.tools.markuptools.Markup.Markup.make_centered_title_markup
      ~abjad.tools.markuptools.Markup.Markup.make_improper_fraction_markup
      ~abjad.tools.markuptools.Markup.Markup.make_vertically_adjusted_composer_markup
      ~abjad.tools.markuptools.Markup.Markup.musicglyph
      ~abjad.tools.markuptools.Markup.Markup.natural
      ~abjad.tools.markuptools.Markup.Markup.note_by_number
      ~abjad.tools.markuptools.Markup.Markup.null
      ~abjad.tools.markuptools.Markup.Markup.override
      ~abjad.tools.markuptools.Markup.Markup.pad_around
      ~abjad.tools.markuptools.Markup.Markup.pad_to_box
      ~abjad.tools.markuptools.Markup.Markup.parenthesize
      ~abjad.tools.markuptools.Markup.Markup.postscript
      ~abjad.tools.markuptools.Markup.Markup.raise_
      ~abjad.tools.markuptools.Markup.Markup.right_column
      ~abjad.tools.markuptools.Markup.Markup.rotate
      ~abjad.tools.markuptools.Markup.Markup.sans
      ~abjad.tools.markuptools.Markup.Markup.scale
      ~abjad.tools.markuptools.Markup.Markup.sharp
      ~abjad.tools.markuptools.Markup.Markup.small
      ~abjad.tools.markuptools.Markup.Markup.smaller
      ~abjad.tools.markuptools.Markup.Markup.stack_priority
      ~abjad.tools.markuptools.Markup.Markup.tiny
      ~abjad.tools.markuptools.Markup.Markup.translate
      ~abjad.tools.markuptools.Markup.Markup.triangle
      ~abjad.tools.markuptools.Markup.Markup.upright
      ~abjad.tools.markuptools.Markup.Markup.vcenter
      ~abjad.tools.markuptools.Markup.Markup.vspace
      ~abjad.tools.markuptools.Markup.Markup.whiteout
      ~abjad.tools.markuptools.Markup.Markup.with_color
      ~abjad.tools.markuptools.Markup.Markup.with_dimensions
      ~abjad.tools.markuptools.Markup.Markup.__add__
      ~abjad.tools.markuptools.Markup.Markup.__copy__
      ~abjad.tools.markuptools.Markup.Markup.__eq__
      ~abjad.tools.markuptools.Markup.Markup.__format__
      ~abjad.tools.markuptools.Markup.Markup.__hash__
      ~abjad.tools.markuptools.Markup.Markup.__illustrate__
      ~abjad.tools.markuptools.Markup.Markup.__ne__
      ~abjad.tools.markuptools.Markup.Markup.__repr__
      ~abjad.tools.markuptools.Markup.Markup.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.markuptools.Markup.Markup.contents

.. autoattribute:: abjad.tools.markuptools.Markup.Markup.direction

.. autoattribute:: abjad.tools.markuptools.Markup.Markup.stack_priority

Methods
-------

.. automethod:: abjad.tools.markuptools.Markup.Markup.bold

.. automethod:: abjad.tools.markuptools.Markup.Markup.box

.. automethod:: abjad.tools.markuptools.Markup.Markup.caps

.. automethod:: abjad.tools.markuptools.Markup.Markup.center_align

.. automethod:: abjad.tools.markuptools.Markup.Markup.circle

.. automethod:: abjad.tools.markuptools.Markup.Markup.dynamic

.. automethod:: abjad.tools.markuptools.Markup.Markup.finger

.. automethod:: abjad.tools.markuptools.Markup.Markup.fontsize

.. automethod:: abjad.tools.markuptools.Markup.Markup.general_align

.. automethod:: abjad.tools.markuptools.Markup.Markup.halign

.. automethod:: abjad.tools.markuptools.Markup.Markup.hcenter_in

.. automethod:: abjad.tools.markuptools.Markup.Markup.huge

.. automethod:: abjad.tools.markuptools.Markup.Markup.italic

.. automethod:: abjad.tools.markuptools.Markup.Markup.larger

.. automethod:: abjad.tools.markuptools.Markup.Markup.line

.. automethod:: abjad.tools.markuptools.Markup.Markup.override

.. automethod:: abjad.tools.markuptools.Markup.Markup.pad_around

.. automethod:: abjad.tools.markuptools.Markup.Markup.pad_to_box

.. automethod:: abjad.tools.markuptools.Markup.Markup.parenthesize

.. automethod:: abjad.tools.markuptools.Markup.Markup.raise_

.. automethod:: abjad.tools.markuptools.Markup.Markup.rotate

.. automethod:: abjad.tools.markuptools.Markup.Markup.sans

.. automethod:: abjad.tools.markuptools.Markup.Markup.scale

.. automethod:: abjad.tools.markuptools.Markup.Markup.small

.. automethod:: abjad.tools.markuptools.Markup.Markup.smaller

.. automethod:: abjad.tools.markuptools.Markup.Markup.tiny

.. automethod:: abjad.tools.markuptools.Markup.Markup.translate

.. automethod:: abjad.tools.markuptools.Markup.Markup.upright

.. automethod:: abjad.tools.markuptools.Markup.Markup.vcenter

.. automethod:: abjad.tools.markuptools.Markup.Markup.whiteout

.. automethod:: abjad.tools.markuptools.Markup.Markup.with_color

.. automethod:: abjad.tools.markuptools.Markup.Markup.with_dimensions

Class & static methods
----------------------

.. automethod:: abjad.tools.markuptools.Markup.Markup.center_column

.. automethod:: abjad.tools.markuptools.Markup.Markup.column

.. automethod:: abjad.tools.markuptools.Markup.Markup.combine

.. automethod:: abjad.tools.markuptools.Markup.Markup.concat

.. automethod:: abjad.tools.markuptools.Markup.Markup.draw_line

.. automethod:: abjad.tools.markuptools.Markup.Markup.filled_box

.. automethod:: abjad.tools.markuptools.Markup.Markup.flat

.. automethod:: abjad.tools.markuptools.Markup.Markup.fraction

.. automethod:: abjad.tools.markuptools.Markup.Markup.hspace

.. automethod:: abjad.tools.markuptools.Markup.Markup.left_column

.. automethod:: abjad.tools.markuptools.Markup.Markup.make_big_centered_page_number_markup

.. automethod:: abjad.tools.markuptools.Markup.Markup.make_blank_line_markup

.. automethod:: abjad.tools.markuptools.Markup.Markup.make_centered_title_markup

.. automethod:: abjad.tools.markuptools.Markup.Markup.make_improper_fraction_markup

.. automethod:: abjad.tools.markuptools.Markup.Markup.make_vertically_adjusted_composer_markup

.. automethod:: abjad.tools.markuptools.Markup.Markup.musicglyph

.. automethod:: abjad.tools.markuptools.Markup.Markup.natural

.. automethod:: abjad.tools.markuptools.Markup.Markup.note_by_number

.. automethod:: abjad.tools.markuptools.Markup.Markup.null

.. automethod:: abjad.tools.markuptools.Markup.Markup.postscript

.. automethod:: abjad.tools.markuptools.Markup.Markup.right_column

.. automethod:: abjad.tools.markuptools.Markup.Markup.sharp

.. automethod:: abjad.tools.markuptools.Markup.Markup.triangle

.. automethod:: abjad.tools.markuptools.Markup.Markup.vspace

Special methods
---------------

.. automethod:: abjad.tools.markuptools.Markup.Markup.__add__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.Markup.Markup.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.Markup.Markup.__eq__

.. automethod:: abjad.tools.markuptools.Markup.Markup.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.Markup.Markup.__hash__

.. automethod:: abjad.tools.markuptools.Markup.Markup.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.Markup.Markup.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.markuptools.Markup.Markup.__repr__

.. automethod:: abjad.tools.markuptools.Markup.Markup.__str__
