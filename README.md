# ASCON Hardware Project

SystemVerilog implementation and verification flow for the ASCON lightweight cryptography algorithm. The project combines a hardware RTL core, Intel Quartus synthesis files, Python reference-vector generation, and saved test vectors for encryption/decryption and hashing checks.

## Project Contents

| Path | Purpose |
| --- | --- |
| `hardware/rtl/` | Main SystemVerilog RTL used by the Quartus project. |
| `hardware/quartus/` | Intel Quartus Prime Lite project targeting Cyclone IV E. |
| `hardware/sim/files.f` | RTL source list for simulator/testbench integration. |
| `hardware/ascon-verilog/` | Upstream ASCON-Verilog source snapshot and attribution files. |
| `software/generate_vectors.py` | Generates reference vectors with the Python `ascon` package. |
| `software/run_vectors.py` | Re-runs the reference checks against the saved CSV vectors. |
| `test_vectors/` | Generated text, CSV, HEX, and PDF test-vector files. |
| `report/` | Project report draft. |

## Hardware Design

The hardware top level is `ascon_core` in `hardware/rtl/ascon_core.sv`. It exposes a streaming key/data input interface, data output interface, mode selection, and authentication status outputs.

Supported mode encodings are defined in `hardware/rtl/config.sv`:

| Mode | Encoding |
| --- | --- |
| `M_AEAD128_ENC` | ASCON authenticated encryption |
| `M_AEAD128_DEC` | ASCON authenticated decryption |
| `M_HASH256` | ASCON-Hash256 |
| `M_XOF128` | ASCON-XOF128 |
| `M_CXOF128` | ASCON-CXOF128 |

The copied RTL was adjusted for Quartus compatibility by replacing unsized enum literals with explicit-width literals in the FSM and mode/type definitions. The default local configuration uses a 32-bit data bus with one ASCON-p round per cycle unless one of the `V1` through `V6` configuration macros is defined.

## Python Reference Flow

The software scripts use Python as the golden reference for the saved vectors.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install ascon
python3 software/generate_vectors.py
python3 software/run_vectors.py
```

`generate_vectors.py` writes:

| File | Format |
| --- | --- |
| `test_vectors/test_vectors.txt` | Human-readable vectors |
| `test_vectors/test_vectors.csv` | Structured CSV vectors |
| `test_vectors/test_vectors_for_tb.hex` | Space-separated hex fields for testbench use |

`run_vectors.py` verifies each saved vector by recomputing ASCON-128 encryption, ASCON-128 decryption, and ASCON-Hash256 outputs.

## Quartus Build

The included Quartus project was built with Intel Quartus Prime Lite 24.1std.0.

```bash
cd hardware/quartus
quartus_sh --flow compile ascon_project -c ascon_core
```

You can also open `hardware/quartus/ascon_project.qpf` in Quartus and compile the `ascon_core` revision.

Current project settings:

| Setting | Value |
| --- | --- |
| Top-level entity | `ascon_core` |
| FPGA family | Cyclone IV E |
| Device | `EP4CE115F29C7` |
| Quartus version | 24.1std.0 Build 1077 Lite Edition |
| Compile status | Successful |

## Synthesis Results

Latest saved fitter results from `hardware/quartus/output_files/ascon_core.fit.summary`:

| Resource | Usage |
| --- | ---: |
| Total logic elements | 2,560 / 114,480 (2%) |
| Combinational functions | 2,516 / 114,480 (2%) |
| Dedicated logic registers | 473 / 114,480 (<1%) |
| Total registers | 473 |
| Total pins | 125 / 529 (24%) |
| Total memory bits | 0 / 3,981,312 (0%) |
| Embedded multiplier 9-bit elements | 0 / 532 (0%) |
| Total PLLs | 0 / 4 (0%) |

Latest saved power results from `hardware/quartus/output_files/ascon_core.pow.summary`:

| Power metric | Value |
| --- | ---: |
| Total thermal power dissipation | 174.29 mW |
| Core dynamic thermal power dissipation | 0.00 mW |
| Core static thermal power dissipation | 98.81 mW |
| I/O thermal power dissipation | 75.47 mW |
| Power estimation confidence | Low |

The power report has low confidence because no detailed switching activity data was supplied. The saved timing report also shows negative setup slack for the current clock assumptions, so timing closure should be revisited before treating the design as board-ready.

## Verification Status

The saved Python vectors cover five reference cases, including empty input, associated data, plaintext messages of different lengths, ASCON-128 ciphertext/tag generation, decryption, and ASCON-Hash256 output.

The current repository includes generated reference data and Quartus synthesis outputs. A complete RTL verification flow should connect `test_vectors/test_vectors_for_tb.hex` to a SystemVerilog or cocotb testbench and compare `ascon_core` outputs against the saved ciphertext/tag and hash values.

## Security Notes

This implementation is a functional ASCON hardware core. It does not add masking, redundancy, parity checks, duplicate computation, or dedicated fault-detection logic in the project-level RTL. For deployment in hostile physical environments, side-channel and fault-injection countermeasures should be evaluated separately.

## Attribution

The ASCON RTL is based on Robert Primas's `ascon-verilog` project, included under `hardware/ascon-verilog/`. The upstream snapshot includes `CITATION.cff` and the CC0 1.0 license text.
