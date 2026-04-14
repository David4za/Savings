# AGENTS.md

## Coding Guidance

Separation of concerns must be at the forefront of all code created in this repository.

- Keep business logic separate from presentation, routing, persistence, and external integrations.
- Prefer small, focused functions and modules with clear responsibilities.
- Avoid mixing data access, validation, formatting, and UI concerns in the same code path.
- Introduce shared helpers only when they reduce meaningful duplication or clarify ownership.
- Keep changes scoped to the layer or component responsible for the behavior being changed.
- When adding features, first identify which part of the system owns the behavior, then place the code there.

Code should be easy to reason about because each module has an obvious purpose and minimal unrelated responsibilities.
