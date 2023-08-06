.. currentmodule:: abjad.tools.instrumenttools

Performer
=========

.. autoclass:: Performer

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
              "abjad.tools.instrumenttools.Performer.Performer" [color=black,
                  fontcolor=white,
                  group=2,
                  label=<<B>Performer</B>>,
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
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.instrumenttools.Performer.Performer";
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

      ~abjad.tools.instrumenttools.Performer.Performer.get_instrument
      ~abjad.tools.instrumenttools.Performer.Performer.instrument_count
      ~abjad.tools.instrumenttools.Performer.Performer.instruments
      ~abjad.tools.instrumenttools.Performer.Performer.is_doubling
      ~abjad.tools.instrumenttools.Performer.Performer.likely_instruments_based_on_performer_name
      ~abjad.tools.instrumenttools.Performer.Performer.list_performer_names
      ~abjad.tools.instrumenttools.Performer.Performer.list_primary_performer_names
      ~abjad.tools.instrumenttools.Performer.Performer.make_performer_name_instrument_dictionary
      ~abjad.tools.instrumenttools.Performer.Performer.most_likely_instrument_based_on_performer_name
      ~abjad.tools.instrumenttools.Performer.Performer.name
      ~abjad.tools.instrumenttools.Performer.Performer.__eq__
      ~abjad.tools.instrumenttools.Performer.Performer.__format__
      ~abjad.tools.instrumenttools.Performer.Performer.__hash__
      ~abjad.tools.instrumenttools.Performer.Performer.__ne__
      ~abjad.tools.instrumenttools.Performer.Performer.__repr__

Read-only properties
--------------------

.. autoattribute:: abjad.tools.instrumenttools.Performer.Performer.instrument_count

.. autoattribute:: abjad.tools.instrumenttools.Performer.Performer.is_doubling

.. autoattribute:: abjad.tools.instrumenttools.Performer.Performer.likely_instruments_based_on_performer_name

.. autoattribute:: abjad.tools.instrumenttools.Performer.Performer.most_likely_instrument_based_on_performer_name

Read/write properties
---------------------

.. autoattribute:: abjad.tools.instrumenttools.Performer.Performer.instruments

.. autoattribute:: abjad.tools.instrumenttools.Performer.Performer.name

Methods
-------

.. automethod:: abjad.tools.instrumenttools.Performer.Performer.get_instrument

Class & static methods
----------------------

.. automethod:: abjad.tools.instrumenttools.Performer.Performer.list_performer_names

.. automethod:: abjad.tools.instrumenttools.Performer.Performer.list_primary_performer_names

.. automethod:: abjad.tools.instrumenttools.Performer.Performer.make_performer_name_instrument_dictionary

Special methods
---------------

.. automethod:: abjad.tools.instrumenttools.Performer.Performer.__eq__

.. automethod:: abjad.tools.instrumenttools.Performer.Performer.__format__

.. automethod:: abjad.tools.instrumenttools.Performer.Performer.__hash__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.Performer.Performer.__ne__

.. only:: html

   .. container:: inherited

      .. automethod:: abjad.tools.instrumenttools.Performer.Performer.__repr__
