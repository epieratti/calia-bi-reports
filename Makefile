# Toolbox dossiês — na raiz do repositório
.PHONY: help \
	validate-dossier-squad-13 validate-dossier-squad-8 validate-dossier-squad-13-strict \
	check-links-squad-13 check-links-squad-8 \
	build-dossier-squad-13 build-dossier-squad-8 \
	validate-dossier-minimo build-dossier-minimo-preview \
	qa-dossier-squad-13 qa-dossier-squad-8 check-html-leakage \
	dossie-build dossie-qa dossie-filename dossie-entregar dossie-pdf

PYTHON ?= python3
ROOT := $(abspath .)

PROJECT_SQUAD_13 := caixa/loterias/always-on-20260401
PROJECT_SQUAD_8 := caixa/loterias/always-on-20260406
MD_SQUAD_13 := projects/$(PROJECT_SQUAD_13)/data/dossier_loterias2026.md
MD_SQUAD_8 := projects/$(PROJECT_SQUAD_8)/data/dossier_loterias2026.md
MD_MINIMO := projects/_template/dossier_minimo_exemplo.md

help:
	@echo "Alvos úteis:"
	@echo "  make dossie-build PROJECT=caixa/loterias/always-on-20260401"
	@echo "  make dossie-qa    PROJECT=caixa/loterias/always-on-20260401"
	@echo "  make dossie-entregar PROJECT=caixa/loterias/always-on-20260401"
	@echo "  make dossie-entregar MD=projects/.../dossier_x.md DEST=caixa/loterias"
	@echo "  make dossie-pdf HTML=caixa/loterias/....html OUT=....pdf"
	@echo "  make qa-dossier-squad-13 / qa-dossier-squad-8 — aliases dos lotes de referência"
	@echo "  make check-html-leakage — vazamento em caixa/, febraban/, embratur/"

dossie-build:
	@test -n "$(PROJECT)" || (echo "Defina PROJECT=caixa/loterias/always-on-20260401"; exit 1)
	cd "$(ROOT)" && $(PYTHON) engine/cli/build_dossier.py --project "$(PROJECT)"

dossie-qa: dossie-build
	@test -n "$(PROJECT)" || (echo "Defina PROJECT="; exit 1)
	cd "$(ROOT)" && $(PYTHON) engine/qa/validate_source.py "projects/$(PROJECT)/data/"*.md
	cd "$(ROOT)" && $(PYTHON) engine/qa/check_html_leakage.py caixa febraban embratur

validate-dossier-squad-13:
	cd "$(ROOT)" && $(PYTHON) engine/qa/validate_source.py "$(MD_SQUAD_13)"

validate-dossier-squad-8:
	cd "$(ROOT)" && $(PYTHON) engine/qa/validate_source.py "$(MD_SQUAD_8)"

validate-dossier-squad-13-strict:
	cd "$(ROOT)" && $(PYTHON) engine/qa/validate_source.py --strict "$(MD_SQUAD_13)"

check-links-squad-13:
	cd "$(ROOT)" && $(PYTHON) engine/qa/check_links.py "$(MD_SQUAD_13)"

check-links-squad-8:
	cd "$(ROOT)" && $(PYTHON) engine/qa/check_links.py "$(MD_SQUAD_8)"

build-dossier-squad-13:
	cd "$(ROOT)" && $(PYTHON) engine/cli/build_dossier.py --project "$(PROJECT_SQUAD_13)"

build-dossier-squad-8:
	cd "$(ROOT)" && $(PYTHON) engine/cli/build_dossier.py --project "$(PROJECT_SQUAD_8)"

validate-dossier-minimo:
	cd "$(ROOT)" && $(PYTHON) engine/qa/validate_source.py "$(MD_MINIMO)"

build-dossier-minimo-preview:
	cd "$(ROOT)" && $(PYTHON) engine/cli/build_dossier.py \
		--md "$(MD_MINIMO)" \
		--panels projects/_template/dossier_minimo_exemplo_panels.yaml \
		--out projects/_template/preview.html \
		--variant squad_8 --no-gate

check-html-leakage:
	cd "$(ROOT)" && $(PYTHON) engine/qa/check_html_leakage.py caixa febraban embratur

qa-dossier-squad-13: validate-dossier-squad-13 check-links-squad-13 build-dossier-squad-13 check-html-leakage
qa-dossier-squad-8: validate-dossier-squad-8 check-links-squad-8 build-dossier-squad-8 check-html-leakage

validate-dossier-13: validate-dossier-squad-13
validate-dossier-8: validate-dossier-squad-8
validate-dossier-strict-13: validate-dossier-squad-13-strict
check-links-13: check-links-squad-13
check-links-8: check-links-squad-8
build-loterias-13: build-dossier-squad-13
build-loterias-8: build-dossier-squad-8

dossie-filename:
	@test -n "$(MD)" || (echo "Defina MD= caminho/dossier_*.md"; exit 1)
	cd "$(ROOT)" && $(PYTHON) engine/cli/html_filename.py --md "$(MD)" \
		$(if $(DATE),--date $(DATE),) \
		$(if $(SUFFIX),--suffix "$(SUFFIX)",)

dossie-entregar:
	@if [ -n "$(PROJECT)" ]; then \
		cd "$(ROOT)" && $(PYTHON) engine/cli/publish_dossier.py --project "$(PROJECT)" \
			$(if $(SKIP_LINKS),--skip-links,); \
	elif [ -n "$(MD)" ] && [ -n "$(DEST)" ]; then \
		cd "$(ROOT)" && $(PYTHON) engine/cli/publish_dossier.py --md "$(MD)" --dest "$(DEST)" \
			$(if $(VARIANT),--variant $(VARIANT),) \
			$(if $(DATE),--date $(DATE),) \
			$(if $(SUFFIX),--suffix "$(SUFFIX)",) \
			$(if $(SKIP_LINKS),--skip-links,); \
	else \
		echo "Defina PROJECT= ou MD= + DEST="; exit 1; \
	fi

dossie-pdf:
	@test -n "$(HTML)" || (echo "Defina HTML= e OUT="; exit 1)
	@test -n "$(OUT)" || (echo "Defina OUT="; exit 1)
	@if [ "$(SKIP_GATE)" != "1" ] && [ -z "$$DOSSIER_PDF_PASSWORD" ]; then echo "Exporte DOSSIER_PDF_PASSWORD ou SKIP_GATE=1"; exit 1; fi
	cd "$(ROOT)" && $(PYTHON) engine/cli/export_pdf.py --html "$(HTML)" --out "$(OUT)" \
		$(if $(SKIP_GATE),--skip-gate,) \
		$(if $(POST_UNLOCK_WAIT),--post-unlock-wait $(POST_UNLOCK_WAIT),) \
		$(if $(PDF_LANDSCAPE),--landscape,) \
		$(if $(PDF_MARGIN_TIGHT),--margin-tight,)
