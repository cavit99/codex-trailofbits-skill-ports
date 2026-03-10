#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

try:
    import yaml
except ModuleNotFoundError:
    print(
        "PyYAML is required to refresh the Polymarket catalog.\n"
        "Run: uv run --with pyyaml python scripts/refresh_catalog.py",
        file=sys.stderr,
    )
    raise SystemExit(1)

USER_AGENT = "codex-polymarket-api-skill/1.0"
HTTP_METHODS = {"get", "post", "put", "delete", "patch"}
SITEMAP_URL = "https://docs.polymarket.com/sitemap.xml"
OPENAPI_REF_PATTERN = re.compile(
    r"(api-(?:spec|reference)/[A-Za-z0-9_-]+\.(?:yaml|yml|json))\s+"
    r"(get|post|put|delete|patch)\s+"
    r"(/[^\"\\]+)"
)
PAGE_METADATA_PATTERN = re.compile(
    r'\\"pageMetadata\\":\{.{0,2400}?\\"openapi\\":\\"([^"]+)\\".{0,800}?\\"href\\":\\"([^"]+)\\"',
    re.DOTALL,
)

SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES_DIR = SKILL_ROOT / "references"
GENERATED_DIR = REFERENCES_DIR / "generated"
SPECS_DIR = REFERENCES_DIR / "specs"

