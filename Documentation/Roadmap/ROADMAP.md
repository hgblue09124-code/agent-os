# Roadmap

Work proceeds as a sequence of small pull requests. Each PR follows:

Inspect -> Design -> Implement -> Test -> Review diff -> Verify -> Stop

Do not collapse later PRs into an earlier one.

## PR-01 — Repository + Architecture Foundation

Current increment.

- Create `agent-os` as an independent repository
- Record purpose, axis, invariants, and dependency direction
- Reserve Kernel, Module, Composition, and Verification packages
- Provide package/test foundation and a smoke test
- Record research direction without copying research implementations

Stop after Definition of Done. Do not start Module Contract code in this PR.

## PR-02 — Module Contract

Introduce the minimal contract protocol that answers identity, capability, input, output, lifecycle, dependency, and verification questions. Tests cover construction and rejection of incomplete contracts.

## PR-03 — Atomic Module

First Module that satisfies the contract and can be tested without composition.

## PR-04 — Composition Program

Implement select -> validate contracts -> connect I/O -> validate dependencies -> construct composed Module. No business logic inside the program.

## PR-05 — Compositional Verification

Local verification plus composition verification of wiring compatibility.

## PR-06 — First Composed / Meso Module

One Meso Module produced only through the Composition Program, with tests that the result is itself a Module.

## PR-07+ — Expand verified Module substrate

Add Modules only when they have a contract, tests, and an extraction or design rationale. Optional later pipelines:

```
legacy source -> analysis / extraction -> atomic capability -> Module Contract -> verification -> Agent OS
living-data-ocean -> qualified Module seed -> contract verification -> Agent OS Module
```

## Explicitly deferred

Runtime execution engine, LLM, Memory, Planner, Tool system, Skills as a product layer, Agent hosting, formal verification engines, distributed topology, benchmarks, and optimization.
