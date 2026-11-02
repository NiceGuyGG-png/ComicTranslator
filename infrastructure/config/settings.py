"""Validated runtime configuration.

YAML is the source of truth (``configs/*.yaml``).  Secrets are optional only to
protect a self-hosted gateway via an Authorization header; they live in
environment variables, never in files.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# Only in-process local inference is supported. Third-party model APIs are
# intentionally absent from the architecture.
ProviderKind = Literal["mock", "local_transformers"]

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "configs" / "default.yaml"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AppInfo(StrictModel):
    name: str = "ComicTranslator"
    version: str = "0.3.0"
    environment: str = "development"


class ProviderSettings(StrictModel):
    kind: ProviderKind = "mock"
    model: str | None = None
    model_path: str | None = Field(
        default=None, description="Local checkpoint dir; no remote download happens here"
    )
    device: str = "cpu"
    dtype: str = "float32"
    max_new_tokens: int = Field(default=1024, ge=1)
    trust_remote_code: bool = False
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=1)
    prompt_version: str = "v1"


class EngineSettings(StrictModel):
    provider: str = "mock"
    enabled: bool = True
    fallback_provider: str | None = None
    options: dict[str, object] = Field(default_factory=dict)


class EvaluationEngineSettings(EngineSettings):
    """Evaluation composes several providers (e.g. rule_based + llm)."""

    providers: list[str] = Field(default_factory=lambda: ["rule_based"])
    aggregate: Literal["merge", "first"] = "merge"


class EnginesSettings(StrictModel):
    story_analysis: EngineSettings = Field(default_factory=lambda: EngineSettings(provider="mock"))
    translation: EngineSettings = Field(default_factory=lambda: EngineSettings(provider="mock"))
    evaluation: EvaluationEngineSettings = Field(
        default_factory=lambda: EvaluationEngineSettings(provider="rule_based")
    )


class ApiSettings(StrictModel):
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])
    max_upload_bytes: int = Field(default=20 * 1024 * 1024, ge=1024)


class StorageSettings(StrictModel):
    backend: Literal["memory", "filesystem"] = "memory"
    root: str = "outputs/jobs"


class ObservabilitySettings(StrictModel):
    log_level: str = "INFO"
    log_format: Literal["plain", "json"] = "plain"


class WorkflowSettings(StrictModel):
    default: Literal[
        "basic_translation",
        "context_aware_translation",
        "translation_with_evaluation",
        "independent_evaluation",
    ] = "context_aware_translation"
    max_correction_iterations: int = Field(default=0, ge=0, le=3)
    fail_fast: bool = False


class AppSettings(StrictModel):
    app: AppInfo = Field(default_factory=AppInfo)
    engines: EnginesSettings = Field(default_factory=EnginesSettings)
    providers: dict[str, ProviderSettings] = Field(
        default_factory=lambda: {"mock": ProviderSettings(kind="mock", model="mock-llm")}
    )
    api: ApiSettings = Field(default_factory=ApiSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    observability: ObservabilitySettings = Field(default_factory=ObservabilitySettings)
    workflow: WorkflowSettings = Field(default_factory=WorkflowSettings)

    @field_validator("providers")
    @classmethod
    def _provider_names(cls, providers: dict[str, ProviderSettings]) -> dict[str, ProviderSettings]:
        if not providers:
            raise ValueError("at least one provider must be configured")
        return providers

    def provider(self, name: str) -> ProviderSettings:
        try:
            return self.providers[name]
        except KeyError as exc:
            raise KeyError(f"provider '{name}' is not configured") from exc


def _deep_merge(base: dict, override: dict) -> dict:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_settings(path: str | Path | None = None) -> AppSettings:
    """Load YAML config, merged over ``configs/default.yaml`` when customising.

    ``COMIC_CONFIG_PATH`` selects an alternate file. Secrets are never stored in
    config files because local inference needs none.
    """
    resolved = Path(path or os.environ.get("COMIC_CONFIG_PATH") or DEFAULT_CONFIG_PATH)
    if not resolved.exists():
        raise FileNotFoundError(f"config file not found: {resolved}")

    raw = yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}
    if resolved.name != "default.yaml" and DEFAULT_CONFIG_PATH.exists():
        default_raw = yaml.safe_load(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8")) or {}
        raw = _deep_merge(default_raw, raw)
    return AppSettings.model_validate(raw)


__all__ = [
    "DEFAULT_CONFIG_PATH",
    "AppSettings",
    "ProviderKind",
    "ProviderSettings",
    "load_settings",
]
