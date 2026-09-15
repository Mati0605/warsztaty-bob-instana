# Warsztaty: Deploy & Monitor z Bobem i Instaną

W tych warsztatach wdrożysz aplikację na klaster OpenShift, zobaczysz ją w Instanie
i użyjesz Boba jako interfejsu do danych monitoringowych na żywo.
Nie musisz znać szczegółów Kubernetes ani API Instany.

---

## Czym jest OpenShift i dlaczego go tutaj używamy?

OpenShift Container Platform (OCP) to platforma firmy Red Hat do uruchamiania aplikacji
w kontenerach. Możesz o niej myśleć jak o systemie operacyjnym dla aplikacji w chmurze —
zamiast instalować program na jednym komputerze, wdrażasz go na klastrze serwerów,
a platforma sama dba o to, żeby działał, restartował się po awarii i skalował gdy potrzeba.
Pod spodem OpenShift używa Kubernetes, ale dodaje do niego graficzny interfejs, zarządzanie
dostępem i wiele innych funkcji przydatnych w środowiskach korporacyjnych.

W kontekście tych warsztatów OpenShift pełni rolę środowiska produkcyjnego —
tego samego typu, z jakiego korzystają duże organizacje do uruchamiania swoich systemów.
Każdy uczestnik dostaje własny, izolowany obszar roboczy (zwany **namespace**), który działa
niezależnie od innych. Dzięki temu możesz swobodnie eksperymentować bez ryzyka wpłynięcia
na kolegów. Korzystamy z jednego wspólnego klastra OCP — nie musisz nic instalować lokalnie
ani zakładać konta w chmurze.

---

## Cel warsztatów

- Wdrożyć aplikację na własny namespace na wspólnym klastrze OCP przez graficzne UI.
- Zobaczyć jak agent Instana automatycznie wykrywa i monitoruje aplikację.
- Zapytać Boba w języku naturalnym o stan aplikacji i błędy — na żywo, z danych Instany.

---

## Wymagania wstępne

Przed warsztatami upewnij się, że masz:

| Co | Skąd |
|---|---|
| Dostęp do konsoli webowej OCP | Prowadzący (adres + login) |
| Twój login i namespace | Prowadzący (login: `labuserNN`, namespace: `labprojNN`) |
| Dostęp do UI Instany | Prowadzący (adres + login) |
| Token API Instana (read-only) | Prowadzący |
| Bob zainstalowany i uruchomiony | [Bob docs] |

---

## Krok 0: Pobierz repozytorium i uruchom Boba

Instrukcja warsztatów jest dostępna online w repozytorium — czytasz ją właśnie teraz.
Żeby mieć dostęp do plików konfiguracyjnych podczas ćwiczeń, pobierz repozytorium na dysk
i otwórz je w Bobie.

### 1. Pobierz repozytorium

Kliknij zielony przycisk **Code** → **Download ZIP** (prawy górny róg strony repozytorium).

> *[screen — przycisk Code → Download ZIP na stronie GitHub]*

Rozpakuj pobrany plik ZIP w dowolnym miejscu na dysku.

### 2. Otwórz folder w Bobie

Uruchom Boba. Na ekranie startowym kliknij **Open Folder** i wskaż rozpakowany folder
repozytorium warsztatowego.

> *[screen — ekran startowy Boba z przyciskiem Open Folder]*

### 3. Zaakceptuj zaufanie do folderu

Bob wyświetli okno z pytaniem czy ufasz zawartości tego folderu.
Kliknij **Yes, I trust the authors** żeby kontynuować.

> *[screen — okno "Do you trust the authors of the files in this folder?"]*

### 4. Zaloguj się do Boba

Jeśli nie jesteś jeszcze zalogowany, Bob wyświetli monit z prośbą o zalogowanie.
Kliknij przycisk **Sign in** i zaloguj się swoimi danymi IBM.

> *[screen — ekran logowania Boba z przyciskiem Sign in]*

Po zalogowaniu Bob jest gotowy do pracy. Interfejs wygląda tak:

> *[screen — Bob z otwartym repozytorium i widocznym drzewem plików]*

Po lewej stronie widzisz drzewo plików repozytorium — stąd możesz otwierać pliki
konfiguracyjne. W środku znajduje się edytor, w którym Bob będzie wprowadzał zmiany
gdy go o to poprosisz. Po prawej stronie masz panel czatu — to tutaj piszesz swoje
pytania i polecenia do Boba. Panel czatu możesz w każdej chwili schować i odkryć
klikając ikonę Boba w prawym górnym rogu, żeby zyskać więcej miejsca na podgląd pliku.

---

## Kroki warsztatów

Wykonuj ćwiczenia po kolei. Każde zaczyna się tam, gdzie skończyło poprzednie.

| Krok | Ćwiczenie | Opis |
|---|---|---|
| 1 | [Lab 1: Deployment aplikacji](workshop/01-deploy-app.md) | Deploy aplikacji przez UI OCP + naprawa YAML-a z Bobem |
| 2 | [Lab 2: Instana — agent i monitoring](workshop/02-deploy-instana.md) | Jak działa agent Instana + weryfikacja w UI |
| 3 | [Lab 3: Monitoring przez Boba](workshop/03-monitoring-with-bob.md) | Pytanie Boba o stan appki na żywo z danych Instany |

---

## Struktura repozytorium

```
.
├── README.md                          # ten plik — zacznij tutaj
├── app/                               # aplikacja Flask + manifesty OCP
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── README.md
│   └── src/
│       ├── app.py
│       ├── Dockerfile
│       └── requirements.txt
├── mcp/                               # konfiguracja MCP dla Boba
│   ├── instana-mcp-config.json
│   └── README.md
└── workshop/                          # instrukcje laboratoriów
    ├── 01-deploy-app.md
    ├── 02-deploy-instana.md
    ├── 03-monitoring-with-bob.md
    └── prompts/
        ├── deploy-app.txt
        ├── health-check.txt
        └── error-report.txt
```

> Plik `workshop-deploy-plan.md` to wewnętrzny plan projektu — nie jest częścią warsztatów.

---

## Notatki dla prowadzącego

- Każdy uczestnik ma login `labuserNN` i namespace `labprojNN` (np. `labuser02` → `labproj02`).
- Namespace'y należy utworzyć przed warsztatami: `oc new-project labproj02` itd.
- Agent Instana jest już zainstalowany na klastrze — uczestnicy nie muszą go wdrażać.
- Token API Instana powinien mieć uprawnienia **read-only** do metryk i zdarzeń.
- Obraz aplikacji: `quay.io/paszkiewicz_pl/workshop-app:v8` — publiczny, bez pull secret.
- Przed warsztatami podaj uczestnikom: adres repo, adres konsoli OCP, adres UI Instany, token API.
