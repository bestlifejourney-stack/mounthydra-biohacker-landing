# Dry-Ice Shipping Cost Analysis — Getting Under $100/Shipment

**Prepared for:** Todd Tzeng, Mount Hydra
**Date:** 2026-07-30
**Origin assumed:** SCEQL Labs, Irvine, CA 92614 (current flow: WooCommerce → ShipStation → FedEx)
**Target:** land the typical dry-ice shipment (≈5 lb payload, currently >$150) under $100

> **Data caveat.** I don't have the actual ShipStation/carrier invoice export in this repo, so the
> per-lane dollar figures below are **modeled estimates** built from FedEx/UPS published 2026 rate
> structure, surcharge schedules, and the dimensional-weight rules — not your negotiated contract
> rates. The *ranking of levers* and *break-even logic* are solid regardless. To turn these into exact
> numbers, pull the export described in the appendix and I'll rerun the math against real lanes.

---

## 1. Why the shipments cost >$150 (the diagnosis)

The cost is **not** primarily the dry ice. Dry ice itself is cheap. Three things stack up:

| Cost driver | What's happening | Rough contribution |
|---|---|---|
| **Overnight air, long zone** | Frozen exosomes from CA to East Coast/Midwest is Zone 7–8. To keep the payload frozen in transit, orders go **Priority/Standard Overnight**. That single line is the biggest cost. | **$120–160** |
| **Dimensional weight** | A 5 lb payload ships in a bulky EPS cooler. FedEx bills the **greater of actual vs. dimensional weight** (divisor 139). A 12×12×11 in cooler = 1,584/139 ≈ **12 lb billable** — you're paying for 12 lb, not 5. A 13×13×13 cooler bills at ~16 lb. | **+$30–70** |
| **Surcharges + materials** | Dry-ice surcharge **$8.50/pkg** (2026), residential + delivery-area surcharges (~$10), fuel surcharge (~16% of base), plus packaging (~$10–18) and dry-ice material (~$6–12). | **+$35–45** |

**Modeled reference shipment** — Irvine CA → NYC (Zone 8), 5 lb payload, 12×12×11 cooler (12 lb billable):

