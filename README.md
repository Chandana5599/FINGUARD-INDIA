# FinGuard India

**An AI-powered financial risk analysis platform** designed to help identify potential financial stress in Indian banks using RBI financial data and explainable risk indicators.

## Technology Stack
- Frontend: React + TypeScript + Vite
- Backend: Node.js + Express + TypeScript
- Database: MySQL 8
- Data processing: Python

## Requirements
- Node.js 20.19+ (or Node.js 22+)
- MySQL 8.0+
- VS Code

## 1. Create MySQL Database

Run `database/schema.sql` in MySQL Workbench, or use:

```bash
mysql -u root -p < database/schema.sql
```

## 2. Start Backend

```bash
cd backend
```

Create your environment file:

```bash
cp .env.example .env
```

Configure your MySQL credentials in `backend/.env`. Then run:

```bash
npm install
npm run seed
npm run dev
```

The application uses 80 annual bank records covering 20 banks from FY22 to FY25.

## 3. Start Frontend

Open a second terminal in the project root:

```bash
npm install
npm run dev
```

Open http://localhost:5173

## API Endpoints

- `/api/health` – Checks backend and database connectivity.
- `/api/banks` – Returns bank information and financial records.
- `/api/banks/:id` – Returns details for an individual bank.
- `/api/compare` – Compares two banks.
- `/api/risk` – Calculates an illustrative risk assessment.

## Financial Indicators

FinGuard India currently evaluates banks using seven indicators:

- **Net NPA:** Net bad loans compared to total advances.
- **Capital Adequacy Ratio (CAR):** Measures the bank's capital strength.
- **Return on Assets (ROA):** Measures how efficiently assets generate profit.
- **Net Interest Margin (NIM):** Measures earnings from lending activities.
- **Provision Coverage Ratio (PCR):** Measures how much of gross bad loans are covered by provisions.
- **Cost-to-Income Ratio:** Measures operating expenses against income.
- **Debt-to-Equity:** Indicates the relationship between borrowings and equity.

Liquidity Coverage Ratio (LCR) is excluded because it is unavailable in the source dataset. The remaining seven indicators are reweighted to a total of 100%.

## Risk Assessment

The platform calculates a weighted score using the indicator thresholds defined in `backend/src/engine.ts`.

The score and risk categories are project-level analytical indicators, not official RBI ratings or guaranteed predictions of bank failure.

Historical trajectory compares FY22 and FY25 scores. It does not claim to forecast future performance.

## Dataset and Scope

- 20 banks
- 4 financial years (FY22–FY25)
- 80 annual observations
- RBI-based financial data
- Missing LCR values are not treated as zero.

## Project Limitations

FinGuard India is an early-warning analysis tool, not a financial guarantee or a substitute for professional financial advice.

The available historical dataset does not contain verified bank-failure labels. Therefore, the platform does not claim validated bank-failure probabilities.

Deposit insurance illustrations are indicative and are not personalized eligibility determinations.

## License

Add your chosen open-source license here!!
