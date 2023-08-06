.. currentmodule:: abjad.tools.instrumenttools

TenorVoice
==========

.. autoclass:: TenorVoice

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
          subgraph cluster_instrumenttools {
              graph [label=instrumenttools];
              "abjad.tools.instrumenttools.Instrument.Instrument" [color=3,
                  group=2,
                  label=Instrument,
                  shape=box];
              "abjad.tools.instrumenttools.TenorVoice.TenorVoice" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>TenorVoice</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.TenorVoice.TenorVoice";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.instrumenttools.Instrument.Instrument";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

Bases
-----

- :py:class:`abjad.tools.instrumenttools.Instrument`

- :py:class:`abjad.tools.abctools.AbjadObject`

- :py:class:`abjad.tools.abctools.AbjadObject.AbstractBase`

- :py:class:`builtins.object`

.. only:: html

   Attribute summary
   -----------------

   .. autosummary::

      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.allowable_clefs
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.instrument_name
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.instrument_name_markup
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.pitch_range
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.short_instrument_name
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.short_instrument_name_markup
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.sounding_pitch_of_written_middle_c
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.transpose_from_sounding_pitch_to_written_pitch
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.transpose_from_written_pitch_to_sounding_pitch
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.__copy__
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.__eq__
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.__format__
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.__hash__
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.__ne__
      ~abjad.tools.instrumenttools.TenorVoice.TenorVoice.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.allowable_clefs

.. autoattribute:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.instrument_name

.. autoattribute:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.instrument_name_markup

.. autoattribute:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.pitch_range

.. autoattribute:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.short_instrument_name

.. autoattribute:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.short_instrument_name_markup

.. autoattribute:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.sounding_pitch_of_written_middle_c

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.transpose_from_sounding_pitch_to_written_pitch

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.transpose_from_written_pitch_to_sounding_pitch

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.TenorVoice.TenorVoice.__repr__
