#Galaxy Analysis Toolkit

A collection of scripts and analysis tools used in my thesis research.

This also includes the text and version history of two as yet unpublished papers
that were the primary research result of the code.

The code is split up into two main pieces. The `galanyl` "library" lives in the
`galanyl` directory, while `helper_scripts` contains a number of scripts that
make use of `yt` and `galanyl` to process simulation data.

#Using these scripts

First, you must download the data you would like to analyze. Right now the
helper scripts are written in a such a way that they expect the full simulation
dataset to be present, but they should be easily modifiable or adaptable if you
only want to look at one or a few simulation outputs.

The data for Paper I are available at https://hub.yt/data/goldbaum2015a/

The data for Paper II are available at https://hub.yt/data/goldbaum2016a

##Generating uniform resolution grid slabs

Note: you can skip this step if you want to download the processed data. This
is only necessary if you would like to generate the processed data from the
raw simulation outputs.

For example, if you would like to regenerate the processed data for the
``nofeedback_20pc`` simulation, you will need to download one or more of
the simulation outputs, unzip the tarball, and place the simulation outputs
in a directory named ``nofeedback_20pc``.

Once you have downloaded the simulation outputs you would like to analyze, you
need to create the needed ancillary data in two steps:

```
$ python generate_covering_grids.py nofeedback_20pc
```

This script uses `yt` to convert the raw simulation outputs into uniform
resolution "covering grids" that the subsequent analysis scripts need. This will
only generate covering grid data for the fields present in the simulation
outputs. To generate the gravitational potential covering grids, you will need
to do:

```
$ python generate_gravitational_covering_grid.py nofeedback_20pc
```

This script needs a copy of the `Enzo` executable (see
[here](https://enzo.readthedocs.org/en/latest/tutorials/building_enzo.html) for
information about compiling the Enzo code) since the script uses the `-g` option
of the `Enzo` executable to to solve the Poisson equation.

Finally, you can run the `validate_covering_grid.py` script verify the integrity
of the covering grid data after it is written to disk. This script merely checks
to make sure all hdf5 files have the same internal structure, so don't
completely trust it against all possible data corruption. I created it
originally to avoid errors after creating incomplete covering grid files when
the generation script crashes or the filesystem hangs.

Note that if you are doing this for the full simulation dataset it will take *a
long time* even if you are running on multiple cores.  Note that both
`generate_covering_grids.py` and `generate_gravitational_covering_grid.py` are
MPI parallelized, so you can them using e.g. `mpirun` on multiple cores to
parallelize the analysis over multiple datasets. Note that this won't scale very
well unless you are running on a parallel filesystem since both scripts are
largely IO bound.

##Generating final processed data

Finally, to generate the final processed data, including maps of surface
densities, velocity dispersions, and Toomre Q parameters, you should use the
`analyze_data.py` script.  This script uses the covering grid data generated
in the previous step to create `GalaxyAnalyzer` objects -- the main analysis
class provided by the galaxy analysis toolkit. The `GalaxyAnalyzer` class offers
a number of analysis options to process a subset of the abailable data but also
offers an interface to calculate all the derived data that it knows how to
calculate. This is the interface that `analyze_data.py` uses. The script can
be easily modified to only calculate a subset of the data if you do not want
*all* of the processed data. To run the script, simply do:

```
$ python analyze_data.py
```

Like the covering grid generators, this script is also MPI-parallel, so run it
with `mpirun` to speed up the analysis. This script is also largely IO-bound, so
you will liekly not see a very good scaling unless you are running on a parallel
filesystem.

Note also that some of the expensive calculations are parallelized using OpenMP
so long as your operating system and compiler supports it. Right now, that means
you will need gcc although supposedly LLVM/Clang is also getting OpenMP support
soon. I optimized to iterate over the data on a single node, using MPI
parallelism to iterate over the datasets, but breaking up the work necessary to
process a given dataset using OpenMP. As a rule of thumb, I used a node with 16
cores and used 4 MPI tasks, so each MPI task used 4 OpenMP threads in the
OpenMP-parallelized sections of the analysis.

#Loading and working with the data

The available data can be accessed via an open-source python analysis
environment. The raw simulation data are written to disk in Enzo's HDF5-based
data format. The processed data are written to disk in a directory structure
containing many simple hdf5 files that contain a single dataset.

##Simulation outputs

For the raw simulation outputs, the recommended way to load them for analysis
and visualization is using yt. You will need to install yt using either the
installation script, conda, or pip, depending on whether you have a python
environment set up and how you set it up. See
http://yt-project.org/doc/installing.html for more details.

Once you have yt installed, download one of the raw datasets, unzip it, and then
load it:

```
$ wget https://hub.yt/data/goldbaum2015b/feedback_20pc/simulation_outputs/DD0600.tar.gz
$ tar xzvf DD0600.tar.gz
$ python
>>> import yt
>>> ds = yt.load('DD0600/DD0600')
```

You can then pass the `ds` object to yt's plotting commands or access yt data
objects through it to get at any on-disk or derived fields.

##Processed Data

The easiest way to deal with the processed data is via the galaxy analysis
toolkit. This can be installed via pip or from the source code. To install via
pip:

    $ pip install galanyl

To install from the source code:

```
$ hg clone https://bitbucket.org/ngoldbaum/galaxy_analysis
$ cd galaxy_analysis
$ python setup.py develop
```

Note that the latter version will make the source code the "live" version that
the python interpreter imports, so edits there will be immediately available
the next time you import the toolkit.

To load one of the example datasets, you will need to download it, unzip it, and
then load it in memory:

```
$ wget https://hub.yt/data/goldbaum2015b/feedback_20pc/processed_data/DD0600_toomre.tar.gz
$ tar xzvf DD0600_toomre.tar.gz
$ python
>>> from galanyl import GalaxyAnalyzer
>>> from matplotlib import pyplot as plt
>>> g = GalaxyAnalyzer.from_hdf5_file('DD0600_toomre')
>>> print g.gas.surface_density
>>> print g.stars.velocity_dispersion
>>> plt.imshow(g.gas.total_toome_q)
```

All of the data will be available via attributes of the GalaxyAnalyzer instance,
as in the above example. All quantities are in CGS units. The easiest way to
explore the various attributes of these objects is via tab completion in IPython
or by reading the `GalaxyAnalyzer` source code.

Alternatively, the data are also split up into one hdf5 file per dataset, so any
hdf5 reader should be able to access the data without going through
GalaxyAnalyzer.
