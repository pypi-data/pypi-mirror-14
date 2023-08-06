.. currentmodule:: abjad.tools.quantizationtools

PitchedQEvent
=============

.. autoclass:: PitchedQEvent

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
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_quantizationtools {
              graph [label=quantizationtools];
              "abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>PitchedQEvent</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.QEvent.QEvent" [color=3,
                  group=2,
                  label=QEvent,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.QEvent.QEvent" -> "abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.quantizationtools.QEvent.QEvent";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.quantizationtools.QEvent`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.attachments
      ~abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.index
      ~abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.offset
      ~abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.pitches
      ~abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.__eq__
      ~abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.__format__
      ~abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.__hash__
      ~abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.__lt__
      ~abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.__ne__
      ~abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.attachments

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.index

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.offset

.. autoattribute:: abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.pitches

Special methods
---------------

.. automethod:: abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.__format__

.. automethod:: abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent.__repr__
