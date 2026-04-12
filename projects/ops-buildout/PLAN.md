# Operations Buildout — Master Plan v4
**Status:** ACTIVE | **Updated:** 2026-03-10 | **Budget:** $75,000

---

## Company Context

- **Company:** Mount Hydra (mounthydra.com)
- **Industry:** Regenerative medicine — MSCs + exosomes
- **Year 1 Revenue:** ~$650K
- **Avg Order Size:** $25K (MSC-heavy) → trending ~$5K as exosome mix increases
- **Budget:** $75K for operations buildout

### Team

| Person | Role | Focus | Future State |
|--------|------|-------|-------------|
| **Jeff** | Sales | All sales, handles manual order exceptions, working on onboarding docs | Transition to oversight as agents + future sales hire take over |
| **Scientist** | Product Production | Product production | Unchanged |
| **Todd** | Advisory / Finance (0.5 FTE) | Was supposed to be advisory. Helping with finance. | Return to advisory + investor role. Agents handle finance ops. |
| **Contract Bookkeeper** | Bookkeeping (on-call) | Previously used, can be brought back for QBO cleanup | Execute corrections with explicit direction, work double-checked |

---

## Current Systems & Status

| System | Role | Status |
|--------|------|--------|
| **mounthydra.com** (WooCommerce) | Primary storefront, account-based ordering, 3 SKUs (expanding to <10) | ✅ Working |
| **PayNote** | ACH payments | ✅ Working (occasional NSF rejections) |
| **ShipStation** | Fulfillment + FedEx | ✅ Working (waits for payment clearance) |
| **FedEx** | Carrier | ✅ Working |
| **QuickBooks Online** | Accounting | ❌ Data incorrect — needs cleanup |
| **Go High Level** | CRM (cold leads, minimal setup) | ⚠️ Building from scratch |
| **3dexosomes.com** | Exosome site (GHL) | 🔄 Converting to lead gen funnel |

---

## Confirmed Decisions

| # | Decision | Status |
|---|----------|--------|
| 1 | WooCommerce = single order channel | ✅ |
| 2 | 3dexosomes.com = lead gen funnel | ✅ |
| 3 | Eliminate QBO direct invoicing | ✅ |
| 4 | GHL = CRM + marketing + sales (build from scratch) | ✅ |
| 5 | Xero replaces QBO (after cleanup) | ✅ |
| 6 | Documents output to `/Documents/Obsidian Vault/` | ✅ |
| 7 | Customer emails: order confirmed, order shipped, order delivered | ✅ |

---

## Current Order Flow (Detailed)

### Happy Path
```
1. Prospect applies for account on mounthydra.com
2. Jeff/Todd MANUALLY approves applicant        ← manual gate
3. Customer logs in, browses 3 SKUs, places order
4. PayNote processes ACH
5. Payment clears → ShipStation creates shipment
6. ShipStation buys FedEx postage → ships
7. FedEx delivers
```

### Known Manual Interventions / Edge Cases

| # | Scenario | Current Handling | Target State |
|---|----------|-----------------|--------------|
| **M1** | Applicant approval | Jeff/Todd manually reviews and approves | Keep manual (security gate for regulated products). Agent surfaces pending applicants daily, provides summary for fast approval. |
| **M2** | ACH rejected (NSF — buyer has pending deposit) | Manual follow-up by Jeff | Agent detects NSF, auto-notifies customer with "payment failed, please retry when funds clear" email. Alerts Jeff. Monitors for retry. |
| **M3** | Buyer sends wire/ACH directly to get same-day shipping (bypasses PayNote wait) | Jeff manually reconciles and tells ShipStation to ship | Agent detects incoming wire/ACH (via bank feed), matches to pending order, alerts Jeff to authorize early release. Future: auto-authorize with confirmation rules. |
| **M4** | Tracking not sent to customer after shipment | Unknown — possibly not happening | Agent sends "order shipped" email with tracking link when ShipStation creates label. |
| **M5** | Order status not updated on delivery | Not happening | Agent monitors FedEx tracking, updates order status to "delivered" when FedEx confirms delivery. Sends "order delivered" email. |

---

## Phase 1A: Order-to-Delivery Pipeline (Weeks 1-4)
### Goal: Bulletproof order flow with full tracking, customer notifications, and GHL recording

