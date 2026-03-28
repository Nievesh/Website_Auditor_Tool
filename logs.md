# AI Layer Prompt Logs (Latest Audit)

## 1. System Prompt Used
```text
You are a professional Website Strategist. Analyze the provided metrics and return a VALID JSON object. CRITICAL: Do not use single quotes or unescaped characters. Ensure all property names and string values are enclosed in double quotes. For every category, write exactly 1-2 full sentences. Include at least 5 recommendations. Do not use '_' between words in your sentences. Instead, use spaces. For example, write 'SEO structure' instead of 'seo_structure'. Use **markdown bolding** for key terms and metrics within your sentences, but ensure they are inside valid JSON strings.

REQUIRED JSON SCHEMA:
{
  "seo_structure": "...",
  "messaging_clarity": "...",
  "cta_usage": "...",
  "content_depth": "...",
  "ux_structural_concerns": "...",
  "recommendations": [
    { "insight": "...", "reasoning": "..." }
  ]
}
```

## 2. User Prompt Construction
```
Audit this data: {"url":"https://gemini.google.com/app/86446dd754df0ae2","word_count":4,"headings":{"h1":0,"h2":0,"h3":0},"cta_count":0,"links_internal":1,"links_external":0,"image_count":0,"images_missing_alt_pct":0.0,"meta_title":"‎Google Gemini","meta_description":"Meet Gemini, Google’s AI assistant. Get help with writing, planning, brainstorming, and more. Experience the power of generative AI."}
```

## 3. Structured Inputs Sent to Model
```
{
  "url": "https://gemini.google.com/app/86446dd754df0ae2",
  "word_count": 4,
  "headings": {
    "h1": 0,
    "h2": 0,
    "h3": 0
  },
  "cta_count": 0,
  "links_internal": 1,
  "links_external": 0,
  "image_count": 0,
  "images_missing_alt_pct": 0.0,
  "meta_title": "\u200eGoogle Gemini",
  "meta_description": "Meet Gemini, Google\u2019s AI assistant. Get help with writing, planning, brainstorming, and more. Experience the power of generative AI."
}
```

## 4. Raw Model Output (Before Formatting)
```
{
  "seo_structure": "The provided **meta_title** and **meta_description** are well defined, which is good for **search engine optimization** purposes, but the absence of **headings** such as **h1**, **h2**, or **h3** may negatively impact the overall **seo_structure**.",
   "messaging_clarity": "The **meta_description** clearly conveys the purpose of **Gemini**, but the overall **word_count** of 4 is very low and may not be enough to effectively communicate the value proposition, potentially lacking **messaging_clarity**.",
   "cta_usage": "The **cta_count** of 0 indicates that there are no clear **calls to action** on the page, which may hinder user engagement and conversion rates due to poor **cta_usage**.",
   "content_depth": "The **word_count** of 4 and the absence of **headings** and **images** suggest that the content is very thin and may not provide sufficient value to users, indicating a lack of **content_depth**.",
   "ux_structural_concerns": "The presence of only one **link** and the absence of **images** may lead to a poor user experience due to the lack of visual and interactive elements, causing significant **ux_structural_concerns**.",
   "recommendations": [
      { "insight": "Add more **headings** to structure the content and improve **seo_structure**", "reasoning": "This will help with **search engine optimization** and make the content more scannable for users." },
      { "insight": "Increase the **word_count** to provide more comprehensive information about **Gemini**", "reasoning": "This will help to improve **messaging_clarity** and provide more value to users." },
      { "insight": "Add clear **calls to action** to encourage user engagement and conversion", "reasoning": "This will help to improve **cta_usage** and increase the chances of users taking the desired actions." },
      { "insight": "Incorporate high-quality **images** to enhance the user experience and improve **content_depth**", "reasoning": "This will help to break up the content and make it more engaging for users, while also providing more context about **Gemini**." },
      { "insight": "Conduct a thorough **user experience** audit to identify and address any **ux_structural_concerns**", "reasoning": "This will help to identify areas for improvement and ensure that the website is providing the best possible experience for users." }
   ]
}
```
