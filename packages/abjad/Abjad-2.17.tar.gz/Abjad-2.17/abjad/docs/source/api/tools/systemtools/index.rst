systemtools
===========

.. automodule:: abjad.tools.systemtools

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
              "abjad.tools.abctools.ContextManager.ContextManager" [color=1,
                  group=0,
                  label=ContextManager,
                  shape=oval,
                  style=bold];
              "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.abctools.ContextManager.ContextManager";
              "abjad.tools.abctools.AbjadObject.AbstractBase" -> "abjad.tools.abctools.AbjadObject.AbjadObject";
          }
          subgraph cluster_systemtools {
              graph [label=systemtools];
              "abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration" [color=black,
                  fontcolor=white,
                  group=3,
                  label=AbjadConfiguration,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker" [color=black,
                  fontcolor=white,
                  group=3,
                  label=BenchmarkScoreMaker,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.Configuration.Configuration" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Configuration,
                  shape=oval,
                  style="filled, rounded"];
              "abjad.tools.systemtools.FilesystemState.FilesystemState" [color=black,
                  fontcolor=white,
                  group=3,
                  label=FilesystemState,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.ForbidUpdate.ForbidUpdate" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ForbidUpdate,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.IOManager.IOManager" [color=black,
                  fontcolor=white,
                  group=3,
                  label=IOManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.ImportManager.ImportManager" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ImportManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle" [color=black,
                  fontcolor=white,
                  group=3,
                  label=LilyPondFormatBundle,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager" [color=black,
                  fontcolor=white,
                  group=3,
                  label=LilyPondFormatManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.Memoize.Memoize" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Memoize,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.NullContextManager.NullContextManager" [color=black,
                  fontcolor=white,
                  group=3,
                  label=NullContextManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.ProgressIndicator.ProgressIndicator" [color=black,
                  fontcolor=white,
                  group=3,
                  label=ProgressIndicator,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.RedirectedStreams.RedirectedStreams" [color=black,
                  fontcolor=white,
                  group=3,
                  label=RedirectedStreams,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.StorageFormatManager.StorageFormatManager" [color=black,
                  fontcolor=white,
                  group=3,
                  label=StorageFormatManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification" [color=black,
                  fontcolor=white,
                  group=3,
                  label=StorageFormatSpecification,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.TemporaryDirectory.TemporaryDirectory" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TemporaryDirectory,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.TemporaryDirectoryChange.TemporaryDirectoryChange" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TemporaryDirectoryChange,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.TestManager.TestManager" [color=black,
                  fontcolor=white,
                  group=3,
                  label=TestManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.Timer.Timer" [color=black,
                  fontcolor=white,
                  group=3,
                  label=Timer,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.UpdateManager.UpdateManager" [color=black,
                  fontcolor=white,
                  group=3,
                  label=UpdateManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.WellformednessManager.WellformednessManager" [color=black,
                  fontcolor=white,
                  group=3,
                  label=WellformednessManager,
                  shape=box,
                  style="filled, rounded"];
              "abjad.tools.systemtools.Configuration.Configuration" -> "abjad.tools.systemtools.AbjadConfiguration.AbjadConfiguration";
          }
          subgraph cluster_builtins {
              graph [label=builtins];
              "builtins.dict" [color=2,
                  group=1,
                  label=dict,
                  shape=box];
              "builtins.object" [color=2,
                  group=1,
                  label=object,
                  shape=box];
              "builtins.object" -> "builtins.dict";
          }
          subgraph cluster_idetools {
              graph [label=idetools];
              "ide.tools.idetools.AbjadIDEConfiguration.AbjadIDEConfiguration" [color=3,
                  group=2,
                  label=AbjadIDEConfiguration,
                  shape=box];
              "ide.tools.idetools.IOManager.IOManager" [color=3,
                  group=2,
                  label=IOManager,
                  shape=box];
          }
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.BenchmarkScoreMaker.BenchmarkScoreMaker";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.Configuration.Configuration";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.IOManager.IOManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.ImportManager.ImportManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.LilyPondFormatBundle.LilyPondFormatBundle";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.LilyPondFormatManager.LilyPondFormatManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.StorageFormatManager.StorageFormatManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.StorageFormatSpecification.StorageFormatSpecification";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.TestManager.TestManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.UpdateManager.UpdateManager";
          "abjad.tools.abctools.AbjadObject.AbjadObject" -> "abjad.tools.systemtools.WellformednessManager.WellformednessManager";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.FilesystemState.FilesystemState";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.ForbidUpdate.ForbidUpdate";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.NullContextManager.NullContextManager";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.ProgressIndicator.ProgressIndicator";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.RedirectedStreams.RedirectedStreams";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.TemporaryDirectory.TemporaryDirectory";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.TemporaryDirectoryChange.TemporaryDirectoryChange";
          "abjad.tools.abctools.ContextManager.ContextManager" -> "abjad.tools.systemtools.Timer.Timer";
          "abjad.tools.systemtools.Configuration.Configuration" -> "ide.tools.idetools.AbjadIDEConfiguration.AbjadIDEConfiguration";
          "abjad.tools.systemtools.IOManager.IOManager" -> "ide.tools.idetools.IOManager.IOManager";
          "builtins.dict" -> "abjad.tools.systemtools.Memoize.Memoize";
          "builtins.object" -> "abjad.tools.abctools.AbjadObject.AbstractBase";
      }

--------

Benchmarking
------------

.. toctree::
   :hidden:

   BenchmarkScoreMaker

.. autosummary::
   :nosignatures:

   BenchmarkScoreMaker

--------

Context managers
----------------

.. toctree::
   :hidden:

   FilesystemState
   ForbidUpdate
   NullContextManager
   ProgressIndicator
   RedirectedStreams
   TemporaryDirectory
   TemporaryDirectoryChange
   Timer

.. autosummary::
   :nosignatures:

   FilesystemState
   ForbidUpdate
   NullContextManager
   ProgressIndicator
   RedirectedStreams
   TemporaryDirectory
   TemporaryDirectoryChange
   Timer

--------

Decorators
----------

.. toctree::
   :hidden:

   Memoize

.. autosummary::
   :nosignatures:

   Memoize

--------

LilyPond formatting
-------------------

.. toctree::
   :hidden:

   LilyPondFormatBundle
   LilyPondFormatManager

.. autosummary::
   :nosignatures:

   LilyPondFormatBundle
   LilyPondFormatManager

--------

Managers
--------

.. toctree::
   :hidden:

   IOManager
   ImportManager
   TestManager
   UpdateManager
   WellformednessManager

.. autosummary::
   :nosignatures:

   IOManager
   ImportManager
   TestManager
   UpdateManager
   WellformednessManager

--------

Storage formatting
------------------

.. toctree::
   :hidden:

   StorageFormatManager
   StorageFormatSpecification

.. autosummary::
   :nosignatures:

   StorageFormatManager
   StorageFormatSpecification

--------

System configuration
--------------------

.. toctree::
   :hidden:

   AbjadConfiguration
   Configuration

.. autosummary::
   :nosignatures:

   AbjadConfiguration
   Configuration