### Target State
```
Customer applies → [MANUAL: Jeff/Todd approves] → Customer orders on WooCommerce
  → PayNote ACH processes
    IF payment clears:
      → ShipStation creates shipment → FedEx ships → delivered
      → Customer gets: ✉️ order confirmed, ✉️ shipped + tracking, ✉️ delivered
      → GHL contact updated at every stage
    IF ACH fails (NSF):
      → Customer gets: ✉️ "payment failed, please retry"
      → Jeff alerted
      → Agent monitors for retry
    IF buyer sends direct wire/ACH for same-day:
      → Agent detects payment, matches to order
      → Jeff alerted to authorize early shipment
```

### Build Steps

#### Step 1: Audit current integrations (Week 1)
- [ ] Verify WooCommerce → ShipStation sync: is it automatic? Webhook or polling? What data flows?
- [ ] Verify PayNote → WooCommerce: how does payment status update? Webhook? Does WooCommerce order status change automatically?
- [ ] Check ShipStation → FedEx tracking: does ShipStation get tracking updates from FedEx? How often?
- [ ] Check: does WooCommerce currently send ANY order emails? (confirmation, shipped, etc.)
- [ ] Document exact API capabilities: WooCommerce REST API, ShipStation API, PayNote API (if any), GHL API

#### Step 2: Customer notification emails (Week 1-2)
Three emails, built in GHL (or WooCommerce native if simpler):

**Email 1: Order Confirmed**
- Trigger: WooCommerce order placed + payment initiated
- Content: Order summary, products, amount, expected timeline
- Tone: Professional, warm, "thank you for your order"

**Email 2: Order Shipped**
- Trigger: ShipStation creates shipping label / FedEx pickup
- Content: "Your order is on its way" + FedEx tracking link + expected delivery date
- Tone: Excited, "it's coming!"

**Email 3: Order Delivered**
- Trigger: FedEx tracking status = delivered
- Content: "Your order has been delivered" + any handling/storage instructions + support contact
- Tone: Warm, "let us know if you need anything"

**Build approach:**
- [ ] Draft email templates → Todd/Jeff review for tone and compliance
- [ ] Decide where to send from: GHL (preferred for CRM tracking) or WooCommerce (simpler)
- [ ] Wire triggers via Make.com:
  - WooCommerce order created → Email 1
  - ShipStation shipment notification → Email 2
  - FedEx delivered status → Email 3

#### Step 3: GHL customer record integration (Week 2-3)
- [ ] Define GHL custom fields:
  - `last_order_date`, `lifetime_value`, `order_count`, `last_order_status`
  - Product tags (MSC, exosome, specific SKUs)
- [ ] Build Make.com automations:
  - WooCommerce new order → create/update GHL contact → log order details
  - Payment confirmed → update GHL
  - ShipStation shipped → update GHL with tracking #
  - FedEx delivered → update GHL status to "delivered"
- [ ] GHL order pipeline (for visibility):
  - `Order Placed → Payment Confirmed → Shipped → In Transit → Delivered`

#### Step 4: Edge case handling (Week 2-3)

**M1 — Applicant approval assist:**
- [ ] Build agent check: daily scan of pending WooCommerce account applications
- [ ] Agent sends Jeff/Todd a summary: "3 pending applicants: [name, business, location]"
- [ ] Jeff/Todd approve or reject (still manual — appropriate security gate)
- [ ] Future: scoring criteria to flag high-priority applicants

**M2 — ACH failure (NSF):**
- [ ] Identify how PayNote reports NSF → does WooCommerce order status change? Webhook?
- [ ] Build Make.com trigger: payment failed → send customer "payment unsuccessful" email
- [ ] Alert Jeff via GHL notification or SMS
- [ ] Agent monitors: if customer retries within 7 days → process normally. If not → follow-up email day 3, day 7.

**M3 — Direct wire/ACH for same-day shipping:**
- [ ] This depends on bank feed visibility. Once Xero is live with bank feeds:
  - Agent detects incoming wire/ACH
  - Matches amount to pending WooCommerce order
  - Alerts Jeff: "Wire received for Order #1234 ($25,000). Authorize early shipment?"
  - Jeff approves → agent (or Make.com) triggers ShipStation to ship
- [ ] For now (pre-Xero): Jeff manually confirms wire receipt and triggers ShipStation
- [ ] Document SOP for Jeff in the interim

**M4/M5 — Tracking and delivery status:**
- [ ] Solved by Email 2 and Email 3 above
- [ ] ShipStation API provides tracking events — use these as triggers
- [ ] If ShipStation doesn't relay FedEx delivery status reliably: use FedEx Track API directly (via Make.com or agent)

#### Step 5: Agent F2 — Order Operations Monitor (Week 3-4)
**Systems:** WooCommerce API, ShipStation API, GHL API, Make.com
**Cadence:** Daily morning check + event-triggered alerts

