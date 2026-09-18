# M3 — Dockerfiles, docker compose och GHCR

**Läge: solo** — samma arbetssätt som M2: `.dockerignore`-ändringen gick
via branch + PR + dokumenterad självgranskning.

## Steg 1 — Gissningar innan körning (backend/Dockerfile)

1. **Python-versionen:** `FROM python:3.12-slim` — basimagen avgör.
2. **Varför `COPY requirements.txt .` + `pip install` före `COPY app ./app`:**
   layer-cachen. Beroendena ändras sällan, koden ofta — i den här
   ordningen ogiltigförklarar en kodändring bara `COPY app`-lagret och
   `pip install` återanvänds från cachen. Omvänd ordning hade
   installerat om alla paket vid varje kodändring.
3. **`EXPOSE 8000`:** gissning — porten blir *inte* nåbar; `EXPOSE` är
   dokumentation. **Testat:** `docker run` utan `-p` →
   `curl http://localhost:8000/api/health` misslyckas (connection
   refused); med `-p 8000:8000` svarar den `{"status":"ok"}`. Gissningen
   stämde.

## Steg 3 — docker compose

`docker compose up --build -d` startar båda tjänsterna utan fel.
Verifierat via proxyn på port 8080:

```text
$ curl http://localhost:8080/api/health
{"status":"ok"}
$ curl http://localhost:8080/api/items
[]
```

Appen svarar i webbläsaren på den vidarebefordrade porten, med den
kombinerade rubriken från M2. `frontend`:s nginx når `backend:8000` via
compose-tjänstenamnet som DNS-namn på det interna nätverket — svaret på
steg 2:s fråga.

## Steg 4 — .dockerignore, med bevis

[PR #5](https://github.com/Tobias-Eriksson/Devops26/pull/5) (mergad via
granskad PR, självgranskning som radkommentar).

**Före:** med en planterad `backend/app/__pycache__/fake.pyc` listade
`docker run --rm backend-nocheck find /app -iname "*pycache*"` både
`/app/app/__pycache__` och `/app/tests/__pycache__` — skräpet hamnade i
imagen via `COPY app ./app` / `COPY tests ./tests`.

**Efter:** samma test mot ett `--no-cache`-bygge med
`backend/.dockerignore` på plats → tom utskrift. `**/`-prefixet är
nödvändigt: `__pycache__/` utan prefix matchar bara roten av
build-kontexten, inte `app/__pycache__` en nivå ner.

## Steg 5 — GHCR

`publish-images.yml` kör vid varje merge till `main`, men pushen nekas
med `denied: permission_denied: write_package` — paketen
`template-app-backend`/`template-app-frontend` under kontot skapades av
template-repots CI, och det här repot saknar skrivåtkomst till dem.
Åtgärd (GitHub-inställning, utanför repot): paketets **Package settings**
→ **Manage Actions access** → lägg till repot med Write — eller radera de
gamla paketen så att nästa CI-körning återskapar dem kopplade till repot.
Därefter: kör om workflown (eller merga nästa PR) och ta skärmdumpen på
**Versions**-fliken med färsk tidsstämpel.

*(Skärmdumpar för steg 1, 3, 4 och 5 — läggs till.)*
