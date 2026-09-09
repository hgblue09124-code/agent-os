# Research Direction

Research informs architectural rules. It is not a source of implementations to copy.

Admission rule for any research insight that later becomes code:

1. What problem does it solve?
2. What architectural rule does it imply?
3. What concrete artifact implements the rule?
4. How is it verified?

If an insight cannot answer those four questions, it remains a note.

## Surveyed directions

### Neural Module Networks

Sources: Andreas, Rohrbach, Darrell, Klein — *Neural Module Networks* (arXiv:1511.02799; CVPR 2016).

Research principle: a task with compositional structure is solved by assembling reusable modules, each with a narrow operation, rather than by one undifferentiated network.

Engineering principle: capability is factored into Modules with explicit interfaces; compound behavior is a layout over those Modules.

Agent OS primitive: Module as first-class unit; Composition Program as the layout constructor.

Verification in this repository: package axis and composition-stage description in `Documentation/Architecture/ARCHITECTURE.md`; no neural layout engine.

### Neural Programmer-Interpreter

Sources: Reed and de Freitas — *Neural Programmer-Interpreter* (2016).

Research principle: a controller invokes a small library of operations and can reuse composed programs as new operations.

Engineering principle: composition yields a Module that may later be selected like any other Module. The composer is not the library.

Agent OS primitive: Meso Module is a Module; Composition Program is not a capability store.

Verification in this repository: invariant I8 and I10.

### Neuro-symbolic program synthesis

Sources: program-synthesis and neuro-symbolic lines (for example DreamCoder-style library learning, neural-symbolic composition).

Research principle: learned or extracted fragments become durable library items only after they have a typed or contractual description.

Engineering principle: extraction from `agent-core` or `living-data-ocean` must land on Module Contract, not on an Agent facade.

Agent OS primitive: future extraction pipeline documented in the README; no import of those repositories.

Verification in this repository: invariant I17 and the companion-repository table.

### Compositional / modular verification

Sources: assume-guarantee reasoning; independent refinement of subsystem contracts.

Research principle: global justification can be assembled from local proofs plus compatibility of composition, instead of one monolithic check.

Engineering principle: every Module has local verification; every composition has a separate verification of wiring and dependencies.

Agent OS primitive: `Verification/Contract` and `Verification/Composition`.

Verification in this repository: boundary packages and invariant I11. No model checker in PR-01.

### Contract-based modular systems

Sources: Meyer, design by contract; Benveniste et al., contract-based design for systems; assume/guarantee specifications.

Research principle: a component is defined by obligations and expectations at its boundary. Independent implementation is possible when the contract is stable.

Engineering principle: identity, capability, input, output, lifecycle, and dependencies are stated before implementation details.

Agent OS primitive: Module Contract (PR-02). PR-01 only reserves the facet packages and the question list.

Verification in this repository: `Documentation/Contracts/CONTRACT_BOUNDARY.md`.

### Related observation (not adopted as code)

MIT CSAIL work on *concepts* and *synchronizations* restates a useful split: independent units plus explicit, inspectable composition rules. Agent OS already encodes that split as Module versus Composition Program. No additional "concept" abstraction is introduced.

## Rejected as code in this repository

- Neural module assemblers
- Differentiable interpreters
- Domain-specific synthesizers
- Model checkers and proof assistants

They may re-enter later if they produce a Module Contract, a Composition rule, or a Verification rule that the four-question test accepts.