**Daily check:**
- [ ] Pending applicants awaiting approval → notify Jeff/Todd
- [ ] Orders placed in last 24h — all accounted for in ShipStation?
- [ ] Payments: any failures, pending, or cleared?
- [ ] Shipments: any orders paid > 24h ago without a shipment?
- [ ] In transit: any packages overdue or with exceptions?
- [ ] Delivered: any deliveries in last 24h → confirm delivery emails sent
- [ ] Digest → Jeff + Todd

**Event-triggered:**
- ACH failure → immediate customer email + Jeff alert
- Shipment created → trigger shipped email
- Delivery confirmed → trigger delivered email + update GHL
- Stuck order (paid but no shipment in 24h) → Jeff alert

**Build steps:**
- [ ] Write Agent F2 SKILL.md
- [ ] Set up API credentials (WooCommerce, ShipStation, GHL)
- [ ] Build daily check routine
- [ ] Build event-triggered alert logic
- [ ] Shadow mode: 1 week (agent reports, Jeff/Todd verify)
- [ ] Go live with daily review for 2 weeks
- [ ] Autonomous

#### Step 6: Eliminate QBO invoicing channel (Week 3-4)
- [ ] Identify any open QBO invoices → close out or migrate to WooCommerce
- [ ] Create WooCommerce accounts for any QBO-invoice-only customers
- [ ] Document "concierge order" SOP: Jeff places WooCommerce order on customer's behalf
- [ ] Communicate to affected customers
- [ ] Disable Intuit Payments for new transactions

### Phase 1A Deliverables
- ✅ Every order tracked from placement through delivery
- ✅ Customer gets 3 emails: confirmed, shipped, delivered
- ✅ GHL records every order lifecycle event on customer record
- ✅ Edge cases handled: NSF, direct wire, applicant approvals
- ✅ Agent F2 monitoring daily + event-triggered alerts
- ✅ QBO invoicing eliminated
- ✅ Jeff's manual work reduced to: applicant approval + exception authorization

---

## Phase 1B: Financial Cleanup & Xero Migration (Weeks 1-4, Concurrent)
### Goal: Clean books, accurate financials, Todd exits daily finance work

### Approach: Audit → Direct → Execute → Verify

Given: contract bookkeeper available, needs explicit direction and double-checking.

#### Step 1: QBO forensic audit (Week 1-2)
**Clark (agent) does the analysis:**
- [ ] Pull complete bank statements for the full operating period
- [ ] Pull all QBO transactions for the same period
- [ ] Reconcile month-by-month:
  - Missing transactions (in bank, not in QBO)
  - Ghost transactions (in QBO, not in bank)
  - Miscategorized transactions
  - Wrong amounts
  - Duplicate entries
- [ ] Compile error report with EXPLICIT corrections:
  - "Transaction X on date Y: currently categorized as Z, should be A"
  - "Missing transaction: $B,000 deposit on date C from [source], categorize as D"
  - "Duplicate entry: delete transaction E (keep transaction F)"
- [ ] Save error report to Obsidian Vault

#### Step 2: Contract bookkeeper execution (Week 2-3)
- [ ] Send bookkeeper the correction document — explicit, line-by-line
- [ ] Bookkeeper executes all corrections in QBO
- [ ] Bookkeeper provides corrected trial balance, P&L, balance sheet

#### Step 3: Verification (Week 3)
**Clark (agent) verifies:**
- [ ] Re-pull QBO data after corrections
- [ ] Re-reconcile against bank statements
- [ ] Verify every correction was executed correctly
- [ ] Flag any remaining discrepancies
- [ ] If clean: generate corrected financial statements
- [ ] If not: send bookkeeper round 2 corrections
- [ ] Todd reviews and signs off on corrected financials

#### Step 4: Xero setup and migration (Week 3-4)
- [ ] Set up Xero account
- [ ] Design chart of accounts:
  - **Revenue:** MSC sales, exosome sales
  - **COGS:** product costs, shipping/postage, packaging
  - **Operating:** software (GHL, ShipStation, hosting, etc.), marketing, contractor payments, payroll/draws
  - **Balance sheet:** checking account(s), AR, AP, credit cards
- [ ] Import CLEANED QBO data via Xero migration tool
- [ ] Connect bank feeds
- [ ] Set up Xero ↔ WooCommerce revenue sync (Make.com)
- [ ] Configure invoice templates (for any non-order receivables)
- [ ] Parallel run: 2 weeks alongside QBO
- [ ] Validate: totals match, no data loss
- [ ] Todd + bookkeeper sign off
- [ ] Cut over to Xero

