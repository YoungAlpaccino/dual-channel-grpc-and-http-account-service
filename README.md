# Dual-Channel gRPC + HTTP Account Service

> ## NOTE
> **The code in this repository is a demonstration of the architecture and is not a working service.**
> Entity names, RPC contracts, and any external integrations have been deliberately abstracted.
> Treat the files as a structural blueprint, not as something you can run against a real backend.

---

## What this project demonstrates

A single service exposed on **two channels at once**:

1. **gRPC** for internal callers — typed proto contracts, low latency, server-streaming for
   long-running queries.
2. **HTTP/JSON** for everything else — humans, dashboards, integrations that don't want
   to compile a proto.

Both channels share the *same* repository layer underneath, so there is exactly one place
where business decisions are made. The service-layer module knows nothing about whether
the caller arrived through gRPC or HTTP.

The companion `crashproof_main.py` shows the supervisor pattern — a tiny parent process that
restarts the worker on any crash, so an upstream RPC hiccup never takes the whole service
down.

## High-level diagram

```
   ┌────────────┐                    ┌────────────┐
   │  gRPC      │                    │  HTTP      │
   │  clients   │                    │  clients   │
   └──────┬─────┘                    └──────┬─────┘
          │  proto                          │  json
          ▼                                 ▼
   ┌─────────────┐                    ┌─────────────┐
   │ grpc_server │                    │ http_server │
   └──────┬──────┘                    └──────┬──────┘
          │                                  │
          └───────────┬──────────────────────┘
                      ▼
              ┌───────────────┐
              │  service.py   │  ◄── single source of truth
              └───────────────┘
                      │
                      ▼
              ┌───────────────┐
              │  models.py    │
              │  (postgres)   │
              └───────────────┘
```

## Files in this showcase

| File | What it shows |
|------|---------------|
| `protos/account.proto`        | Wire contract: messages + service definitions. |
| `generate_proto.py`           | Codegen wrapper around `grpc_tools.protoc`. |
| `grpc_server.py`              | Async gRPC server wiring. |
| `grpc_client.py`              | Sample client for smoke tests. |
| `http_server.py`              | FastAPI mirror of the same operations. |
| `service.py`                  | The shared service layer both channels call into. |
| `models.py`                   | SQLAlchemy entity sketches (abstract). |
| `schemas.py`                  | Pydantic contracts for the HTTP side. |
| `database.py`                 | Engine + session factory. |
| `config.py`                   | Settings via env vars. |
| `crashproof_main.py`          | Tiny supervisor that restarts the worker on crash. |
| `main.py`                     | Single-process entrypoint (gRPC + HTTP on the same loop). |
| `requirements.txt`            | Unpinned dependency surface. |
