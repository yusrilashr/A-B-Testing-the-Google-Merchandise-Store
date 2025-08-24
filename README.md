# A/B Testing — Google Merchandise Store

This project analyzes **A/B Testing** data from the [Google Merchandise Store](https://shop.googlemerchandisestore.com/), an online shop selling Google-branded products. The analysis uses the `ga4_obfuscated_sample_ecommerce` dataset, available through the **BigQuery Public Datasets program**, which provides a three-month sample of obfuscated BigQuery event export data from **November 1, 2020 to January 31, 2021**.

---

## Goals
The goal of this project is to evaluate the effect of layout changes on user behavior and conversion.  

- **Variant A**: Original layout (baseline design).  
- **Variant B**: Simplified layout (proposed design).  

The A/B testing methodology is applied to assess differences in **UI/UX performance** between the two variants.

---

## Analysis Workflow
1. **Data Preparation**
   - Aggregate user-level data by variant.
   - Track key funnel events: `session_start`, `view_item`, `begin_checkout`, and `purchase`.

2. **Conversion Analysis**
   - Calculate conversion rates (checkout & purchase) for each variant.
   - Measure revenue per session.

3. **Statistical Testing**
   - Chi-Square Test for proportions.  
   - Z-Test for conversion rate differences.  

   Significance level: **α = 0.05**

4. **Funnel Visualization**
   - Compare drop-offs between stages (`view_item → checkout → purchase`) for A vs. B.

---

## Key Findings
- These results indicate a clear and statistically robust disparity, but in the unfavorable direction for Variant B.
- his underperformance is consistent across checkout conversions, purchase conversions, and revenue generation, suggesting that the simpler design may introduce usability barriers, reduce user engagement, or fail to effectively guide users through the funnel.
