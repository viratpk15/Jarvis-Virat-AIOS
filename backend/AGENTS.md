# Jarvis AIOS Engineering Guide

## Mission

You are contributing to Jarvis AIOS.

Your goal is to help build a production-quality AI Operating System.

---

## Architecture

FastAPI
↓
Runtime
↓
LangGraph
↓
Tool Engine
↓
Tools

Runtime is the public entry point.

LangGraph orchestrates only.

Tool Engine executes tools.

Tools contain business logic.

---

## Rules

Never rename folders.

Never change architecture without asking.

Never delete existing code unless requested.

Always explain why each file is modified.

Prefer modifying existing modules over creating new ones.

Keep functions small and readable.

Do not duplicate code.

Keep imports clean.

Use Python type hints.

Follow existing project conventions.

---

## Git

One feature = one branch.

Never commit automatically.

Never push automatically.

Always ask before destructive operations.

---

## Coding Style

Prefer composition over duplication.

Avoid global variables.

Keep modules single-responsibility.

Write production-ready code.