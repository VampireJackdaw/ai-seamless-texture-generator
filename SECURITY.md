# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security fixes only |
| < 0.5   | no        |

## Reporting a vulnerability

Do not open a public issue for security problems. Email
`security@texturegen.local` with:

- A description of the issue and its impact.
- Steps to reproduce (prompt, seed, backend, OS build).
- Whether the issue is remotely reachable (e.g. via the local HTTP
  bridge in `services/bridge_service.py`).

We aim to acknowledge within 72 hours and ship a fix or mitigation
within 14 days for high-severity issues.

## Scope

In scope:

- Arbitrary file write via prompt-controlled output paths.
- Path traversal in the tile cache loader.
- Deserialization of untrusted model checkpoints (`.pt`, `.ckpt`).
- Command injection through the native kernel build hook.
- Local privilege escalation via the Windows shell extension.

Out of scope:

- Generated texture content itself.
- Denial of service from intentionally huge prompts.
- Issues that require a compromised local model file the user placed
  there themselves.

## Hardening notes for users

- Only load checkpoints from sources you trust. `torch.load` with
  `weights_only=True` is enforced in `services/model_loader.py`.
- The bridge service binds to `127.0.0.1` by default. Do not expose it
  to a LAN without a reverse proxy and auth.
- Tile cache is content-addressed by SHA-256; poisoning requires a hash
  collision, which is out of scope.