SERVICE_SPECS: dict[str, dict[str, str]] = {
    "gamma": {
        "label": "Gamma API",
        "spec_name": "gamma-openapi.yaml",
        "spec_url": "https://docs.polymarket.com/api-spec/gamma-openapi.yaml",
        "fallback_doc_url": "https://docs.polymarket.com/api-reference/introduction",
    },
    "clob": {
        "label": "CLOB API",
        "spec_name": "clob-openapi.yaml",
        "spec_url": "https://docs.polymarket.com/api-spec/clob-openapi.yaml",
        "fallback_doc_url": "https://docs.polymarket.com/api-reference/introduction",
    },
    "data": {
        "label": "Data API",
        "spec_name": "data-openapi.yaml",
        "spec_url": "https://docs.polymarket.com/api-spec/data-openapi.yaml",
        "fallback_doc_url": "https://docs.polymarket.com/api-reference/introduction",
    },
    "bridge": {
        "label": "Bridge API",
        "spec_name": "bridge-openapi.yaml",
        "spec_url": "https://docs.polymarket.com/api-spec/bridge-openapi.yaml",
        "fallback_doc_url": "https://docs.polymarket.com/api-reference/introduction",
    },
    "relayer": {
        "label": "Relayer API",
        "spec_name": "relayer-openapi.yaml",
        "spec_url": "https://docs.polymarket.com/api-spec/relayer-openapi.yaml",
        "fallback_doc_url": "https://docs.polymarket.com/api-reference/introduction",
    },
}


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def normalize_whitespace(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def normalize_spec_name(spec_path: str) -> str:
    name = Path(spec_path).name
    if name.endswith(".json"):
        return name[:-5] + ".yaml"
    if name.endswith(".yml"):
        return name[:-4] + ".yaml"
    return name


def parse_sitemap_urls() -> list[str]:
    xml_text = fetch_text(SITEMAP_URL)
    return sorted(set(re.findall(r"<loc>(.*?)</loc>", xml_text)))


def extract_doc_refs(page_html: str, page_url: str) -> list[tuple[str, str, str]]:
    page_path = urlsplit(page_url).path
    refs: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for raw_ref, href in PAGE_METADATA_PATTERN.findall(page_html):
        if href != page_path:
            continue
        for spec_path, method, route in OPENAPI_REF_PATTERN.findall(raw_ref):
            ref = (normalize_spec_name(spec_path), method.upper(), route)
            if ref not in seen:
                refs.append(ref)
                seen.add(ref)
    return refs


def fetch_doc_refs(url: str) -> tuple[str, list[tuple[str, str, str]], str | None]:
    try:
        refs = extract_doc_refs(fetch_text(url), url)
    except Exception as exc:  # pragma: no cover - network errors are only surfaced at runtime
        return url, [], f"{type(exc).__name__}: {exc}"
    return url, refs, None


def collect_doc_urls() -> tuple[dict[tuple[str, str, str], str], list[str]]:
    api_urls = [url for url in parse_sitemap_urls() if "/api-reference/" in url]
    doc_urls: dict[tuple[str, str, str], str] = {}
    errors: list[str] = []
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = [pool.submit(fetch_doc_refs, url) for url in api_urls]
        for future in as_completed(futures):
            url, refs, error = future.result()
            if error:
                errors.append(f"{url}: {error}")
                continue
            for ref in refs:
                doc_urls.setdefault(ref, url)
    return doc_urls, sorted(errors)


def schema_type(schema: dict[str, Any] | None) -> str | None:
    if not isinstance(schema, dict):
        return None
    if "$ref" in schema:
        return str(schema["$ref"]).split("/")[-1]
    if "type" in schema:
        schema_name = str(schema["type"])
        if schema_name == "array":
            item_type = schema_type(schema.get("items")) or "object"
            return f"array[{item_type}]"
        return schema_name
    if "enum" in schema:
        return "enum"
    if "oneOf" in schema:
        return "oneOf"
    if "anyOf" in schema:
        return "anyOf"
    return None


def merge_parameters(path_item: dict[str, Any], operation: dict[str, Any]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for raw_param in list(path_item.get("parameters") or []) + list(operation.get("parameters") or []):
        if not isinstance(raw_param, dict):
            continue
        name = str(raw_param.get("name") or "")
        location = str(raw_param.get("in") or "")
        if not name or not location:
            continue
        key = (name, location)
        if key in seen:
            continue
        merged.append(
            {
                "name": name,
                "in": location,
                "required": bool(raw_param.get("required")),
                "description": normalize_whitespace(raw_param.get("description")),
                "type": schema_type(raw_param.get("schema")),
            }
        )
        seen.add(key)
    return merged


def infer_auth_level(service: str, operation: dict[str, Any]) -> str:
    if service != "clob":
        return "public"
    security = operation.get("security") or []
    if not security:
        return "public"
    schemes = {scheme for requirement in security if isinstance(requirement, dict) for scheme in requirement}
    if schemes and schemes <= {"polyAddress", "polySignature", "polyTimestamp", "polyNonce"}:
        return "l1"
    return "l2"


def infer_sdk_preference(service: str, path: str, auth_level: str) -> str:
    if service == "relayer":
        return "official-relayer-sdk"
    if service == "clob" and (path.startswith("/auth/builder-api-key") or path.startswith("/builder/")):
        return "official-builder-sdk"
    if service == "clob" and auth_level in {"l1", "l2"}:
        return "official-clob-sdk"
    return "direct-http"


def request_body_summary(operation: dict[str, Any]) -> dict[str, Any] | None:
    request_body = operation.get("requestBody")
    if not isinstance(request_body, dict):
        return None
    content = request_body.get("content") or {}
    content_types = sorted(content.keys())
    body_schemas: dict[str, str | None] = {}
    for content_type, details in content.items():
        if isinstance(details, dict):
            body_schemas[content_type] = schema_type(details.get("schema"))
    return {
        "required": bool(request_body.get("required")),
        "content_types": content_types,
        "schemas": body_schemas,
    }


def operation_entries(
    *,
    service: str,
    spec_name: str,
    spec: dict[str, Any],
    doc_urls: dict[tuple[str, str, str], str],
    generated_at: str,
) -> list[dict[str, Any]]:
    server = ""
    servers = spec.get("servers") or []
    if servers and isinstance(servers[0], dict):
        server = str(servers[0].get("url") or "")

    entries: list[dict[str, Any]] = []
    for path, path_item in sorted((spec.get("paths") or {}).items()):
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            auth_level = infer_auth_level(service, operation)
            parameters = merge_parameters(path_item, operation)
            entry = {
                "service": service,
                "service_label": SERVICE_SPECS[service]["label"],
                "server": server,
                "method": method.upper(),
                "path": path,
                "operation_id": str(operation.get("operationId") or f"{method}_{path}"),
                "summary": normalize_whitespace(operation.get("summary")) or normalize_whitespace(operation.get("description")),
                "description": normalize_whitespace(operation.get("description")),
                "tags": [str(tag) for tag in operation.get("tags") or []],
                "auth_level": auth_level,
                "sdk_preference": infer_sdk_preference(service, path, auth_level),
                "doc_url": doc_urls.get(
                    (spec_name, method.upper(), path),
                    SERVICE_SPECS[service]["fallback_doc_url"],
                ),
                "source_spec": spec_name,
                "source_spec_url": SERVICE_SPECS[service]["spec_url"],
                "parameters": parameters,
                "path_params": [param for param in parameters if param["in"] == "path"],
                "query_params": [param for param in parameters if param["in"] == "query"],
                "header_params": [param for param in parameters if param["in"] == "header"],
                "request_body": request_body_summary(operation),
                "security_schemes": sorted(
                    {
                        scheme
                        for requirement in operation.get("security") or []
                        if isinstance(requirement, dict)
                        for scheme in requirement
                    }
                ),
                "deprecated": bool(operation.get("deprecated")),
                "generated_at": generated_at,
            }
            entries.append(entry)
    return entries


def render_rest_endpoints(entries: list[dict[str, Any]], generated_at: str) -> str:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        grouped[entry["service"]].append(entry)

    lines = [
        "# Polymarket REST Endpoints",
        "",
        f"Generated from the official Polymarket OpenAPI specs on {generated_at}.",
        "Regenerate with `scripts/refresh_catalog.py`.",
        "",
    ]
    for service in SERVICE_SPECS:
        service_entries = sorted(grouped.get(service, []), key=lambda item: (item["path"], item["method"]))
        if not service_entries:
            continue
        lines.extend(
            [
                f"## {SERVICE_SPECS[service]['label']}",
                "",
                f"Base URL: `{service_entries[0]['server']}`",
                "",
                "| Method | Path | Auth | Operation ID | Summary | Docs |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for entry in service_entries:
            summary = entry["summary"] or "-"
            docs = f"[Docs]({entry['doc_url']})" if entry["doc_url"] else "-"
            lines.append(
                f"| {entry['method']} | `{entry['path']}` | `{entry['auth_level']}` | "
                f"`{entry['operation_id']}` | {summary} | {docs} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> int:
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    doc_urls, doc_errors = collect_doc_urls()

    spec_payloads: dict[str, str] = {}
    entries: list[dict[str, Any]] = []
    missing_docs: list[str] = []

    for service, metadata in SERVICE_SPECS.items():
        spec_text = fetch_text(metadata["spec_url"])
        spec_payloads[service] = spec_text
        spec = yaml.safe_load(spec_text)
        if not isinstance(spec, dict):
            raise ValueError(f"Unexpected spec payload for {service}")
        service_entries = operation_entries(
            service=service,
            spec_name=metadata["spec_name"],
            spec=spec,
            doc_urls=doc_urls,
            generated_at=generated_at,
        )
        for entry in service_entries:
            if entry["doc_url"] == metadata["fallback_doc_url"]:
                missing_docs.append(f"{entry['method']} {entry['path']} ({service})")
        entries.extend(service_entries)

    for service, spec_text in spec_payloads.items():
        write_text(SPECS_DIR / SERVICE_SPECS[service]["spec_name"], spec_text)

    entries.sort(key=lambda item: (list(SERVICE_SPECS).index(item["service"]), item["path"], item["method"]))
    write_text(GENERATED_DIR / "endpoints.json", json.dumps(entries, indent=2) + "\n")
    write_text(REFERENCES_DIR / "rest-endpoints.md", render_rest_endpoints(entries, generated_at))

    print(f"Wrote {len(entries)} endpoints to {GENERATED_DIR / 'endpoints.json'}")
    print(f"Wrote REST index to {REFERENCES_DIR / 'rest-endpoints.md'}")
    if doc_errors:
        print(f"Encountered {len(doc_errors)} API reference fetch errors:", file=sys.stderr)
        for error in doc_errors[:10]:
            print(f"  - {error}", file=sys.stderr)
    if missing_docs:
        print(f"{len(missing_docs)} endpoints fell back to the service intro doc.", file=sys.stderr)
        for missing in missing_docs[:10]:
            print(f"  - {missing}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
