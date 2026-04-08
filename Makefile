# Toolbox dossiês — na raiz do repositório
.PHONY: help \
	validate-dossier-squad-13 validate-dossier-squad-8 validate-dossier-squad-13-strict \
	check-links-squad-13 check-links-squad-8 \
	build-dossier-squad-13 build-dossier-squad-8 \
	validate-dossier-minimo build-dossier-minimo-preview \
	qa-dossier-squad-13 qa-dossier-squad-8 check-html-leakage \
	validate-dossier-13 validate-dossier-8 validate-dossier-strict-13 \
	check-links-13 check-links-8 \
	build-loterias-13 build-loterias-8

PYTHON ?= python3
ROOT := $(abspath .)

help:
	@echo "Alvos úteis:"
	@echo "  make validate-dossier-squad-13   — valida loterias2026/data/dossier_loterias2026.md"
	@echo "  make validate-dossier-squad-8   — valida loterias2026-20260406/data/dossier_loterias2026.md"
	@echo "  make validate-dossier-minimo    — valida examples/minimo/dossier_minimo_exemplo.md"
	@echo "  make build-dossier-minimo-preview — gera examples/minimo/output-preview.html (gitignored)"
	@echo "  make qa-dossier-squad-13        — validate + links + build 13 + check vazamento HTML"
	@echo "  make qa-dossier-squad-8         — idem para lote 8"
	@echo "  make check-html-leakage         — vazamento em caixa/, embratur/, outputs modo B"
	@echo "  make check-links-squad-13        — HTTP check dos links no .md (13)"
	@echo "  make build-dossier-squad-13     — gera HTML squad 13 em loterias2026/output/"
	@echo "  make build-dossier-squad-8      — gera HTML squad 8 em loterias2026-20260406/output/"
	@echo "(Aliases legados: validate-dossier-13, build-loterias-13, …)"

validate-dossier-squad-13:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py loterias2026/data/dossier_loterias2026.md

validate-dossier-squad-8:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py loterias2026-20260406/data/dossier_loterias2026.md

validate-dossier-squad-13-strict:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py --strict loterias2026/data/dossier_loterias2026.md

check-links-squad-13:
	cd "$(ROOT)" && $(PYTHON) tools/check_dossier_links.py loterias2026/data/dossier_loterias2026.md

check-links-squad-8:
	cd "$(ROOT)" && $(PYTHON) tools/check_dossier_links.py loterias2026-20260406/data/dossier_loterias2026.md

build-dossier-squad-13:
	cd "$(ROOT)/loterias2026" && $(PYTHON) scripts/build_dossier_completo.py

build-dossier-squad-8:
	cd "$(ROOT)/loterias2026-20260406" && $(PYTHON) scripts/build_dossier_completo.py

validate-dossier-minimo:
	cd "$(ROOT)" && $(PYTHON) tools/validate_dossier_source.py examples/minimo/dossier_minimo_exemplo.md

build-dossier-minimo-preview:
	cd "$(ROOT)/loterias2026" && $(PYTHON) scripts/build_dossier_completo.py \
		--md ../examples/minimo/dossier_minimo_exemplo.md \
		--panels ../examples/minimo/dossier_minimo_exemplo_panels.yaml \
		--out ../examples/minimo/output-preview.html \
		--variant squad_8 --no-gate

check-html-leakage:
	cd "$(ROOT)" && $(PYTHON) tools/check_client_html_leakage.py caixa embratur loterias2026/output loterias2026-20260406/output

qa-dossier-squad-13: validate-dossier-squad-13 check-links-squad-13 build-dossier-squad-13 check-html-leakage

qa-dossier-squad-8: validate-dossier-squad-8 check-links-squad-8 build-dossier-squad-8 check-html-leakage

# Aliases (nomes antigos; mantidos para scripts e hábitos locais)
validate-dossier-13: validate-dossier-squad-13
validate-dossier-8: validate-dossier-squad-8
validate-dossier-strict-13: validate-dossier-squad-13-strict
check-links-13: check-links-squad-13
check-links-8: check-links-squad-8
build-loterias-13: build-dossier-squad-13
build-loterias-8: build-dossier-squad-8
