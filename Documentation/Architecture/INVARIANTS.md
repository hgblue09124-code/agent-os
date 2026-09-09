# Architectural Invariants

These rules are binding for every subsequent pull request. A PR that violates an invariant is incomplete, even if tests pass.

## Module invariants

I1. A Module has exactly one stated responsibility.

I2. A Module boundary is independent: other Modules may depend on its contract, not on its internals.

I3. A Module is described by a contract. No Module enters composition without a contract.

I4. Input and output of a Module are determinate types or schemas, not informal side effects.

I5. Dependencies of a Module are explicit and enumerable.

I6. A Module is independently testable. Tests of a Module must not require an Agent, Skill, or application layer.

I7. A Module must not depend on an application or business layer above it.

## Composition invariants

I8. A Composition Program constructs structure from existing Modules. It does not embed those Modules' business logic.

I9. Composition proceeds only after contract validation and dependency validation.

I10. The result of composition is a Module (Meso), not a new kind of primitive.

I11. Verification is part of composition architecture: local verification of each Module, then composition verification of the wiring.

## Design-process invariants

I12. Abstraction is introduced only when a boundary is required by a concrete composition or verification need.

I13. Optimization is deferred until correctness, composability, and verification are established.

I14. Distribution, microservices, and enterprise topology are forbidden until a demonstrated single-process limit is reached.

I15. Priority order is fixed: correctness -> composability -> verification -> reusability -> scale -> optimization.

## Dependency-direction invariant

I16. Allowed dependency direction is downward only:

```
Agent -> Skill -> Meso Module -> Atomic Module -> Module Contract -> Kernel
```

Kernel and Module must not import Skill or Agent. Composition and Verification may inspect Module contracts. They must not import Agent or Skill implementations.

## Repository-relation invariant

I17. `agent-os` must not declare a required runtime dependency on `agent-core`, `agent-core-next`, or `living-data-ocean`.

## PR-01 scope invariant

I18. PR-01 must not implement a Runtime engine, LLM adapter, Memory, Planner, or Tool system.
