.. currentmodule:: abjad.tools.quantizationtools

TerminalQEvent
==============

.. autoclass:: TerminalQEvent

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
              "abjad.tools.quantizationtools.QEvent.QEvent" [color=3,
                  group=2,
                  label=QEvent,
                  shape=oval,
                  style=bold];
              "abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TerminalQEvent</B>>,
                  shape=box,
                  style="filled, rounded"];
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

- :py:class:`abjad.tools.quantizationtools.QEvent`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.index
      ~abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.offset
      ~abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.__eq__
      ~abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.__format__
      ~abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.__hash__
      ~abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.__lt__
      ~abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.__ne__
      ~abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.__repr__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.index

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.offset

Special methods
---------------

.. automethod:: abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.__format__

.. automethod:: abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.quantizationtools.TerminalQEvent.TerminalQEvent.__repr__
