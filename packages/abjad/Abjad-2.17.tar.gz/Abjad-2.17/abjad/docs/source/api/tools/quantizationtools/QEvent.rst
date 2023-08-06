.. currentmodule:: abjad.tools.quantizationtools

QEvent
======

.. autoclass:: QEvent

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
              "abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent" [color=3,
                  group=2,
                  label=PitchedQEvent,
                  shape=box];
              "abjad.tools.quantizationtools.QEvent.QEvent" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>QEvent</B>>,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.quantizationtools.SilentQEvent.SilentQEvent" [color=3,
                  group=2,
                  label=SilentQEvent,
                  shape=box];
              "abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent" [color=3,
                  group=2,
                  label=TerminalQEvent,
                  shape=box];
              "abjad.tools.quantizationtools.QEvent.QEvent" -> "abjad.tools.quantizationtools.PitchedQEvent.PitchedQEvent";
              "abjad.tools.quantizationtools.QEvent.QEvent" -> "abjad.tools.quantizationtools.SilentQEvent.SilentQEvent";
              "abjad.tools.quantizationtools.QEvent.QEvent" -> "abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent";
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

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.quantizationtools.QEvent.QEvent.index
      ~abjad.tools.quantizationtools.QEvent.QEvent.offset
      ~abjad.tools.quantizationtools.QEvent.QEvent.__eq__
      ~abjad.tools.quantizationtools.QEvent.QEvent.__format__
      ~abjad.tools.quantizationtools.QEvent.QEvent.__hash__
      ~abjad.tools.quantizationtools.QEvent.QEvent.__lt__
      ~abjad.tools.quantizationtools.QEvent.QEvent.__ne__
      ~abjad.tools.quantizationtools.QEvent.QEvent.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.quantizationtools.QEvent.QEvent.index

.. autoattribute:: abjad.tools.quantizationtools.QEvent.QEvent.offset

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QEvent.QEvent.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QEvent.QEvent.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QEvent.QEvent.__hash__

.. automethod:: abjad.tools.quantizationtools.QEvent.QEvent.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QEvent.QEvent.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.QEvent.QEvent.__repr__
