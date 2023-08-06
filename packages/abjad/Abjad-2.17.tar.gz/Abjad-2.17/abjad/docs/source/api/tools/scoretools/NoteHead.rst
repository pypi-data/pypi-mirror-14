.. currentmodule:: abjad.tools.scoretools

NoteHead
========

.. autoclass:: NoteHead

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
          subgraph cluster_scoretools {
              graph [label=scoretools];
              "abjad.tools.scoretools.DrumNoteHead.DrumNoteHead" [color=3,
                  group=2,
                  label=DrumNoteHead,
                  shape=box];
              "abjad.tools.scoretools.NoteHead.NoteHead" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>NoteHead</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.NoteHead.NoteHead" -> "abjad.tools.scoretools.DrumNoteHead.DrumNoteHead";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.scoretools.NoteHead.NoteHead";
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

      ~abjad.tools.scoretools.NoteHead.NoteHead.client
      ~abjad.tools.scoretools.NoteHead.NoteHead.is_cautionary
      ~abjad.tools.scoretools.NoteHead.NoteHead.is_forced
      ~abjad.tools.scoretools.NoteHead.NoteHead.is_parenthesized
      ~abjad.tools.scoretools.NoteHead.NoteHead.named_pitch
      ~abjad.tools.scoretools.NoteHead.NoteHead.tweak
      ~abjad.tools.scoretools.NoteHead.NoteHead.written_pitch
      ~abjad.tools.scoretools.NoteHead.NoteHead.__copy__
      ~abjad.tools.scoretools.NoteHead.NoteHead.__eq__
      ~abjad.tools.scoretools.NoteHead.NoteHead.__format__
      ~abjad.tools.scoretools.NoteHead.NoteHead.__ge__
      ~abjad.tools.scoretools.NoteHead.NoteHead.__gt__
      ~abjad.tools.scoretools.NoteHead.NoteHead.__hash__
      ~abjad.tools.scoretools.NoteHead.NoteHead.__le__
      ~abjad.tools.scoretools.NoteHead.NoteHead.__lt__
      ~abjad.tools.scoretools.NoteHead.NoteHead.__ne__
      ~abjad.tools.scoretools.NoteHead.NoteHead.__repr__
      ~abjad.tools.scoretools.NoteHead.NoteHead.__str__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.scoretools.NoteHead.NoteHead.client

.. autoattribute:: abjad.tools.scoretools.NoteHead.NoteHead.named_pitch

.. autoattribute:: abjad.tools.scoretools.NoteHead.NoteHead.tweak

Read/write properties
---------------------

.. autoattribute:: abjad.tools.scoretools.NoteHead.NoteHead.is_cautionary

.. autoattribute:: abjad.tools.scoretools.NoteHead.NoteHead.is_forced

.. autoattribute:: abjad.tools.scoretools.NoteHead.NoteHead.is_parenthesized

.. autoattribute:: abjad.tools.scoretools.NoteHead.NoteHead.written_pitch

Special methods
---------------

.. automethod:: abjad.tools.scoretools.NoteHead.NoteHead.__copy__

.. automethod:: abjad.tools.scoretools.NoteHead.NoteHead.__eq__

.. automethod:: abjad.tools.scoretools.NoteHead.NoteHead.__format__

.. automethod:: abjad.tools.scoretools.NoteHead.NoteHead.__ge__

.. automethod:: abjad.tools.scoretools.NoteHead.NoteHead.__gt__

.. automethod:: abjad.tools.scoretools.NoteHead.NoteHead.__hash__

.. automethod:: abjad.tools.scoretools.NoteHead.NoteHead.__le__

.. automethod:: abjad.tools.scoretools.NoteHead.NoteHead.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.NoteHead.NoteHead.__ne__

.. automethod:: abjad.tools.scoretools.NoteHead.NoteHead.__repr__

.. automethod:: abjad.tools.scoretools.NoteHead.NoteHead.__str__
