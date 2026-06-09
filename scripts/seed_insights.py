"""
StockIQ Static Insights
Pre-written narrative insights for all 10 MVP stocks.
These are used as fallbacks or when no Anthropic API key is set.
Each insight is ~100-150 words per section.
"""

STATIC_INSIGHTS = {
    "TCS": {
        "about_company": (
            "Tata Consultancy Services (TCS) is India's largest IT services company and one of "
            "the most valuable companies in the country. Founded in 1968 and listed in 2004, "
            "TCS provides IT consulting, outsourcing, and business solutions to clients across "
            "more than 50 countries. Its key verticals include BFSI, retail, manufacturing, and "
            "life sciences. TCS is part of the Tata Group conglomerate and is known for its "
            "people-first culture, low attrition compared to peers, and strong execution. With "
            "over 600,000 employees worldwide, TCS benefits from massive scale and long-term "
            "partnerships with Fortune 500 companies."
        ),
        "future_scope": (
            "The global IT services market is expected to grow steadily, driven by digital "
            "transformation, cloud adoption, and AI integration across industries. TCS is "
            "well-positioned to benefit through its growing cloud services practice, "
            "AI-powered automation offerings, and partnerships with hyperscalers like AWS, "
            "Azure, and Google Cloud. Emerging markets and BFSI modernisation represent "
            "significant expansion opportunities. TCS's large deal pipeline, particularly in "
            "Europe and North America, provides strong revenue visibility. The company's "
            "investment in proprietary platforms and reskilling employees at scale is a "
            "structural advantage for long-term growth."
        ),
        "risks": (
            "TCS faces risks from currency fluctuations, as most revenue is in USD while "
            "costs are partly in INR. A slowdown in BFSI or retail spending — its largest "
            "verticals — could impact deal flows. Rising competition from Accenture, "
            "Cognizant, and HCL, along with the emergence of AI-based automation, could "
            "compress margins over the medium term. Visa and immigration policy changes in "
            "the US affect staffing flexibility. High dependence on a few large clients adds "
            "concentration risk. Additionally, any significant global recession could delay "
            "client IT budgets."
        ),
        "investment_thesis": (
            "TCS is a classic Stalwart — a large, consistently profitable business with "
            "steady growth in the 8–15% range, high returns on equity exceeding 50%, "
            "minimal debt, and reliable dividend payouts. It doesn't need to take big risks "
            "to grow because its scale, brand, and client relationships create compounding "
            "advantages. For long-term investors seeking lower-volatility exposure to India's "
            "IT sector, TCS offers predictable earnings growth backed by strong governance, "
            "the Tata brand, and a diversified global client base."
        ),
    },
    "INFY": {
        "about_company": (
            "Infosys is India's second-largest IT services company, founded in Pune in 1981 "
            "and headquartered in Bengaluru. The company offers a wide range of services "
            "including IT consulting, software development, business process outsourcing, and "
            "cloud transformation. Infosys serves over 1,800 clients across banking, insurance, "
            "manufacturing, and energy sectors. With a strong US and European presence, it "
            "competes directly with TCS, Wipro, and global giants like Accenture. Infosys is "
            "known for its high engineering talent, campus recruitment programs, and a series "
            "of digital-first acquisitions in recent years to boost capabilities in cloud and AI."
        ),
        "future_scope": (
            "Infosys is betting heavily on its AI-first strategy called Topaz, which aims to "
            "embed generative AI across its service offerings. The company's cloud migration "
            "capabilities are growing rapidly, particularly in BFSI and manufacturing. Growth "
            "in Europe — through recent acquisitions and partnerships — should offset slower "
            "demand from North America in the near term. The rise of AI tools may create new "
            "service lines around AI governance, integration, and implementation, which Infosys "
            "is actively targeting. With a large engineering workforce and strong brand "
            "recognition, Infosys remains well placed to capitalise on enterprise tech spending."
        ),
        "risks": (
            "Infosys has faced revenue growth pressure in FY24, with clients cutting "
            "discretionary IT spending amid macroeconomic uncertainty. Its lower promoter "
            "holding compared to TCS means it is more susceptible to market-driven "
            "governance pressures. Currency headwinds, particularly INR appreciation against "
            "USD, reduce realisations. The transition from legacy outsourcing to AI-enabled "
            "automation could commoditise some of its core offerings. Additionally, high "
            "employee costs in a competitive talent market continue to pressure margins. "
            "Client concentration in BFSI remains a vulnerability."
        ),
        "investment_thesis": (
            "Infosys fits the Stalwart mould — a large, mature IT business with consistent "
            "profitability, high ROE above 30%, and a history of regular dividends and "
            "buybacks. While growth has moderated recently, it remains structurally tied to "
            "global enterprise technology spending, which has a long runway. Infosys trades "
            "at a moderate discount to TCS, offering a margin of safety. Its Topaz AI "
            "strategy and cloud capabilities add optionality. For investors seeking a "
            "dependable large-cap IT holding with strong cash flows and capital returns, "
            "Infosys is a compelling candidate."
        ),
    },
    "WIPRO": {
        "about_company": (
            "Wipro Limited is one of India's oldest and most recognised IT services companies, "
            "founded in 1945 as a vegetable oil company and pivoted into technology in the "
            "1980s. Today, Wipro provides IT consulting, cloud transformation, cybersecurity, "
            "and engineering services to clients across 65 countries. Its major verticals "
            "include BFSI, healthcare, communications, and manufacturing. Wipro has made "
            "several acquisitions over the past decade — including Capco and Rizing — to "
            "build depth in banking and SAP consulting. With a 72% promoter stake held by the "
            "Premji family, it has a stable ownership structure."
        ),
        "future_scope": (
            "Wipro's strategic focus areas — cloud, data analytics, AI, and cybersecurity — "
            "align with long-term enterprise technology trends. The company's recent "
            "restructuring into four global business lines is expected to improve client "
            "relationship management and cross-selling. Acquisitions in Europe and the "
            "Americas have expanded its addressable market. Wipro is also investing in its "
            "AI360 strategy, which embeds AI across all service lines. A recovery in "
            "discretionary IT spending globally, particularly from BFSI and telecom clients, "
            "could drive improved growth in FY26 and beyond."
        ),
        "risks": (
            "Wipro has underperformed its IT peers in revenue growth over the past few years, "
            "losing market share to Infosys and HCL. Revenue declined 4.4% in FY24, raising "
            "questions about demand recovery timelines. Its margin trajectory has been under "
            "pressure from higher employee costs and integration expenses of acquired "
            "companies. Dependency on a few large BFSI and telecom clients introduces "
            "concentration risk. Currency headwinds and potential visa/immigration policy "
            "changes in key markets (US and UK) could further impact profitability. "
            "Leadership transitions have added to near-term uncertainty."
        ),
        "investment_thesis": (
            "Wipro is a Stalwart that is currently facing a soft growth phase. Its long "
            "operating history, debt-light balance sheet, and stable promoter backing provide "
            "a solid foundation. The stock's P/E is at a modest discount to TCS and Infosys, "
            "partly reflecting slower growth expectations. For patient investors, Wipro "
            "offers a recovery play within the IT sector — if it executes on its AI360 and "
            "restructuring strategy, earnings growth could re-accelerate. Its strong free "
            "cash flow generation provides downside support even during periods of tepid "
            "revenue growth."
        ),
    },
    "PERSISTENT": {
        "about_company": (
            "Persistent Systems is a mid-cap IT services company headquartered in Pune, "
            "specialising in digital engineering, cloud modernisation, and product development "
            "services. Founded in 1990, it was initially known for outsourced product "
            "development before expanding into enterprise software services. Key clients include "
            "technology companies in North America and Europe. Persistent has one of the "
            "strongest growth profiles in the Indian IT sector, with revenue growing at nearly "
            "29% CAGR over five years. The company has consistently delivered strong margins "
            "and earned a premium valuation. Partnerships with Salesforce, AWS, and Azure are "
            "central to its go-to-market strategy."
        ),
        "future_scope": (
            "Persistent is targeting USD 2 billion in annual revenue and sees a massive "
            "opportunity in AI-assisted software engineering and cloud platform services. "
            "Its early investments in AI-led development tools and strong partnerships with "
            "hyperscalers give it a competitive edge. The healthcare, BFSI, and software "
            "verticals in North America offer significant headroom. Persistent's ability to "
            "work with both ISVs (independent software vendors) and large enterprises is a "
            "unique differentiator. New-age digital services such as GenAI integration, "
            "platform engineering, and data modernisation represent high-growth demand areas "
            "where Persistent is particularly strong."
        ),
        "risks": (
            "At a P/E of 64x, Persistent is priced for near-perfect execution. Any "
            "deceleration in revenue growth — caused by client budget freezes, macroeconomic "
            "headwinds, or talent attrition — could trigger a sharp re-rating. The company "
            "is heavily dependent on North America, making it vulnerable to US economic cycles. "
            "Competition from larger peers with more resources is intensifying in the "
            "mid-market IT space. Talent costs remain high due to demand for skilled engineers "
            "in digital services. Key-man risk is a concern given its concentrated client "
            "relationships."
        ),
        "investment_thesis": (
            "Persistent Systems is a textbook Fast Grower — revenue and profit have compounded "
            "at over 28% and 42% respectively over five years, driven by strong execution in "
            "high-demand service areas. Unlike many IT peers, it has maintained growth "
            "acceleration even in a challenging macroeconomic environment. While the valuation "
            "is high, it reflects genuine business quality — strong ROE, minimal debt, and "
            "expanding margins. Investors who believe in India's mid-cap IT growth story and "
            "are comfortable with premium valuations will find Persistent a compelling "
            "long-term compounder."
        ),
    },
    "SAIL": {
        "about_company": (
            "Steel Authority of India Limited (SAIL) is a Maharatna public sector enterprise "
            "and one of India's largest integrated steel manufacturers. It operates five "
            "integrated steel plants and three special steel plants across Bhilai, Rourkela, "
            "Bokaro, Durgapur, and Burnpur. SAIL produces flat products, long products, "
            "pipes, and specialty steels for infrastructure, railways, defence, and "
            "construction sectors. As a government-owned entity, SAIL benefits from assured "
            "demand from state infrastructure projects. The company controls captive iron ore "
            "mines, reducing raw material dependency. With a market cap of ~₹41,000 crore, "
            "it is a significant player in India's steel landscape."
        ),
        "future_scope": (
            "India's infrastructure push — including roads, railways, housing, and defence "
            "modernisation — provides a strong long-term demand base for steel. SAIL is "
            "investing in capacity expansion and modernisation of its steel plants to improve "
            "efficiency and reduce costs. The China+1 strategy adopted by global manufacturers "
            "could increase demand for Indian steel exports. Government capex programmes like "
            "PM Gati Shakti and the National Infrastructure Pipeline are structural positives. "
            "SAIL's captive iron ore mines are a significant cost advantage compared to "
            "privately sourced raw materials."
        ),
        "risks": (
            "SAIL's profitability is highly sensitive to global steel prices, which are "
            "cyclical and can fall sharply when China dumps excess steel on global markets. "
            "In FY24, revenue fell 8.5% and profits dropped over 40% due to softening steel "
            "prices. High fixed costs from ageing plants weigh on margins during downturns. "
            "The company carries moderate debt, and capital expenditure for plant upgrades is "
            "significant. Being a PSU, SAIL may also face political interference in pricing "
            "and staffing decisions. Competition from private players like JSW Steel and "
            "Tata Steel, which operate more efficiently, is a structural headwind."
        ),
        "investment_thesis": (
            "SAIL is a classic Cyclical — its revenues and profits move in lockstep with "
            "steel prices and India's economic cycle. The stock's low P/B ratio (0.8x) "
            "indicates it trades below its book value, making it an interesting value "
            "proposition when the steel cycle turns. The key thesis is timing: invest when "
            "steel prices are depressed and sentiment is negative, exit when utilisation rates "
            "peak. SAIL is not a compounder — it rewards traders more than long-term holders. "
            "Investors who understand commodity cycle positioning will find SAIL attractive "
            "at current valuations."
        ),
    },
    "ADANIPOWER": {
        "about_company": (
            "Adani Power is India's largest private thermal power producer, with an installed "
            "capacity of over 15,250 MW across plants in Gujarat, Rajasthan, Maharashtra, "
            "Karnataka, and Chhattisgarh. Part of the Adani Group, the company generates "
            "electricity primarily from coal-fired plants under long-term power purchase "
            "agreements (PPAs) with state electricity boards. It has also benefited from "
            "government-backed tariff compensation adjustments in recent years. Listed since "
            "2009, Adani Power has significantly improved its financial health, reducing debt "
            "and generating strong profits. Its promoter holds nearly 75% of the company."
        ),
        "future_scope": (
            "India's rapidly growing electricity demand — driven by industrial expansion, "
            "urbanisation, and the EV transition — provides a structural tailwind for power "
            "producers. Adani Power is exploring renewable energy additions under the broader "
            "Adani Group green energy push. Capacity additions and renegotiated PPAs at "
            "higher tariffs offer revenue upside. India's peak power deficit presents "
            "opportunities for merchant power sales at premium rates. The government's "
            "focus on 24x7 electricity availability for all increases the need for reliable "
            "base-load capacity, where thermal power remains indispensable."
        ),
        "risks": (
            "Adani Power carries a debt-to-equity ratio of 1.8x, making it sensitive to "
            "interest rate changes. Dependence on imported coal exposes the company to "
            "global coal price volatility and currency risk. The stock has experienced "
            "sharp price swings following the 2023 Hindenburg Research report on the Adani "
            "Group, and reputational risk remains elevated. Long-term, the transition to "
            "renewable energy could structurally reduce demand for thermal power, affecting "
            "asset lifetimes. Regulatory changes in tariff structures or state DISCOMs' "
            "financial stress could impact payment realisations."
        ),
        "investment_thesis": (
            "Adani Power is a Cyclical operating in the power sector, with recent profits "
            "significantly elevated by favourable tariff orders and coal cost normalisation. "
            "Its P/E of 10.5x looks attractive, but investors must account for the cyclical "
            "nature of these profits, which may not be sustained at peak levels. The stock "
            "suits investors who understand the power cycle and the Adani Group's risk "
            "profile. Near-term profitability is strong, but the high leverage and "
            "regulatory dependencies mean this is not a low-risk holding. Position sizing "
            "and careful monitoring of coal prices are essential."
        ),
    },
    "ONGC": {
        "about_company": (
            "Oil and Natural Gas Corporation (ONGC) is India's largest oil and gas exploration "
            "and production company and a Maharatna public sector enterprise. It accounts for "
            "over 70% of India's domestic crude oil and natural gas production. ONGC operates "
            "both onshore and offshore fields, with its flagship Mumbai High field being one "
            "of the largest oil fields in Asia. The company also has downstream interests "
            "through HPCL and holds stakes in energy projects overseas. With a market cap "
            "above ₹3 lakh crore and consistent dividend payouts, ONGC is a cornerstone of "
            "India's energy security and a significant player in the public sector portfolio."
        ),
        "future_scope": (
            "India's growing energy demand presents long-term opportunities for ONGC, "
            "particularly in natural gas, which is a transitional fuel in the shift away "
            "from coal. The company is investing in deepwater exploration and enhanced oil "
            "recovery in its ageing fields to arrest production decline. ONGC's foray into "
            "renewable energy and green hydrogen through ONGC Green signals diversification "
            "intent. Improved crude oil prices, if sustained, would significantly boost "
            "operating profits. International operations through ONGC Videsh provide "
            "geographic diversification. Government-backed disinvestment or asset monetisation "
            "could unlock value."
        ),
        "risks": (
            "ONGC's fortunes are highly correlated with global crude oil prices, which are "
            "volatile and subject to geopolitical shocks. Government pricing controls — "
            "including subsidised fuel and gas price caps — limit the company's ability to "
            "fully benefit from high oil prices. Ageing oil fields result in natural "
            "production decline, requiring heavy reinvestment to maintain output levels. "
            "As a PSU, ONGC faces political risks around operational decisions, dividend "
            "expectations, and strategic direction. The global energy transition poses a "
            "longer-term structural risk to fossil fuel demand."
        ),
        "investment_thesis": (
            "ONGC is a Cyclical with Asset Play characteristics. Its P/B ratio of under 1x "
            "means investors are essentially buying its vast oil and gas reserves at a "
            "discount to book value — a classic asset play. The dividend yield of 4.5% "
            "provides an income cushion during price troughs. The investment case hinges "
            "on crude oil prices remaining above USD 70/barrel, which covers ONGC's "
            "breakeven costs comfortably. For contrarian investors comfortable with PSU "
            "risks, ONGC offers deep value with significant upside if energy prices stay "
            "elevated and the government reduces subsidy burden."
        ),
    },
    "VEDL": {
        "about_company": (
            "Vedanta Limited is one of India's largest diversified natural resources companies, "
            "with operations spanning zinc, lead, silver, aluminium, copper, iron ore, and oil "
            "and gas. It is the Indian listed entity of Vedanta Resources, controlled by "
            "Anil Agarwal. Vedanta's flagship asset is Hindustan Zinc — one of the world's "
            "largest zinc-lead miners — which contributes the majority of its profits. "
            "The company also operates oil fields through Cairn India in Rajasthan. Vedanta "
            "is known for paying high dividends, sometimes funded by debt or asset sales, "
            "which has attracted both income-seeking investors and raised governance questions."
        ),
        "future_scope": (
            "Vedanta is pursuing a demerger into six separate listed entities — each covering "
            "a distinct commodity business — which could unlock significant value by allowing "
            "each business to be valued on its own merits. The aluminium business has "
            "significant growth potential given India's rising industrial demand and the "
            "government's PLI push for downstream aluminium products. Hindustan Zinc's silver "
            "production expansion is on track. Semiconductor-grade materials and specialty "
            "metals are longer-term opportunities aligned with India's electronics "
            "manufacturing ambition. A recovery in commodity prices globally would benefit "
            "all of Vedanta's businesses simultaneously."
        ),
        "risks": (
            "Vedanta carries significant debt at a holding company level (Vedanta Resources), "
            "which creates refinancing risk and pressure to extract cash from the Indian "
            "listed entity through dividends. The company's debt-to-equity ratio of 1.95x "
            "is high, and interest coverage of 2.8x leaves limited buffer. Commodity price "
            "cycles — especially for zinc and aluminium — can sharply impact earnings. "
            "Governance concerns around related-party transactions and dividend policies "
            "are ongoing risks. Regulatory scrutiny in the mining sector and environmental "
            "compliance requirements add operational uncertainty."
        ),
        "investment_thesis": (
            "Vedanta is a Cyclical with elements of an Asset Play — it sits on world-class "
            "natural resource assets but is burdened by leverage at the group level. The "
            "dividend yield of 8.5% is eye-catching but partly debt-funded, making "
            "sustainability a valid concern. The demerger plan, if successful, could be a "
            "significant catalyst. Investors should approach this as a higher-risk, "
            "higher-reward commodity play — the upside is tied to commodity price recovery "
            "and successful deleveraging, while the downside is amplified by the holding "
            "company debt structure. Suitable only for risk-tolerant investors."
        ),
    },
    "YESBANK": {
        "about_company": (
            "Yes Bank is a private sector bank that underwent a crisis in 2020 when the "
            "Reserve Bank of India (RBI) imposed a moratorium due to mounting bad loans and "
            "governance failures. The bank was subsequently rescued through a government-led "
            "consortium involving SBI, LIC, and other financial institutions. Since the "
            "reconstruction, Yes Bank has been rebuilding its balance sheet under new "
            "management — focusing on retail and MSME banking, reducing wholesale loan "
            "concentration, and growing its deposit franchise. As of late 2024, it has "
            "returned to profitability, though ROE remains well below industry averages."
        ),
        "future_scope": (
            "Yes Bank's turnaround trajectory will depend on sustained execution in retail "
            "banking — growing CASA deposits, reducing NPAs, and improving net interest "
            "margins. The bank has a strong digital banking infrastructure that gives it "
            "a competitive edge in acquiring younger customers. If it can improve credit "
            "quality and capital efficiency to match peers over the next 3–5 years, "
            "there is significant re-rating potential. SBI's backstop ownership provides "
            "confidence to depositors. A recovery in small business lending and a focus "
            "on fee-based income could improve profitability metrics over time."
        ),
        "risks": (
            "Yes Bank's ROE of just 4.2% and thin margins indicate it is still in early "
            "stages of recovery. NPAs, while declining, remain above comfortable levels. "
            "Zero promoter holding means there is no natural anchor shareholder with "
            "skin in the game for long-term value creation. The bank's high debt-to-equity "
            "ratio (9.2x, typical for banks but elevated for Yes Bank's recovery stage) "
            "leaves little room for error. Intense competition from HDFC Bank, ICICI Bank, "
            "and newer digital banks makes customer acquisition expensive. Any reversal in "
            "credit quality or regulatory action could derail the recovery."
        ),
        "investment_thesis": (
            "Yes Bank is a classic Turnaround — a business that collapsed due to structural "
            "failures but has been rebuilt under new management with government backing. "
            "The numbers show genuine improvement: profit grew 140% in FY24, revenue is "
            "rising, and the worst of the NPA cycle appears to be behind. At a P/B of 1.2x, "
            "it's priced modestly for a recovery story. The key risk is execution — the bank "
            "must sustain profitability improvement over multiple quarters to justify continued "
            "investor confidence. This is a high-conviction trade for those who believe the "
            "turnaround is real and have the patience to hold through a multi-year recovery arc."
        ),
    },
    "RELIANCE": {
        "about_company": (
            "Reliance Industries Limited (RIL) is India's largest private sector company "
            "and one of the country's most recognised conglomerates. Originally an oil refining "
            "and petrochemicals business, Reliance has transformed itself under Mukesh Ambani "
            "into a diversified platform spanning energy, retail (Reliance Retail), and "
            "telecom (Jio). Jio disrupted the Indian telecom market with cheap data plans and "
            "now commands over 400 million subscribers. Reliance Retail is the country's "
            "largest retailer by revenue. The energy business remains the cash engine, "
            "funding investments in green energy and new commerce. RIL's market cap exceeds "
            "₹17 lakh crore, making it India's most valuable company."
        ),
        "future_scope": (
            "Reliance has announced a $75 billion investment plan in clean energy, including "
            "solar manufacturing, green hydrogen, and battery storage under its New Energy "
            "business. Jio is expanding into 5G, enterprise services, and financial services "
            "(Jio Financial Services). Reliance Retail is targeting to become one of the "
            "world's top 10 retailers through store expansion and e-commerce integration. "
            "The planned IPOs of Jio and Reliance Retail could be landmark events that "
            "unlock significant value for shareholders. India's growing consumer class and "
            "digital adoption across rural areas provide a massive runway for both Jio and "
            "Retail businesses."
        ),
        "risks": (
            "Reliance's conglomerate structure means investors need to track multiple "
            "businesses simultaneously — the refining cycle, telecom competition (Airtel), "
            "and retail execution. The new energy segment requires massive capital deployment "
            "with uncertain near-term returns. High capital expenditure — over ₹1.5 lakh "
            "crore committed — pressures free cash flow. Delayed IPOs of Jio and Retail "
            "would defer value unlocking. Competition in retail from D-Mart, Amazon, and "
            "Flipkart is fierce. Regulatory risk in telecom and petroleum pricing "
            "remain. Debt, while manageable, is significant in absolute terms."
        ),
        "investment_thesis": (
            "Reliance is a Stalwart of the highest order — it consistently delivers 13–15% "
            "revenue CAGR across business cycles, backed by irreplaceable assets in refining, "
            "telecom, and retail. The stock does not need a turnaround or a cycle upturn; "
            "it grows steadily through structural expansion of India's consumer economy. "
            "The optionality from Jio and Retail IPOs, combined with the green energy "
            "transformation, adds upside beyond what the current P/E reflects. For investors "
            "seeking a single stock that captures India's economic growth story, Reliance "
            "remains the benchmark."
        ),
    },
}


def seed_insights():
    """Insert static insights for all 10 companies."""
    from app import db
    from app.models import Company, Classification, Insights
    from datetime import datetime

    inserted = 0
    for ticker, data in STATIC_INSIGHTS.items():
        company = Company.query.filter_by(ticker=ticker).first()
        if not company:
            print(f"  SKIP {ticker} — not found in DB")
            continue

        ins = Insights.query.filter_by(company_id=company.id).first()
        if not ins:
            ins = Insights(company_id=company.id)
            db.session.add(ins)

        ins.about_company    = data["about_company"]
        ins.future_scope     = data["future_scope"]
        ins.risks            = data["risks"]
        ins.investment_thesis = data["investment_thesis"]
        ins.generated_at     = datetime.utcnow()
        inserted += 1

    db.session.commit()
    print(f"  ✅ Seeded insights for {inserted} companies.")
