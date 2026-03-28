import os
import httpx
import re
import json
from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
from pydantic import BaseModel
from groq import Groq
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware;
from dotenv import load_dotenv;
app = FastAPI()

# Enable CORS for React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv(os.path.join("..", ".env"))
# 1. Initialize Groq (Replace with your actual key or use env variables)
# Pro-tip: For the final submission, ensure this key is active or moved to .env
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=GROQ_KEY)
class AuditMetrics(BaseModel):
    url: str
    word_count: int
    headings: dict
    cta_count: int
    links_internal: int
    links_external: int
    image_count: int
    images_missing_alt_pct: float
    meta_title: Optional[str]
    meta_description: Optional[str]

def update_prompt_logs(system_prompt: str, user_prompt: str, structured_input: dict, raw_output: str):
    """
    Overwrites logs.md with the latest audit data to fulfill the 
    Prompt Logs (Required Deliverable).
    """
    log_content = f"""# AI Layer Prompt Logs (Latest Audit)

## 1. System Prompt Used
```text
{system_prompt}
```

## 2. User Prompt Construction
```
{user_prompt}
```

## 3. Structured Inputs Sent to Model
```
{json.dumps(structured_input, indent=2)}
```

## 4. Raw Model Output (Before Formatting)
```
{raw_output}
```
"""
    # 'w' mode ensures the file is refreshed with every new audit
    file_path = os.path.join("..", "logs.md") 
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(log_content)    

def scrape_factual_metrics(url: str, html: str) -> AuditMetrics:
    """Extracts key factual metrics required by the assignment."""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Text and Word Count
    text = soup.get_text(separator=' ', strip=True)
    words = re.findall(r'\w+', text)

    # Heading hierarchy (H1-H3)
    headings = {
        "h1": len(soup.find_all('h1')),
        "h2": len(soup.find_all('h2')),
        "h3": len(soup.find_all('h3'))
    }

    # Detect CTAs (buttons or links with primary action classes)
    ctas = soup.find_all(['button', 'a'], class_=re.compile(r'btn|button|cta', re.I))
    
    # Link Analysis
    links = soup.find_all('a', href=True)
    internal = [l for l in links if url in l['href'] or l['href'].startswith('/')]

    # Image and Accessibility Analysis
    images = soup.find_all('img')
    missing_alt = [img for img in images if not img.get('alt')]
    alt_pct = (len(missing_alt) / len(images) * 100) if images else 0

    return AuditMetrics(
        url=url,
        word_count=len(words),
        headings=headings,
        cta_count=len(ctas),
        links_internal=len(internal),
        links_external=len(links) - len(internal),
        image_count=len(images),
        images_missing_alt_pct=round(alt_pct, 2),
        meta_title=soup.title.string if soup.title else "Missing",
        meta_description=soup.find("meta", attrs={"name": "description"}).get("content") if soup.find("meta", attrs={"name": "description"}) else "Missing"
    )

@app.get("/audit")
async def perform_audit(url: str):
    try:
        # Standard headers to prevent 403 Forbidden errors
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        }

        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(url, headers=headers, follow_redirects=True, timeout=15.0)
            response.raise_for_status()
        
        # 1. Deterministic Scraping (Factual Metrics)
        metrics = scrape_factual_metrics(url, response.text)
        
        # 2. Define Prompting Strategy
        system_content = (
    "You are a professional Website Strategist. Analyze the provided metrics and return a VALID JSON object. "
    "CRITICAL: Do not use single quotes or unescaped characters. Ensure all property names and string values are enclosed in double quotes. "
    "For every category, write exactly 1-2 full sentences. Include at least 5 recommendations. "
    "Do not use '_' between words in your sentences. Instead, use spaces. For example, write 'SEO structure' instead of 'seo_structure'. "
    "Use **markdown bolding** for key terms and metrics within your sentences, but ensure they are inside valid JSON strings.\n\n"
    
    "REQUIRED JSON SCHEMA:\n"
    "{\n"
    "  \"seo_structure\": \"...\",\n"
    "  \"messaging_clarity\": \"...\",\n"
    "  \"cta_usage\": \"...\",\n"
    "  \"content_depth\": \"...\",\n"
    "  \"ux_structural_concerns\": \"...\",\n"
    "  \"recommendations\": [\n"
    "    { \"insight\": \"...\", \"reasoning\": \"...\" }\n"
    "  ]\n"
    "}"
)
        user_content = f"Audit this data: {metrics.model_dump_json()}"

        # 3. AI Layer Orchestration (Using Groq/Llama-3)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        
        raw_ai_output = chat_completion.choices[0].message.content

        # 4. Automate Deliverable: Prompt Logs
        update_prompt_logs(
            system_prompt=system_content,
            user_prompt=user_content,
            structured_input=metrics.model_dump(),
            raw_output=raw_ai_output
        )

        return {
            "factual_metrics": metrics,
            "ai_insights": raw_ai_output
        }

    except Exception as e:
        # Detailed error handling for frontend feedback
        raise HTTPException(status_code=400, detail=str(e))
