.. currentmodule:: abjad.tools.scoretools

DrumNoteHead
============

.. autoclass:: DrumNoteHead

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
              "abjad.tools.scoretools.DrumNoteHead.DrumNoteHead" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>DrumNoteHead</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.scoretools.NoteHead.NoteHead" [color=3,
                  group=2,
                  label=NoteHead,
                  shape=box];
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

- :py:class:`abjad.tools.scoretools.NoteHead`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.client
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.is_cautionary
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.is_forced
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.is_parenthesized
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.named_pitch
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.tweak
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.written_pitch
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__copy__
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__eq__
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__format__
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__ge__
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__gt__
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__hash__
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__le__
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__lt__
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__ne__
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__repr__
      ~abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__str__

Read-only properties
--------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.client

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.named_pitch

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.tweak

Read/write properties
---------------------

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.is_cautionary

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.is_forced

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.is_parenthesized

.. only:: html

   .. container:: inherited

      .. autoattribute:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.written_pitch

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__ge__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__gt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__le__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__lt__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__repr__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.scoretools.DrumNoteHead.DrumNoteHead.__str__
