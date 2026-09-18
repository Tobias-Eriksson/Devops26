# M2 — Branch protection, review och en löst konflikt

**Läge: solo.** *Required approvals* står på **0** i rulesetten (GitHub
låter aldrig PR-författaren approva sin egen PR), så godkännandet ersätts
av dokumenterad självgranskning i varje PR — beskrivningens "Så testar du"
plus minst en egen kommentar på diffen.

## Steg 1 — Branch protection

Ruleset *Main branch protection* på default-branchen med **Require a pull
request before merging** och **Required approvals: 0** (solo),
**Enforcement status: Active**. Bypass-listan är tom.

*(Skärmdump: inställningssidan för regeln — läggs till.)*

## Steg 2 — Testet att skyddet håller

En tom commit direkt mot `main` avvisades av GitHub med
*"Changes must be made through a pull request"*. Testcommitten städades
bort med `git reset --hard origin/main`.

*(Skärmdump: terminalen med den avvisade pushen — läggs till.)*

## Steg 4 — Mergad PR med dokumenterad självgranskning

[PR #1 — Add endpoint for fetching a single item](https://github.com/Tobias-Eriksson/Devops26/pull/1):
mergad via granskad PR. Självgranskningen: checkade ut branchen, körde
`cd backend && pytest` — alla tester gröna, inklusive de två nya
(träffen och 404:an). Kommentaren ligger kvar på PR:en.

## Steg 5 — Konfliktövningen (solo-varianten)

Två brancher från samma `main`-commit (`69043b1`), båda ändrade
`<h1>`-raden i `frontend/index.html`:

- [PR #2 (`konflikt-1`)](https://github.com/Tobias-Eriksson/Devops26/pull/2)
  satte rubriken till *Tobias anteckningar* — mergades först.
- [PR #3 (`konflikt-2`)](https://github.com/Tobias-Eriksson/Devops26/pull/3)
  satte samma rad till *Template App – anteckningar* — GitHub visade
  *"This branch has conflicts that must be resolved"*.

Konflikten löstes i terminalen: `git merge origin/main` gav
`CONFLICT (content): Merge conflict in frontend/index.html`, blocket
ersattes med den **kombinerade** rubriken *Template App – Tobias
anteckningar*, sedan `git add` + `git commit` + `git push` och merge av
PR:en. Verifierat på `main`: `git grep '<<<<<<<'` är tyst och appen visar
den kombinerade rubriken. Mergade brancher raderades på GitHub.

*(Skärmdump: konflikt-bannern på PR #3 / terminalens CONFLICT-rad — läggs till.)*
