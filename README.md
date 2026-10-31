# FinGuard India — React + TypeScript + Express + MySQL

## Requirements
- Node.js 20.19+ (or Node.js 22+)
- MySQL 8.0+
- VS Code

## 1. Create MySQL database
Run `database/schema.sql` in MySQL Workbench, or:

```bash
mysql -u root -p < database/schema.sql
```

## 2. Start backend
```bash
cd backend
cp .env.example .env
```
Edit `backend/.env` with your MySQL username/password. Then:
```bash
npm install
npm run seed
npm run dev
```
The importer uses the 80 original bank-year records extracted from the supplied RBI workbook, **not** fake seed values. The original workbook is at `dataset/RBI_FY22_FY25.xlsx`; a lossless numeric extraction of the financial columns is at `dataset/rbi_records.json`.

## 3. Start React frontend (second terminal)
From the project root:
```bash
npm install
npm run dev
```
Open http://localhost:5173

## Test
- `http://localhost:4000/api/health` → `ok:true` after DB connection
- `http://localhost:4000/api/banks` → 20 banks with 4 years each
- `cd backend && npm run typecheck`
- `npm run typecheck` from project root

## What is calculated
- Net NPA = closing net NPA / advances × 100
- CAR = RBI-published total CRAR
- ROA = net profit / year-end assets × 100
- NIM = net interest income / year-end assets × 100
- PCR = (closing gross NPA − closing net NPA) / closing gross NPA × 100
- Cost-to-income = operating expenses / (net interest income + other income) × 100
- Debt/equity = borrowings / (capital + reserves)

Health score uses the project's explicit weighted min/max normalisation in `backend/src/engine.ts`. The workbook's weight mapping is Net NPA 25%, CAR 20%, ROA 15%, NIM 10%, LCR 10%, cost-to-income 10%, debt/equity 5%, PCR 5%. Missing LCR is *not imputed*; its 10% is proportionally redistributed among available indicators. Scoring thresholds and Safe/Caution/Risky labels are **project heuristics**, not official RBI ratings.

Trajectory is the difference between FY22 and FY25 computed scores: >2 = Improving, <-2 = Deteriorating, otherwise Stable. No forecast is claimed. Historical source is annual; no fabricated quarters.

## Scope and limits
20 banks × FY22–FY25 = 80 annual observations. All 80 LCR entries are missing in the workbook. No bank-failure event labels exist, so the app cannot honestly provide validated failure probabilities or future financial projections. Deposit insurance illustrations are generic, not personalized eligibility determinations. Watchlist is stored in browser localStorage. The reference ZIP's Firebase auth and generative chatbot were intentionally not used: the project runs locally without cloud credentials and does not generate ungrounded claims.