#### Step 5: Agent F1 — Bookkeeper (Week 4+)
**Systems:** Xero API, bank feeds
**Cadence:** Daily + weekly + monthly

**Daily:**
- Check bank feed for new transactions
- Auto-categorize known transaction types (WooCommerce deposits, PayNote, recurring expenses)
- Flag uncategorized or unusual transactions → Todd

**Weekly:**
- Cash flow summary → Todd (current balance, in/out this week, projected next 2 weeks)
- AR status: any outstanding receivables?

**Monthly:**
- Close checklist: reconcile all accounts, review auto-categorizations
- Generate P&L and balance sheet
- Flag anomalies (margins shifting, unexpected expenses, trends)
- Report → Todd

**Quarterly:**
- Compile data package for tax prep
- Send to external accountant (if applicable)

**Escalation:**
- Unmatched transaction > $500 → Todd immediately
- Cash balance below $X threshold → Todd
- Suspicious transaction → Todd

**Build steps:**
- [ ] Write Agent F1 SKILL.md
- [ ] Set up Xero API credentials
- [ ] Build daily/weekly/monthly routines
- [ ] Build report templates
- [ ] Shadow mode: 2 weeks (agent reports, Todd/bookkeeper verify)
- [ ] Go live

### Phase 1B Deliverables
- ✅ QBO cleaned up — accurate, reconciled, verified
- ✅ Corrected financial statements available
- ✅ Xero live with clean data
- ✅ Bank feeds connected, auto-categorization running
- ✅ Agent F1 handling daily bookkeeping
- ✅ Todd gets weekly cash flow summary, monthly financials
- ✅ Todd OUT of daily finance work

---

## Phase 2: Sales Pipeline Build (Weeks 4-8)
### Goal: GHL pipeline from cold lead to closed deal

#### GHL Pipeline Stages
1. **New Lead** — entered system from any source
2. **Contacted** — first outreach made
3. **Engaged** — responded, showing interest
4. **Qualified** — budget, need, authority, timeline confirmed
5. **Proposal/Quote** — pricing/product discussion
6. **Onboarding** — Jeff's prospect-to-customer docs and execution
7. **Closed Won** → triggers WooCommerce account setup + first order
8. **Closed Lost** → log reason, enter re-engagement pool

#### Lead Scoring
| Signal | Points | Rationale |
|--------|--------|-----------|
| Referral source | +30 | Highest conversion |
| Organic search | +20 | Intent-driven |
| Paid ad | +15 | — |
| Cold list | +5 | Low intent |
| Multi-provider clinic | +25 | Higher volume potential |
| Solo practitioner | +15 | — |
| New practice | +10 | — |
| Opened email | +5 | — |
| Clicked link | +10 | — |
| Visited pricing page | +15 | High intent |
| Replied to outreach | +20 | Active engagement |
| Requested call | +30 | Ready to talk |
| Asked about pricing | +15 | Buying signal |
| Volume inquiry | +20 | Large deal potential |
| Domestic | +10 | Easier fulfillment |
| Score > 60 | → Auto-offer call scheduling | — |

#### 3dexosomes.com Conversion to Lead Gen
- [ ] Redesign as educational / lead capture:
  - Product information and clinical use cases
  - "Request Information" / "Schedule Consultation" forms
  - Lead magnet (whitepaper, guide)
- [ ] All form submissions → GHL with source tag
- [ ] Remove checkout/payment functionality

#### Cold Lead Warm-Up Campaign
Re-engagement sequence for existing GHL cold leads:
1. Value-add email (industry insight, not salesy)
2. Case study / success story
3. Product update (exosome launch)
4. Direct offer (consultation, pricing)
5. Breakup email

#### Agent F4 — Sales Pipeline Manager
- Daily: new leads, stage movements, stale leads (no activity 7 days)
- Pre-call briefs for Jeff before every scheduled call
- Lead score updates based on engagement
- Alert on high-value leads (>$50K potential)
- Weekly pipeline report: volume, conversion, pipeline value

#### Jeff's Onboarding Docs Integration
- Once Jeff completes onboarding documentation → build into GHL "Onboarding" stage
- Automate document delivery and signature tracking
- Agent monitors completion → triggers order flow

### Phase 2 Deliverables
- ✅ GHL pipeline fully built
- ✅ Lead scoring operational
- ✅ 3dexosomes.com = lead gen funnel
- ✅ Cold leads being warmed
- ✅ Call scheduling automated
- ✅ Agent F4 managing pipeline daily
- ✅ Jeff focused on calls and relationships

---

## Phase 3: Customer Lifecycle + Optimization (Weeks 8-12)

