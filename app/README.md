# Aplikacja warsztatowa

W tym katalogu znajdują się manifesty Kubernetes/OCP oraz kod aplikacji Flask wdrażanej podczas warsztatów.

## Zawartość

| Plik / katalog | Opis |
|---|---|
| `deployment.yaml` | Deployment z jedną repliką kontenera aplikacji Flask |
| `service.yaml` | ClusterIP Service wystawiający port 8080 |
| `src/app.py` | Kod aplikacji Flask |
| `src/Dockerfile` | Definicja obrazu kontenera |
| `src/requirements.txt` | Zależności Python (flask, gunicorn, instana) |

## Jak działa aplikacja

Aplikacja wystawia endpointy HTTP:

| Endpoint | Opis |
|---|---|
| `GET /health` | Health check dla OCP probe — zwraca `{"status": "ok"}` |
| `GET /products` | Lista produktów |
| `GET /orders` | Lista zamówień |
| `GET /inventory` | Stan magazynu |
| `GET /recommendations` | Rekomendacje |
| `GET /users/profile` | Profil użytkownika |
| `POST /checkout` | Złożenie zamówienia |
| `POST /payments` | Płatność — losowo zwraca błąd HTTP 500 (~30%) |
| `POST /checkout/confirm` | Potwierdzenie zamówienia — losowo zwraca błąd HTTP 500 (~20%) |

W tle działają dwa wątki generujące ruch widoczny w Instanie:

| Wątek | Co robi | Interwał |
|---|---|---|
| Traffic simulator | Co kilkanaście sekund wysyła prawdziwy request GET do losowego endpointu | co 10–20 sek |
| Error generator | Loguje błędy na poziomie `ERROR`, `WARNING`, `CRITICAL` | co 30–70 sek |

Aplikacja nie wymaga żadnej interakcji — od momentu uruchomienia samoczynnie produkuje
ruch i błędy HTTP 500 widoczne w Instanie.

## Przed deployment

W pliku `deployment.yaml` znajdziesz placeholder `NAMESPACE` — podmień go na swój namespace
(np. `labproj02`). Bob pomoże Ci to zrobić w Lab 1.

## Obraz kontenera

Gotowy obraz jest dostępny publicznie:

```
quay.io/paszkiewicz_pl/workshop-app:v8
```

Nie musisz budować obrazu — jest już gotowy do użycia.
