# Architecture Foundation

Status: PR-01 — boundary definition only. No runtime execution engine.

## Axis

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

The axis is a construction order, not a request-response call stack. Lower layers must not import upper layers.

## Layers

### Kernel / Runtime

Host for module execution. Owns process lifetime, scheduling hooks, and isolation of module invocation. In PR-01 this layer is a reserved package boundary plus invariants. It does not execute agents.

### Module Contract

The only legal surface through which Modules are described, selected, connected, and verified. A contract must be able to answer:

- What is the Module?
- What is its identity?
- What capability does it provide?
- What input does it accept?
- What output does it produce?
- What is its lifecycle?
- What does it depend on?
- How can it be verified?

Contract implementation belongs to PR-02. This document only freezes the questions the contract must answer.

### Module

First-class architectural primitive.

```
Module
|-- Atomic Module
`-- Meso Module
```

Atomic and Meso are not two stacked architectures. Both satisfy the same Module Contract. Meso is a Module whose body is a composition of other Modules.

### Composition Program

Second primitive. It constructs structure from existing Modules:

```
select modules
      ↓
validate contracts
      ↓
connect inputs / outputs
      ↓
validate dependencies
      ↓
construct composed module
```

A Composition Program must not become a container for business capability. It does not invent behavior; it wires Modules that already exist.

### Composed / Meso Module

The product of a successful Composition Program. It is itself a Module and therefore has a contract, identity, capability, input, output, lifecycle, dependencies, and a verification story.

### Skill

A named, reusable grouping of Modules presented to an Agent. Skill is above Module and is out of scope until the Module substrate is verified.

### Agent

A composition of Skills hosted by the Runtime. Agent is the top of the axis and is out of scope for PR-01.

## Why Module is first-class

Prior experimental work organized the system around an Agent core with supporting subsystems. Agent OS inverts that default: capability lives in Modules; the Agent is an assembly. This keeps extraction from legacy sources and from `living-data-ocean` at the Module boundary rather than at an application facade.

## What is reserved versus implemented

| Boundary | PR-01 state |
| --- | --- |
| Kernel / Runtime | Package + protocol |
| Module facets (Contract, Identity, Capability, Input, Output, Lifecycle) | Package + protocol |
| Composition Program / Graph | Package + protocol |
| Verification (Contract, Composition) | Package + protocol |
| Architectural invariants | Encoded as data and tested |
| Runtime engine, LLM, Memory, Planner, Tools | Absent by design |

If a boundary is not yet required as code, it remains a protocol. No placeholder class hierarchy is introduced to occupy space.

## Non-goals of the foundation

- Copying package names or types from `agent-core` or `agent-core-next`
- Binding to the current `living-data-ocean` tree
- Formal proof engines
- Horizontal scale, brokers, or service meshes
