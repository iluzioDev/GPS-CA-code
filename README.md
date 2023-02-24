# GPS L1C/A Codes Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Twitter](https://img.shields.io/twitter/follow/luctstt.svg?label=Follow&style=social)](https://twitter.com/iluzioDev)

## Introduction 📋

__GPS L1C/A (Coarse/Acquisition)__ are sequences of zeroes and ones used in GPS communications, being __P-Code__ other type of code GPS uses.

They are also known by PRN codes (Pseudorandom Noise), but in reality they are generated using an algorithm, which is freely available, and that's the main goal of this repo.

Inside this repo is an implementation of the C/A Algorithm developed in Python, so anyone could generate codes with customized polynomials and sequences of ```n``` desired bits.

[GPS Signals](https://en.wikipedia.org/wiki/GPS_signals)

<p float="left">
	<img src="https://www.researchgate.net/publication/340551421/figure/fig2/AS:879832166563841@1586779743041/Structural-scheme-GPS-C-A-ranging-code-generator.png" alt="C/A code generator" height="225px">
</p>

## Features ✨

* Customized inputs.
* Collection of satellites taps by prn code.

## Install 🔧

```console
git clone https://github.com/iluzioDev/gpsl1ca
cd gpsl1ca
python3 gpsl1ca
```

## Usage 💡

Once executed, a menu will prompt asking for desired option:

```console
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
■          WELCOME TO THE GPS L1C/A CODE GENERATOR!               ■
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
What would you want to do?
[1] Generate GPS L1C/A Code.
[2] Check G2 Taps by prn id.
[0] Exit.
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
Option  ->
```

1. Asks for a ```prn id``` and number of bits to generate. Once inputs are introduced, it will generate a code of ```n bits``` each one result of the algorithm operations. In the end, a table will be prompted with all steps made and the resulting code.

2. Shows the collection of taps by ```prn id```. 

## API

```{eval-rst}
.. autofunction:: gpsl1ca.LFSR
```

```{eval-rst}
.. autofunction:: gpsl1ca.GPS_L1CA_generator
```

```{eval-rst}
.. autofunction:: gpsl1ca.main
```

## Maintainers 👷

<table>
  <tr>
    <td align="center"><a href="https://github.com/iluzioDev"><img src="https://avatars.githubusercontent.com/u/45295283?v=4" width="100px;" alt="IluzioDev"/><br /><sub><b>IluzioDev</b></sub></a><br />💻</td>
  </tr>
</table>

## License ⚖️

Distributed under the MIT License. [Click here](LICENSE.md) for more information.

---
<div align="center">
	<b>
		<a href="https://www.npmjs.com/package/get-good-readme">File generated with get-good-readme module</a>
	</b>
</div>