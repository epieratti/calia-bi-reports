# Toolbox dossiês — na raiz do repositório
.PHONY: help validate-dossier-13 validate-dossier-8 check-links-13 check-links-8 build-loterias-13 build-loterias-8

PYTHON ?= python3
ROOT := $(abspath .)

help:
	@echo "Alvos úteis:"
	@echo "  make validate-dossier-13   — valida loterias2026/data/dossier_loterias2026.md"
	@echo "  make validate-dossier-8   — valida loterias2026-20260406/data/dossier_loterias2026.md"
	@echo "  make check-links-13        — HTTP check dos links no .md (13)"
	@echo "  make build-loterias-13     — gera HTML squad 13 em loterias2026/output/"
	@echo "  make build-loterias-8      — gera HTML squad 8 em loterias2026-20260406/output/"

validate-dossier-13:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py loterias2026/data/dossier_loterias2026.md

validate-dossier-8:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py loterias2026-20260406/data/dossier_loterias2026.md

validate-dossier-strict-13:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py --strict loterias2026/data/dossier_loterias2026.md

check-links-13:
	cd "$(ROOT)" && $(PYTHON) tools/check_dossier_links.py loterias2026/data/dossier_loterias2026.md

check-links-8:
	cd "$(ROOT)" && $(PYTHON) tools/check_dossier_links.py loterias2026-20260406/data/dossier_loterias2026.md

build-loterias-13:
	cd "$(ROOT)/loterias2026" && $(PYTHON) scripts/build_dossier_completo.py

build-loterias-8:
	cd "$(ROOT)/loterias2026-20260406" && $(PYTHON) scripts/build_dossier_completo.py
