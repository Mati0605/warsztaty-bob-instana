# Agent Instana — materiały referencyjne

Ten katalog zawiera przykładowe manifesty agenta Instana.
Na potrzeby tych warsztatów agent jest już zainstalowany na klastrze —
nie musisz wdrażać tych plików.

Możesz je przejrzeć jako materiał poglądowy lub wykorzystać do instalacji
agenta we własnym środowisku po warsztatach.

## Zawartość

| Plik | Opis |
|---|---|
| `agent-secret.yaml` | Secret z kluczem agenta (`INSTANA_AGENT_KEY`) |
| `agent-configmap.yaml` | Konfiguracja agenta — strefa, klaster, pluginy |
| `agent-daemonset.yaml` | Deployment agenta Instana |

## Instrukcja instalacji

Szczegółowa instrukcja instalacji agenta (Helm i Operator) znajduje się w
[workshop/02-deploy-instana.md](../workshop/02-deploy-instana.md).
