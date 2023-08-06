exceptiontools
==============

.. automodule:: abjad.tools.exceptiontools

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
          subgraph cluster_exceptiontools {
              graph [label=exceptiontools];
              "abjad.tools.exceptiontools.AssignabilityError.AssignabilityError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=AssignabilityError,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.exceptiontools.ExtraSpannerError.ExtraSpannerError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=ExtraSpannerError,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.exceptiontools.ImpreciseTempoError.ImpreciseTempoError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=ImpreciseTempoError,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=LilyPondParserError,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.exceptiontools.MissingMeasureError.MissingMeasureError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=MissingMeasureError,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=MissingSpannerError,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.exceptiontools.MissingTempoError.MissingTempoError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=MissingTempoError,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.exceptiontools.OverfullContainerError.OverfullContainerError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=OverfullContainerError,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.exceptiontools.ParentageError.ParentageError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=ParentageError,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.exceptiontools.SchemeParserFinishedError.SchemeParserFinishedError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=SchemeParserFinishedError,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.exceptiontools.UnboundedTimeIntervalError.UnboundedTimeIntervalError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=UnboundedTimeIntervalError,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=UnderfullContainerError,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.exceptiontools.WellformednessError.WellformednessError" [color=black,
                  fontcolor=white,
                  group=1,
                  label=WellformednessError,
                  shape=box,
                  style="filled, rounded"];
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.BaseException" [color=1,
                  group=0,
                  label=BaseException,
                  shape=box];
              "builtins.Exception" [color=1,
                  group=0,
                  label=Exception,
                  shape=box];
              "builtins.object" [color=1,
                  group=0,
                  label=object,
                  shape=box];
              "builtins.BaseException" -> "builtins.Exception";
              "builtins.object" -> "builtins.BaseException";
          }
          "builtins.Exception" -> "abjad.tools.exceptiontools.AssignabilityError.AssignabilityError";
          "builtins.Exception" -> "abjad.tools.exceptiontools.ExtraSpannerError.ExtraSpannerError";
          "builtins.Exception" -> "abjad.tools.exceptiontools.ImpreciseTempoError.ImpreciseTempoError";
          "builtins.Exception" -> "abjad.tools.exceptiontools.LilyPondParserError.LilyPondParserError";
          "builtins.Exception" -> "abjad.tools.exceptiontools.MissingMeasureError.MissingMeasureError";
          "builtins.Exception" -> "abjad.tools.exceptiontools.MissingSpannerError.MissingSpannerError";
          "builtins.Exception" -> "abjad.tools.exceptiontools.MissingTempoError.MissingTempoError";
          "builtins.Exception" -> "abjad.tools.exceptiontools.OverfullContainerError.OverfullContainerError";
          "builtins.Exception" -> "abjad.tools.exceptiontools.ParentageError.ParentageError";
          "builtins.Exception" -> "abjad.tools.exceptiontools.SchemeParserFinishedError.SchemeParserFinishedError";
          "builtins.Exception" -> "abjad.tools.exceptiontools.UnboundedTimeIntervalError.UnboundedTimeIntervalError";
          "builtins.Exception" -> "abjad.tools.exceptiontools.UnderfullContainerError.UnderfullContainerError";
          "builtins.Exception" -> "abjad.tools.exceptiontools.WellformednessError.WellformednessError";
      }

--------

Errors
------

.. toctree::
   :hidden:

   AssignabilityError
   ExtraSpannerError
   ImpreciseTempoError
   LilyPondParserError
   MissingMeasureError
   MissingSpannerError
   MissingTempoError
   OverfullContainerError
   ParentageError
   SchemeParserFinishedError
   UnboundedTimeIntervalError
   UnderfullContainerError
   WellformednessError

.. autosummary::
   :nosignatures:

   AssignabilityError
   ExtraSpannerError
   ImpreciseTempoError
   LilyPondParserError
   MissingMeasureError
   MissingSpannerError
   MissingTempoError
   OverfullContainerError
   ParentageError
   SchemeParserFinishedError
   UnboundedTimeIntervalError
   UnderfullContainerError
   WellformednessError
