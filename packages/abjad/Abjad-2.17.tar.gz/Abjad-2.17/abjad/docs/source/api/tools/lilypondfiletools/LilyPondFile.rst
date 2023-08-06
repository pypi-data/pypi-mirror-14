.. currentmodule:: abjad.tools.lilypondfiletools

LilyPondFile
============

.. autoclass:: LilyPondFile

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
          subgraph cluster_lilypondfiletools {
              graph [label=lilypondfiletools];
              "abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>LilyPondFile</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile";
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

      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.comments
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.date_time_token
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.default_paper_size
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.global_staff_size
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.header_block
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.includes
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.items
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.layout_block
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.lilypond_language_token
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.lilypond_version_token
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.paper_block
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.score_block
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.use_relative_includes
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__eq__
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__format__
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__getitem__
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__hash__
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__illustrate__
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__ne__
      ~abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.comments

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.date_time_token

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.default_paper_size

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.global_staff_size

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.header_block

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.includes

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.items

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.layout_block

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.lilypond_language_token

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.lilypond_version_token

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.paper_block

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.score_block

.. autoattribute:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.use_relative_includes

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__eq__

.. automethod:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__format__

.. automethod:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__getitem__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__hash__

.. automethod:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__illustrate__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__ne__

.. automethod:: abjad.tools.lilypondfiletools.LilyPondFile.LilyPondFile.__repr__
