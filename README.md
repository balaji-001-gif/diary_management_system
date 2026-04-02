# Dairy Management System (DMS) — Frappe App

[![Frappe](https://img.shields.io/badge/Frappe-v15-blue)](https://frappe.io)
[![ERPNext](https://img.shields.io/badge/ERPNext-v15-green)](https://erpnext.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A production-ready **custom Frappe app** built on ERPNext v15+ covering the complete dairy value chain — from herd management and raw milk collection through processing, quality control, and farmer billing.

---

## 📦 Modules

| # | Module | DocTypes | Description |
|---|--------|----------|-------------|
| 1 | **Animal Management** | Animal, Breed, Health Record, Breeding Record, Lactation Cycle | Herd registry, health events, breeding, lactation tracking |
| 2 | **Milk Collection & Quality** | Milk Collection Entry, Milk Quality Test, Shift Summary, BMC Log, Collection Center, Rejection Record | Daily farmer collection, fat/SNF testing, shift summaries |
| 3 | **Processing & Production** | Processing Order, Pasteurization Log, Batch Production, Packaging Record, Product Formula, Yield Analysis, Plant Downtime Log | Pasteurization, batch production, yield analysis |
| 4 | **Procurement & Routes** | Farmer, Milk Route, Rate Slab (+ Rate Slab Row), Milk Procurement, Procurement Payment, Deduction Master | Farmer master, route management, fat×SNF rate matrix |
| 5 | **Inventory & Cold Chain** | Cold Storage Log (+ Temperature Reading), Expiry Tracker, Crate Container Master | Cold chain monitoring, expiry tracking, crate management |
| 6 | **Quality Control & Lab** | Lab Test Template (+ QC Parameter), QC Inspection (+ QC Result), Compliance Log, Supplier Milk Rejection Log, Equipment Calibration Log | FSSAI compliance, lab tests, calibration records |
| 7 | **Farmer Billing & Finance** | Farmer Invoice (+ Deduction Voucher), Advance Loan, Milk Price Revision, Payment Cycle Setting, Cooperative Member | Monthly billing, loan EMI deductions, Purchase Invoice integration |
| 8 | **Reports & Analytics** | 8 Script Reports | Yield, cost, quality, cold chain dashboards |

---

## 🚀 Installation

```bash
# 1. Get the app
bench get-app dairy_management https://github.com/balaji-001-gif/diary_management_system.git

# 2. Install on your ERPNext site
bench --site your-site.local install-app dairy_management

# 3. Run migrations
bench --site your-site.local migrate

# 4. Restart and clear cache
bench restart
bench --site your-site.local clear-cache
```

---

## 📊 Script Reports

| Report | Module | Filters |
|--------|--------|---------|
| Herd Yield Report | Animal Management | Animal, Date Range |
| Animal Health Calendar | Animal Management | Animal, Date Range |
| Milk Procurement Summary | Milk Collection | Farmer, Route, Period |
| Processing Yield Report | Processing | Product, Period |
| Cold Chain Compliance | Inventory | Warehouse, Date Range |
| Expiry Alert Report | Inventory | Days to Expiry threshold |
| Farmer Payment Register | Billing | Farmer, Period |
| Dairy PL Summary | Billing | Period |

---

## ⚙️ Key Technical Features

- **Fat × SNF Price Engine** — `dairy_management/utils/calculations.py` — auto-fetches rate from Rate Slab matrix on every Milk Collection Entry save
- **Auto-creation hooks** — Milk Quality Test on MCE submit, Stock Entry on Batch Production submit, Purchase Receipt on Milk Procurement submit, Purchase Invoice on Farmer Invoice submit, Work Order on Processing Order submit
- **Scheduler tasks** — Daily milk summary aggregation, vaccination due alerts, cold chain temperature breach checks, weekly farmer invoice generation
- **FSSAI compliance** — Pasteurization parameter validation (HTST ≥ 72°C / 15s), QC Inspection pass/fail engine, Compliance Log, Equipment Calibration Log
- **ERPNext integration** — Custom fields on Supplier, Item, Stock Entry, Purchase Invoice, Quality Inspection via `fixtures/custom_fields.json`

---

## 🔑 Custom Roles

| Role | Description |
|------|-------------|
| Dairy Manager | Full access to all DMS modules |
| Milk Collection Supervisor | Collection entry, shift management |
| Lab Technician | Quality testing, calibration logs |
| Route Agent | Field collection, crate management |
| Farmer | Portal access (read-only) |

---

## 📁 Directory Structure

```
dairy_management/
├── hooks.py                  # Scheduler events, doc events, roles
├── tasks.py                  # Scheduler task implementations
├── config/desktop.py         # Workspace module tiles
├── fixtures/                 # roles.json, custom_fields.json
├── utils/
│   ├── calculations.py       # Fat/SNF price engine
│   ├── validators.py         # Input validation helpers
│   └── reports.py            # Report utilities
├── animal_management/        # Module 1
├── milk_collection/          # Module 2
├── processing/               # Module 3
├── procurement/              # Module 4
├── inventory/                # Module 5
├── quality_control/          # Module 6
├── billing/                  # Module 7
└── public/                   # JS/CSS assets
```

---

## 📋 Naming Series

| DocType | Series |
|---------|--------|
| Animal | `ANM-.YYYY.-.####` |
| Milk Collection Entry | `MCE-.YYYY.MM.DD.-.###` |
| Batch Production | `BPR-.YYYY.-.####` |
| Processing Order | `PO-DMS-.YYYY.-.####` |
| Farmer Invoice | `FINV-.YYYY.MM.-.####` |
| Milk Procurement | `MPR-.YYYY.MM.DD.-.##` |
| QC Inspection | `QCI-.YYYY.-.####` |
| Advance Loan | `ALN-.YYYY.-.####` |

---

## 🖥️ Server Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Ubuntu 20.04 LTS | Ubuntu 22.04 LTS |
| Python | 3.10+ | 3.11+ |
| ERPNext | v15.0 | v15 latest |
| Frappe | v15.0 | v15 latest |
| RAM | 8 GB | 16 GB |
| Disk | 50 GB SSD | 200 GB SSD |

---

## 📄 License

MIT License — Copyright © 2026 Antigravity
