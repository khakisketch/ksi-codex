# Review Checklist

- Active `AGENTS.md`, explorer, and rules match the source PC.
- Portable config contains no absolute home paths, project trust, desktop state,
  app tool approvals, authentication, or secret material.
- Context7 uses portable `npx` invocation.
- Dry-run makes no changes.
- Conflicts require backup or explicit force.
- Isolated install writes only documented targets.
- Repository is private.
- Release and install prompt use the final repository address.
