# Hardware Implementation of ASCON

## 1. Introduction
ASCON is a lightweight cryptographic algorithm designed for constrained devices such as IoT systems, embedded systems, and sensor networks. This project implements and verifies ASCON using a hardware RTL implementation and a Python software reference model.

## 2. Project Objectives
The project objectives are:
- Understand ASCON encryption, decryption, and hashing.
- Implement ASCON as a hardware crypto engine.
- Verify the hardware implementation using software-generated test vectors.
- Evaluate area and power consumption.

## 3. Tools and Environment
- Operating system: Ubuntu Linux
- Hardware tool: Intel Quartus Prime Lite 24.1std
- Software language: Python 3
- Python package: ascon
- HDL: SystemVerilog
- Top-level RTL module: ascon_core
- FPGA device: [insert device]

## 4. Hardware Implementation
The ASCON RTL files were downloaded from an ASCON-Verilog hardware repository. The relevant RTL files were copied into the project hardware/rtl directory. The main hardware files used were config.sv, functions.sv, register.sv, simple_cells.v, asconp.sv, and ascon_core.sv.

The top-level entity used for synthesis was ascon_core. The design was compiled in Intel Quartus Prime Lite using SystemVerilog input settings.

## 5. RTL Compatibility Fixes
During Quartus synthesis, the original RTL failed during elaboration because some SystemVerilog enum values were written using unsized integer literals. Quartus interpreted these values as 32-bit constants while the enum base types were declared as 4-bit and 5-bit fields.

The enum values in config.sv and ascon_core.sv were rewritten using explicit-width literals such as 4'd0 and 5'd0. This does not change the functional behavior of the RTL; it only makes the state and mode encodings explicit for Quartus synthesis compatibility.

## 6. Hardware Security Analysis
The hardware implementation was analyzed against physical implementation threats. Side-channel attacks may attempt to recover secret information by observing power consumption, timing behavior, or electromagnetic leakage. Fault injection attacks may attempt to disturb the circuit using voltage glitches, clock glitches, or other physical interference.

The RTL design uses a synchronous hardware structure with finite-state-machine control, internal registers, and a permutation-based datapath. If no masking, redundancy, parity checking, duplicate computation, or fault-detection logic is present, the design should be considered functionally correct but not fully protected against advanced side-channel or fault-injection attacks.

## 7. Software Implementation
The software implementation was written in Python. It was used as the golden reference model for generating ASCON encryption, decryption, and hash test vectors.

The file generate_vectors.py generates test vectors containing key, nonce, associated data, plaintext, ciphertext with authentication tag, and hash output.

The file run_vectors.py reloads the generated test vectors and verifies that encryption, decryption, and hashing produce the expected values.

## 8. Test Vectors
The generated test vectors are stored in:
- test_vectors/test_vectors.txt
- test_vectors/test_vectors.csv
- test_vectors/test_vectors_for_tb.hex

These vectors were used as reference input/output pairs for verification.

## 9. Verification
The Python software implementation successfully generated and verified all test vectors. The hardware implementation was synthesized successfully in Quartus. The software output acts as the expected reference for comparing hardware outputs.

## 10. Area Results
[Insert Quartus area table here]

## 11. Power Results
[Insert Quartus power table here]

## 12. GitHub Repository
The complete project files were uploaded to a public GitHub repository.

Repository link:
[insert GitHub link]

## 13. Conclusion
The ASCON hardware implementation was prepared, corrected for Quartus SystemVerilog compatibility, and synthesized successfully. Python software was used to generate and verify reference test vectors. Quartus was used to obtain area and power results. The project demonstrates the complete flow of hardware implementation, software reference generation, and synthesis-based evaluation of ASCON.

