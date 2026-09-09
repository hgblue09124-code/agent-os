# Module Contract Boundary

Status: protocol for PR-02. No contract framework is implemented in PR-01.

## Questions the contract must answer

| Question | Facet | Package reserved in this repository |
| --- | --- | --- |
| What is a Module? | definition | `Module/` |
| What identity does it have? | identity | `Module/Identity/` |
| What capability does it provide? | capability | `Module/Capability/` |
| What input does it accept? | input | `Module/Input/` |
| What output does it produce? | output | `Module/Output/` |
| What is its lifecycle? | lifecycle | `Module/Lifecycle/` |
| What does it depend on? | dependency list on the contract | `Module/Contract/` |
| How can it be verified? | local verification | `Verification/Contract/` |

## Design constraint for PR-02

Prefer a small protocol, interface, or dataclass. Do not introduce a framework, registry service, plugin loader, or schema language until a second independent consumer exists.

Atomic and Meso share this contract. Composition does not invent a second contract type; it produces a Module that satisfies the same contract.

## Verification pairing

```
Module Contract  ->  local verification
A + B + wiring   ->  composition verification
```

Long-term goal: if each Module satisfies its contract and the composition satisfies compatibility rules, the composed Module is justified at the composition layer. Formal proof engines are not required to establish the boundary.
