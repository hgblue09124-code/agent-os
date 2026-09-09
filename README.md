# Agent OS

Canonical architecture for Agent OS: a module-centric operating system and runtime for agents.

This repository is a clean foundation. It is not a fork, copy, or refactor of prior agent repositories. Implementation in this first increment is intentionally small. The architecture is designed so that later industrial scale does not require a rewrite of the primitive boundaries.

## Purpose

Agent OS treats **Module** as the first-class primitive. An agent is assembled from verified modules, not from a monolithic application core.

Architectural axis:

```
Kernel / Runtime
        ↓
Module Contract
        ↓
Atomic Module
        ↓
Composition Program
        ↓
Composed / Meso Module
        ↓
Skill
        ↓
Agent
```

`Atomic Module` and `Meso Module` are both Modules. Meso is not a separate architectural tier. It is a Module produced by composing smaller Modules.

## Scope of this repository

In scope for the foundation:

- Kernel and Runtime *boundary*
- Module Contract *boundary*
- Composition Program *boundary*
- Compositional Verification *boundary*
- Architectural invariants and dependency direction
- Roadmap of small, reviewable pull requests

Explicitly out of scope for PR-01 and not present as implementation:

- Agent runtime execution engine
- LLM integration
- Memory subsystem
- Planner
- Tool system
- Distributed or microservice topology

Industrial architecture is not the same as industrial-scale implementation. The first implementation remains minimal.

## Relation to other repositories

| Repository | Role relative to Agent OS |
| --- | --- |
| `agent-core` | Legacy source / historical material |
| `agent-core-next` | Previous experimental reconstruction |
| `living-data-ocean` | Refined Module-ready seed substrate |
| `agent-os` | Canonical Agent OS architecture |

Agent OS has **no required runtime dependency** on the three companion repositories.

Future extraction pipeline (not implemented here):

```
legacy source
      ↓
analysis / extraction
      ↓
atomic capability
      ↓
Module Contract
      ↓
verification
      ↓
Agent OS
```

```
living-data-ocean
      ↓
qualified Module seed
      ↓
contract verification
      ↓
Agent OS Module
```

`living-data-ocean` may later supply qualified seeds. Agent OS must not hard-depend on Ocean's current directory or schema.

## Package layout

```
agent-os/
|-- Kernel/           # runtime host boundary
|-- Module/           # first-class Module primitive and contract facets
|-- Composition/      # Composition Program and graph boundary
|-- Verification/     # local and compositional verification boundary
|-- Tests/            # package and invariant smoke tests
`-- Documentation/    # architecture, contracts, roadmap, research
```

Empty-looking package directories are reserved boundaries, not unfinished product code. Where a boundary is not yet implemented, the protocol lives in documentation.

## Architectural rules

1. One Module has one clear responsibility.
2. A Module has an independent boundary.
3. A Module has an explicit contract.
4. Input and output are determinate.
5. Dependencies are explicit.
6. A Module can be tested in isolation.
7. A Module must not depend upward on an application or business layer.
8. Composition must not embed the business logic of the composed Modules.
9. Verification is part of the composition architecture.
10. Do not add abstraction solely to enlarge the architecture.
11. Do not optimize prematurely.
12. Do not introduce distribution, microservices, or enterprise topology before they are required.
13. Priority order: correctness -> composability -> verification -> reusability -> scale -> optimization.

## Development

Requires Python 3.11 or newer.

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## Roadmap

See [Documentation/Roadmap/ROADMAP.md](Documentation/Roadmap/ROADMAP.md).

PR-01 establishes the repository and architecture foundation only. Subsequent PRs introduce Module Contract, Atomic Module, Composition Program, compositional verification, and the first Meso Module.

## License

Not declared in PR-01.
