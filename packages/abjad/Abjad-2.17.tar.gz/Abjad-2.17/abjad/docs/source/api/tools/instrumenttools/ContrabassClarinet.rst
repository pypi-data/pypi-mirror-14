.. currentmodule:: abjad.tools.instrumenttools

ContrabassClarinet
==================

.. autoclass:: ContrabassClarinet

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
              "abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>ContrabassClarinet</B>>,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Instrument.Instrument" [color=3,
                  group=2,
                  label=Instrument,
                  shape=box];
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet";
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

      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.allowable_clefs
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.instrument_name
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.instrument_name_markup
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.pitch_range
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.short_instrument_name
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.short_instrument_name_markup
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.sounding_pitch_of_written_middle_c
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.transpose_from_sounding_pitch_to_written_pitch
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.transpose_from_written_pitch_to_sounding_pitch
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.__copy__
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.__eq__
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.__format__
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.__hash__
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.__ne__
      ~abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.allowable_clefs

.. autoattribute:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.instrument_name

.. autoattribute:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.instrument_name_markup

.. autoattribute:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.pitch_range

.. autoattribute:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.short_instrument_name

.. autoattribute:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.short_instrument_name_markup

.. autoattribute:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.sounding_pitch_of_written_middle_c

Methods
-------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.transpose_from_sounding_pitch_to_written_pitch

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.transpose_from_written_pitch_to_sounding_pitch

Special methods
---------------

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.__copy__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.__eq__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.__format__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet.__repr__