| Service | Est. carrier cost* | + surcharges/materials | **Landed** | Transit | Dry-ice viable? |
|---|---|---|---|---|---|
| **Priority Overnight** | ~$150 | ~$35 | **~$185** | 1 day | Yes (today's default) |
| **Standard Overnight** | ~$135 | ~$35 | **~$170** | 1 day (later) | Yes |
| **2Day** | ~$75 | ~$35 | **~$110** | 2 days | Only if payload validated ≥72–96h |
| **Ground/Home Delivery** | ~$40 | ~$35 | **~$75** | **5 days** | **No** — dry ice sublimates first |

*Carrier cost = estimated FedEx list rate at ~12 lb billable to Zone 8, less an assumed ~30% negotiated/ShipStation discount. Your real number depends on your contract.

The takeaway: **ground is cheap but impossible cross-country on dry ice; overnight is viable but expensive.** Every lever below is about escaping that trap.

---

## 2. The levers, ranked by ROI and speed to deploy

### Lever 1 — Right-size the shipper (kill dimensional weight) · *near-zero capex, this month*
Your 5 lb payload is almost certainly being **billed at 11–17 lb** because the cooler is oversized. Switch
to a **right-sized high-performance shipper** — a vacuum-insulated-panel (VIP) box or a slimmer EPS
system engineered for the exosome payload. This does three things at once:
- Drops billable weight (12 lb → ~7–8 lb) → **~$20–40 off the carrier line**.
- Holds temperature with **less dry ice** → lower material + surcharge exposure.
- A better-insulated box **extends hold time**, which unlocks Lever 3 (downgrade to 2Day).

**Est. saving: $30–60/shipment. No operational change. Do this first.**

### Lever 2 — Rate-shop carriers, add UPS, least-cost routing · *this month*
You're FedEx-only today. UPS typically runs **15–25% cheaper on cold-chain lanes**. Add a UPS account,
turn on **automatic rate-shopping in ShipStation** so each order picks the cheapest qualifying service,
and — even at modest volume — **negotiate off list** with both carriers (the ~30% discount assumed above
is conservative; cold-chain shippers often do better).

**Est. saving: 15–25% on the carrier line (~$20–35/shipment).**

### Lever 3 — Downgrade service where transit + validated hold time allow · *1-time validation*
Overnight is only mandatory because the package can't hold frozen long enough for a slower service.
Do a **one-time thermal validation** (data loggers in a live box across your worst-case lane) to prove
the qualified shipper holds ≥72–96h. Once proven, most Zone 5–8 lanes move on **2Day instead of Priority
Overnight**, roughly **halving** the carrier line.

**Est. saving: $40–100/shipment on downgraded lanes. Biggest single lever, gated by validation.**

### Lever 4 — Distributed cold-storage warehousing · *structural, justify with volume*
Stock inventory at 1–2 additional **frozen 3PL nodes** so most orders ship a **short zone** at 2Day or
even ground. This is the structural fix that permanently removes the cross-country-overnight problem.

- **Ideal footprint already exists:** Cold Chain 3PL operates **Pacoima CA (west) + Chicago (central) +
  Baltimore MD (east)** — frozen-capable, does dry-ice packaging. An East node (Baltimore) puts ~80% of
  the US population within Zone 2–4 / 1–2-day ground of a node.
- **Effect:** a $150+ coast-to-coast overnight becomes a **$40–70 short-zone 2Day/ground** shipment.
- **Cost to add:** frozen storage ~**$36/pallet/month** base + receiving + pick/pack (~$3–6/order) +
  the working-capital and **FEFO/expiry management** of splitting biologic inventory across sites.

**Break-even:** if a node saves ~$80/shipment and adds ~$8–10 handling, net ≈ **$65–70 saved per order**
routed through it, against ~$200–500/month of fixed storage + minimums. So an East-Coast node pays for
itself once you're clearing roughly **8–12+ frozen cross-country orders/month**. At ~$38K/mo today that
may be premature; as you push toward the $100K/mo target it becomes the right move — build the plan now,
pull the trigger on volume.

---

## 3. Recommendation — phased

**Phase 1 (this month, near-zero capex):** right-size the shipper (L1) + add UPS and least-cost routing
(L2) + run the thermal validation to unlock 2Day (L3).
→ Modeled result on the reference lane: **~$80–110 landed, under $100 on the majority of lanes.**

**Phase 2 (trigger at ~10+ frozen cross-country orders/month):** add an East-Coast frozen 3PL node (L4),
optionally Central.
→ Modeled result: **~$50–70 landed**, and faster/lower-risk delivery for East/Midwest customers.

Phase 1 alone very likely gets you under the $100 target on most shipments. Phase 2 is what makes <$100
structural and durable as volume scales.

---

## 4. What I need to make this exact

The estimates above become hard numbers with a **ShipStation export of the last 90 days** including,
per shipment:
1. **Billed weight** and **package dimensions** (to quantify how much dim-weight inflation you're eating)
2. **Origin + destination ZIP** and **zone**
3. **Service level** used (Priority Overnight / 2Day / etc.)
4. **Itemized surcharges** (dry ice, residential, DAS, fuel)
5. **Actual paid amount** per shipment
6. **Destination geography distribution** (how many orders go East/Central vs. West — this sizes the 3PL case)

With that I can compute exact per-lane savings for each lever and the precise 3PL break-even.

---

## Sources
- FedEx 2026 dry-ice surcharge ($8.50/pkg) & ground hazmat fee ($57.25): [ParcelPath – FedEx Dry Ice Shipping Cost](https://parcelpath.com/shipping-companies/fedex/fedex-dry-ice-shipping-cost/), [FedEx 2026 surcharge & fee changes (PDF)](https://www.fedex.com/content/dam/fedex/us-united-states/services/surcharge_and_fee_changes_2026.pdf)
- FedEx 5.9% GRI 2026 & rate structure: [AFMS](https://afms.com/fedex-announces-5-9-general-rate-increase-for-2026/), [Shipware 2026 rate guide](https://shipware.com/blog/what-are-fedex-shipping-rates/)
- 5 lb Priority Overnight vs 2Day zone examples: [ParcelPath – FedEx Overnight Rates](https://parcelpath.com/carrier-services/delivery-tracking/fedex-overnight-rates/)
- Dimensional weight divisor 139 (2026) & billable-weight rule: [ScaleBlog](https://scaleblog.com/what-is-dimensional-weight-shipping/), [vMeasure](https://vmeasure.ai/fedex-dim-weight-formula/)
- UPS ~15–25% cheaper on cold lanes / frozen shipping: [ShipFare – Does UPS Ship Frozen Food](https://shipfare.com/blog/does-ups-ship-frozen-food)
- Cold-chain 3PL footprint (Pacoima/Chicago/Baltimore) & frozen fulfillment: [Cold Chain 3PL](https://coldchain3pl.com/), [Fulfill.com – Cold Chain 3PL profile](https://www.fulfill.com/3pl/profile/cold-chain-3pl)
- Frozen storage pricing (~$36/pallet/mo base): [WarehousingCosts.com cold storage calculator](https://warehousingcosts.com/tools/cold-storage-cost-calculator), [AMZ Prep cold storage calculator](https://amzprep.com/cold-storage-cost-calculator/)
