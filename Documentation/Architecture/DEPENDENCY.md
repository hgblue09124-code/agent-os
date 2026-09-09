# Dependency Direction

## Allowed direction

```
Agent
  -> Skill
    -> Meso Module
      -> Atomic Module
        -> Module Contract
          -> Kernel / Runtime
```

Arrows mean "may depend on". The reverse direction is forbidden.

## Layer permissions

| From | May depend on | Must not depend on |
| --- | --- | --- |
| Kernel | language runtime, standard library | Module implementations, Composition, Verification consumers, Skill, Agent, companion repos |
| Module | Kernel, Module Contract facets | Skill, Agent, application/business packages, companion repos |
| Composition | Module Contract, Module identity metadata | Module internal implementations, Skill, Agent, companion repos |
| Verification | Module Contract, Composition structure | Skill, Agent, companion repos |
| Skill (future) | Modules | Kernel internals |
| Agent (future) | Skill, Runtime host API | Module internals |

## Companion repositories

`agent-core`, `agent-core-next`, and `living-data-ocean` are external material. They may be read by future extraction pipelines that live outside the runtime import graph. They must not appear in `pyproject.toml` runtime dependencies.

## Composition does not invert direction

Connecting Module A's output to Module B's input does not create an import from B into A. Wiring is data-flow. Import direction remains downward toward Kernel and Contract.
