# AI Layer Prompt Logs

## 1. System Prompt
```text
You are a professional Website Strategist. Analyze metrics and return a VALID JSON object. Use double quotes for all keys/strings. Write 1-2 sentences per category and at least 5 recommendations. Use **markdown bolding** for key terms (e.g., **SEO structure**) within strings. When bolding text, do not use '_' between words. Instead, use spaces (e.g., **SEO structure** not **SEO_structure**). REQUIRED JSON SCHEMA: { "seo_structure": "", "messaging_clarity": "", "cta_usage": "", "content_depth": "", "ux_structural_concerns": "", "recommendations": [{ "insight": "", "reasoning": "" }] }
```

## 2. User Prompt
```text
Audit this data: {"url":"https://dictionary.cambridge.org/dictionary/english/article","word_count":2552,"headings":{"h1":1,"h2":10,"h3":8},"cta_count":65,"links_internal":204,"links_external":309,"image_count":14,"images_missing_alt_pct":14.29,"meta_title":"ARTICLE | English meaning - Cambridge Dictionary","meta_description":"ARTICLE definition: 1. a piece of writing on a particular subject in a newspaper or magazine, or on the internet:  2…. Learn more."}
```

## 3. Inputs
```json
{
  "url": "https://dictionary.cambridge.org/dictionary/english/article",
  "word_count": 2552,
  "headings": {
    "h1": 1,
    "h2": 10,
    "h3": 8
  },
  "cta_count": 65,
  "links_internal": 204,
  "links_external": 309,
  "image_count": 14,
  "images_missing_alt_pct": 14.29,
  "meta_title": "ARTICLE | English meaning - Cambridge Dictionary",
  "meta_description": "ARTICLE definition: 1. a piece of writing on a particular subject in a newspaper or magazine, or on the internet:  2\u2026. Learn more."
}
```

## 4. Raw AI Output
```json
{
  "seo_structure": "The website has a well-structured **SEO structure** with a clear meta title and meta description, but could be improved with more descriptive alt tags for images.",
   "messaging_clarity": "The messaging is clear, with a concise meta description that accurately reflects the **page content** and a well-structured headings hierarchy.",
   "cta_usage": "The high **call-to-action** count may be overwhelming, consider streamlining or prioritizing the most important **CTAs** to improve user experience.",
   "content_depth": "The page has a substantial **word count** indicating comprehensive coverage of the topic, but may benefit from visual breaks or summaries to enhance **scannability**.",
   "ux_structural_concerns": "The presence of a large number of internal and external **links** may impact **page load times** and user navigation, consider implementing a more intuitive **link management system**.",
   "recommendations": [
      {
         "insight": "Optimize image alt tags to improve **image accessibility** and **SEO**.",
         "reasoning": "Currently, 14.29% of images are missing alt tags, which can negatively impact **search engine rankings** and user experience for visually impaired individuals."
      },
      {
         "insight": "Streamline **call-to-action** usage to reduce user overwhelm.",
         "reasoning": "With 65 **CTAs** on the page, users may experience decision paralysis, reducing the effectiveness of each individual **call-to-action**."
      },
      {
         "insight": "Implement a more robust **internal linking strategy** to enhance user navigation.",
         "reasoning": "The high number of internal **links** can make it difficult for users to find relevant information, consider using a more hierarchical or categorization-based approach."
      },
      {
         "insight": "Consider adding a **table of contents** or **summary sections** to improve **content scannability**.",
         "reasoning": "The substantial **word count** and multiple headings may make it difficult for users to quickly understand the page structure and find relevant information."
      },
      {
         "insight": "Monitor and optimize **page load times** to ensure a smooth user experience.",
         "reasoning": "The large number of internal and external **links**, as well as images, may impact **page load times**, consider using techniques like lazy loading or compressing images to mitigate this issue."
      }
   ]
}
```