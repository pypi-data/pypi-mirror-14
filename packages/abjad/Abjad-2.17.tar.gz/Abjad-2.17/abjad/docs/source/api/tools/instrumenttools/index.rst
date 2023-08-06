instrumenttools
===============

.. automodule:: abjad.tools.instrumenttools

--------

Lineage
-------

.. container:: graphviz

   .. graphviz::

      digraph InheritanceGraph {
          graph [bgcolor=transparent,
              color=lightslategrey,
              dpi=72,
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
          subgraph cluster_datastructuretools {
              graph [label=datastructuretools];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" [color=3,
                  group=2,
                  label=TypedCollection,
                  shape=oval,
                  style=bold];
              "abjad.tools.datastructuretools.TypedList.TypedList" [color=3,
                  group=2,
                  label=TypedList,
                  shape=box];
              "abjad.tools.datastructuretools.TypedCollection.TypedCollection" -> "abjad.tools.datastructuretools.TypedList.TypedList";
          }
          subgraph cluster_instrumenttools {
              graph [label=instrumenttools];
              "abjad.tools.instrumenttools.Accordion.Accordion" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Accordion,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.AltoFlute.AltoFlute" [color=black,
                  fontcolor=white,
                  group=3,
                  label=AltoFlute,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.AltoSaxophone.AltoSaxophone" [color=black,
                  fontcolor=white,
                  group=3,
                  label=AltoSaxophone,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.AltoTrombone.AltoTrombone" [color=black,
                  fontcolor=white,
                  group=3,
                  label=AltoTrombone,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.AltoVoice.AltoVoice" [color=black,
                  fontcolor=white,
                  group=3,
                  label=AltoVoice,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.BaritoneSaxophone.BaritoneSaxophone" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BaritoneSaxophone,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.BaritoneVoice.BaritoneVoice" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BaritoneVoice,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.BassClarinet.BassClarinet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BassClarinet,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.BassFlute.BassFlute" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BassFlute,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.BassSaxophone.BassSaxophone" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BassSaxophone,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.BassTrombone.BassTrombone" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BassTrombone,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.BassVoice.BassVoice" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BassVoice,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Bassoon.Bassoon" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Bassoon,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Cello.Cello" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Cello,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.ClarinetInA.ClarinetInA" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ClarinetInA,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.ClarinetInBFlat.ClarinetInBFlat" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ClarinetInBFlat,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.ClarinetInEFlat.ClarinetInEFlat" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ClarinetInEFlat,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Contrabass.Contrabass" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Contrabass,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ContrabassClarinet,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.ContrabassFlute.ContrabassFlute" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ContrabassFlute,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.ContrabassSaxophone.ContrabassSaxophone" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ContrabassSaxophone,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Contrabassoon.Contrabassoon" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Contrabassoon,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.EnglishHorn.EnglishHorn" [color=black,
                  fontcolor=white,
                  group=3,
                  label=EnglishHorn,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Flute.Flute" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Flute,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.FrenchHorn.FrenchHorn" [color=black,
                  fontcolor=white,
                  group=3,
                  label=FrenchHorn,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Glockenspiel.Glockenspiel" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Glockenspiel,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Guitar.Guitar" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Guitar,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Harp.Harp" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Harp,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Harpsichord.Harpsichord" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Harpsichord,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Instrument.Instrument" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Instrument,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=InstrumentInventory,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Marimba.Marimba" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Marimba,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice" [color=black,
                  fontcolor=white,
                  group=3,
                  label=MezzoSopranoVoice,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Oboe.Oboe" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Oboe,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Percussion.Percussion" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Percussion,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Performer.Performer" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Performer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.PerformerInventory.PerformerInventory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=PerformerInventory,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Piano.Piano" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Piano,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Piccolo.Piccolo" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Piccolo,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.SopraninoSaxophone.SopraninoSaxophone" [color=black,
                  fontcolor=white,
                  group=3,
                  label=SopraninoSaxophone,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.SopranoSaxophone.SopranoSaxophone" [color=black,
                  fontcolor=white,
                  group=3,
                  label=SopranoSaxophone,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.SopranoVoice.SopranoVoice" [color=black,
                  fontcolor=white,
                  group=3,
                  label=SopranoVoice,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.TenorSaxophone.TenorSaxophone" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TenorSaxophone,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.TenorTrombone.TenorTrombone" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TenorTrombone,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.TenorVoice.TenorVoice" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TenorVoice,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Trumpet.Trumpet" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Trumpet,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Tuba.Tuba" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Tuba,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Vibraphone.Vibraphone" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Vibraphone,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Viola.Viola" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Viola,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Violin.Violin" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Violin,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.WoodwindFingering.WoodwindFingering" [color=black,
                  fontcolor=white,
                  group=3,
                  label=WoodwindFingering,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Xylophone.Xylophone" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Xylophone,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Accordion.Accordion";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.AltoFlute.AltoFlute";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.AltoSaxophone.AltoSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.AltoTrombone.AltoTrombone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.AltoVoice.AltoVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BaritoneSaxophone.BaritoneSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BaritoneVoice.BaritoneVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassClarinet.BassClarinet";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassFlute.BassFlute";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassSaxophone.BassSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassTrombone.BassTrombone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.BassVoice.BassVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Bassoon.Bassoon";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Cello.Cello";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ClarinetInA.ClarinetInA";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ClarinetInBFlat.ClarinetInBFlat";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ClarinetInEFlat.ClarinetInEFlat";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Contrabass.Contrabass";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ContrabassClarinet.ContrabassClarinet";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ContrabassFlute.ContrabassFlute";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.ContrabassSaxophone.ContrabassSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Contrabassoon.Contrabassoon";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.EnglishHorn.EnglishHorn";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Flute.Flute";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.FrenchHorn.FrenchHorn";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Glockenspiel.Glockenspiel";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Guitar.Guitar";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Harp.Harp";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Harpsichord.Harpsichord";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Marimba.Marimba";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.MezzoSopranoVoice.MezzoSopranoVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Oboe.Oboe";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Percussion.Percussion";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Piano.Piano";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Piccolo.Piccolo";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.SopraninoSaxophone.SopraninoSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.SopranoSaxophone.SopranoSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.SopranoVoice.SopranoVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.TenorSaxophone.TenorSaxophone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.TenorTrombone.TenorTrombone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.TenorVoice.TenorVoice";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Trumpet.Trumpet";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Tuba.Tuba";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Vibraphone.Vibraphone";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Viola.Viola";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Violin.Violin";
              "abjad.tools.instrumenttools.Instrument.Instrument" -> "abjad.tools.instrumenttools.Xylophone.Xylophone";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.datastructuretools.TypedCollection.TypedCollection";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.instrumenttools.Instrument.Instrument";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.instrumenttools.Performer.Performer";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.instrumenttools.WoodwindFingering.WoodwindFingering";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.instrumenttools.InstrumentInventory.InstrumentInventory";
          "abjad.tools.datastructuretools.TypedList.TypedList" -> "abjad.tools.instrumenttools.PerformerInventory.PerformerInventory";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Classes
-------

.. toctree::
   :hidden:

   Accordion
   AltoFlute
   AltoSaxophone
   AltoTrombone
   AltoVoice
   BaritoneSaxophone
   BaritoneVoice
   BassClarinet
   BassFlute
   BassSaxophone
   BassTrombone
   BassVoice
   Bassoon
   Cello
   ClarinetInA
   ClarinetInBFlat
   ClarinetInEFlat
   Contrabass
   ContrabassClarinet
   ContrabassFlute
   ContrabassSaxophone
   Contrabassoon
   EnglishHorn
   Flute
   FrenchHorn
   Glockenspiel
   Guitar
   Harp
   Harpsichord
   Instrument
   InstrumentInventory
   Marimba
   MezzoSopranoVoice
   Oboe
   Percussion
   Performer
   PerformerInventory
   Piano
   Piccolo
   SopraninoSaxophone
   SopranoSaxophone
   SopranoVoice
   TenorSaxophone
   TenorTrombone
   TenorVoice
   Trumpet
   Tuba
   Vibraphone
   Viola
   Violin
   WoodwindFingering
   Xylophone

.. autosummary::
   :nosignatures:

   Accordion
   AltoFlute
   AltoSaxophone
   AltoTrombone
   AltoVoice
   BaritoneSaxophone
   BaritoneVoice
   BassClarinet
   BassFlute
   BassSaxophone
   BassTrombone
   BassVoice
   Bassoon
   Cello
   ClarinetInA
   ClarinetInBFlat
   ClarinetInEFlat
   Contrabass
   ContrabassClarinet
   ContrabassFlute
   ContrabassSaxophone
   Contrabassoon
   EnglishHorn
   Flute
   FrenchHorn
   Glockenspiel
   Guitar
   Harp
   Harpsichord
   Instrument
   InstrumentInventory
   Marimba
   MezzoSopranoVoice
   Oboe
   Percussion
   Performer
   PerformerInventory
   Piano
   Piccolo
   SopraninoSaxophone
   SopranoSaxophone
   SopranoVoice
   TenorSaxophone
   TenorTrombone
   TenorVoice
   Trumpet
   Tuba
   Vibraphone
   Viola
   Violin
   WoodwindFingering
   Xylophone

--------

Functions
---------

.. toctree::
   :hidden:

   iterate_out_of_range_notes_and_chords
   notes_and_chords_are_in_range
   notes_and_chords_are_on_expected_clefs
   transpose_from_sounding_pitch_to_written_pitch
   transpose_from_written_pitch_to_sounding_pitch

.. autosummary::
   :nosignatures:

   iterate_out_of_range_notes_and_chords
   notes_and_chords_are_in_range
   notes_and_chords_are_on_expected_clefs
   transpose_from_sounding_pitch_to_written_pitch
   transpose_from_written_pitch_to_sounding_pitch
