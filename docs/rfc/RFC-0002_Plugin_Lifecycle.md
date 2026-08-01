# RFC-0002 Plugin Lifecycle

## Purpose

This RFC defines the lifecycle states for plugins in Shirakami OS and describes the expected behavior for each state. The lifecycle clarifies how the Runtime manages plugin presence and activity without prescribing implementation details.

## States

- Installed

  The plugin's files and metadata are present in the environment but it is not yet known to the Runtime for operation.

- Registered

  The Runtime has recorded the plugin's metadata and acknowledges its existence; registration does not imply the plugin is active.

- Activated

  The plugin is prepared by the Runtime for execution (resources allocated, preconditions checked) but may not yet process workloads.

- Running

  The plugin is actively performing its responsibilities and processing inputs as designed within the Runtime's control model.

- Suspended

  The plugin's execution is temporarily paused by the Runtime; state is preserved to allow later resumption without full reinitialization.

- Stopped

  The plugin is no longer executing and has released runtime resources; it may be restarted or removed depending on policy.

- Removed

  The plugin's artifacts and registration are deleted from the environment; the Runtime no longer recognizes the plugin.

## Principles

- Runtime controls lifecycle.
- Foundation remains immutable.
- Plugins do not manage other plugins.

## Out of Scope

This RFC does not define or prescribe:

- APIs
- Loaders
- Dependency resolution
- Security
- Configuration
- Runtime implementation

Lifecycle precedes implementation.