### Agent F3 — Customer Communications
Extends the 3 order emails (Phase 1A) to full lifecycle:

**Post-delivery:**
- Day 7: "How's everything? Questions about the product?"
- Day 30: "Checking in — how are results?"
- Day 60: Satisfaction survey

**Re-order engine:**
- Calculate reorder window by product type
- Reminder → follow-up → "ready to reorder?" with WooCommerce link

**Inbound triage:**
- Order status → auto-answer from tracking data
- Product question (non-medical) → auto-answer from knowledge base
- Medical/clinical → ESCALATE TO HUMAN IMMEDIATELY
- Complaint → escalate to Jeff/Todd
- Reorder request → send link or offer concierge order

**⚠️ Constraint: NO medical claims. NO clinical advice. ALL templates reviewed.**

### System Optimization
- Measure end-to-end: lead → close → order → delivery → reorder
- KPI dashboard (weekly from Clark to Todd):
  - Revenue, pipeline, operations, finance, customer metrics
- Tune agent escalation thresholds
- Document SOPs for all processes

---

## Phase 4 (Future): Scale & Expand

### Prospect Followup & Conversion
- Nurture sequences for unconverted prospects
- Multi-touch, multi-channel automation
- Conversion tracking and attribution
- Win/loss analysis
- Referral program automation

### Team Scaling
- Sales hire when Jeff is ready to hand off
- Agents scale with business — add specialized agents as needed

---

## Agent Architecture

```
┌──────────────────────────────────────────────┐
│              CLARK (Chief of Staff)            │
│                                                │
│  Orchestration · Escalation · Weekly report    │
│  Cross-agent coordination · Strategy           │
│                                                │
├──────────┬──────────┬──────────┬──────────────┤
│          │          │          │              │
▼          ▼          ▼          ▼              │
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐    │
│  F1    │ │  F2    │ │  F3    │ │  F4    │    │
│  Book  │ │ Order  │ │ Comms  │ │ Sales  │    │
│ keeper │ │  Ops   │ │        │ │Pipeline│    │
│        │ │        │ │        │ │        │    │
│ Xero   │ │ WooC   │ │ GHL    │ │ GHL    │    │
│ Bank   │ │ ShipSt │ │ Email  │ │ CRM    │    │
│ feeds  │ │ FedEx  │ │ SMS    │ │ Cal    │    │
│        │ │ GHL    │ │        │ │ Score  │    │
└────────┘ └────────┘ └────────┘ └────────┘    │
└──────────────────────────────────────────────┘
```

---

## Budget

### Ongoing Monthly
| Item | Cost |
|------|------|
| Xero (Growing) | $50 |
| Make.com (Pro) | $75 |
| Agent compute (API) | ~$200 |
| GHL, WooCommerce, ShipStation | existing |
| **Total new monthly** | **~$325** |

### One-Time
| Item | Cost |
|------|------|
| Contract bookkeeper (QBO cleanup) | $2,000-4,000 |
| Xero migration | $500 |
| Make.com automation build | $1,000 |
| GHL pipeline setup | $500 |
| **Total one-time** | **$4,000-6,000** |

### Year 1: ~$8,000-10,000 | Remaining from $75K: ~$65,000-67,000

---

## Open Questions

1. **Stripe on WooCommerce** — add card payments alongside ACH? Reduces friction for smaller exosome orders.
2. **External accountant** — do you have one for tax filing? Needs to know about Xero migration.
3. **Jeff's onboarding docs** — timeline? We integrate into GHL once ready.
4. **Product catalog** — all SKUs listed on mounthydra.com? Any gaps before exosome expansion?
5. **Compliance counsel** — any regulatory relationship for reviewing customer comms about biologics?
6. **Applicant approval criteria** — what does Jeff/Todd look for when approving? Can we build a scoring rubric?

---

## Immediate Next Steps

| # | Action | Owner | Target |
|---|--------|-------|--------|
| 1 | Answer remaining open questions | Todd | This week |
| 2 | Clark audits WooCommerce, ShipStation, PayNote, GHL APIs | Clark | Week 1 |
| 3 | Clark begins QBO forensic audit | Clark | Week 1 |
| 4 | Walk through a live order end-to-end with Jeff | Clark + Jeff | Week 1 |
| 5 | Set up Make.com account | Todd (payment) / Clark (config) | Week 1 |
| 6 | Draft 3 customer email templates | Clark | Week 1 |
| 7 | Compile QBO correction document for bookkeeper | Clark | Week 2 |

---

*Living document. Updated as decisions are made and phases execute.*
*Workspace: projects/ops-buildout/PLAN.md*
