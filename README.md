# preCICE CLI

The `precice-cli` is a uniform and simple access to all command line tools of preCICE.
Some commands use tools provided by the preCICE library and require it to be installed.
The installed executables must be in PATH.

## Installation options

Install directly from PyPi using [pipx](https://pipx.pypa.io/stable/) or via pip:

```console
pipx install precice-cli
```

## Usage examples


### Configuration

```console
precice-cli config format precice-config.xml
```

```console
precice-cli config visualize precice-config.xml -o graph.pdf
```

```console
precice-cli config check precice-config.xml
precice-cli config check precice-config.xml SolverOne
```

### Profiling

Pre-processing:

```console
precice-cli profiling merge
```

Post-processing:

```console
precice-cli profiling export
precice-cli profiling trace
precice-cli profiling analyze SolverOne
```

### Version display

```console
precice-cli version
```

### Case generation

```console
precice-cli init
```
