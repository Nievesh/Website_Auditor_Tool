import os
import re
import json
import httpx
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv(os.path.join("..", ".env"))
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise RuntimeError("GROQ_API_KEY missing from environment")

app = FastAPI()
client = Groq(api_key=GROQ_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---
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

# --- PROMPTS ---
SYSTEM_PROMPT = (
    "You are a professional Website Strategist. Analyze metrics and return a VALID JSON object. "
    "Use double quotes for all keys/strings. Write 1-2 sentences per category and at least 5 recommendations. "
    "Use **markdown bolding** for key terms (e.g., **SEO structure**) within strings. "
    "When bolding text, do not use '_' between words. Instead, use spaces (e.g., **SEO structure** not **SEO_structure**). "
    "REQUIRED JSON SCHEMA: "
    "{ \"seo_structure\": \"\", \"messaging_clarity\": \"\", \"cta_usage\": \"\", "
    "\"content_depth\": \"\", \"ux_structural_concerns\": \"\", "
    "\"recommendations\": [{ \"insight\": \"\", \"reasoning\": \"\" }] }"
)

# --- UTILITIES ---
def log_audit_trace(system: str, user: str, inputs: dict, output: str):
    """Saves the required deliverable: Prompt Logs."""
    content = (
        f"# AI Layer Prompt Logs\n\n"
        f"## 1. System Prompt\n```text\n{system}\n```\n\n"
        f"## 2. User Prompt\n```text\n{user}\n```\n\n"
        f"## 3. Inputs\n```json\n{json.dumps(inputs, indent=2)}\n```\n\n"
        f"## 4. Raw AI Output\n```json\n{output}\n```"
    )
    with open(os.path.join("..", "logs.md"), "w", encoding="utf-8") as f:
        f.write(content)

def scrape_metrics(url: str, html: str) -> AuditMetrics:
    """Scrapes factual data independently of the AI layer."""
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    
    links = soup.find_all('a', href=True)
    internal = [l for l in links if url in l['href'] or l['href'].startswith('/')]
    images = soup.find_all('img')
    missing_alt = [i for i in images if not i.get('alt')]

    return AuditMetrics(
        url=url,
        word_count=len(re.findall(r'\w+', text)),
        headings={f"h{i}": len(soup.find_all(f'h{i}')) for i in range(1, 4)},
        cta_count=len(soup.find_all(['button', 'a'], class_=re.compile(r'btn|button|cta', re.I))),
        links_internal=len(internal),
        links_external=len(links) - len(internal),
        image_count=len(images),
        images_missing_alt_pct=round((len(missing_alt)/len(images)*100), 2) if images else 0,
        meta_title=soup.title.string if soup.title else "Missing",
        meta_description=(soup.find("meta", attrs={"name": "description"}) or {}).get("content", "Missing")
    )

# --- ROUTES ---
@app.get("/audit")
async def perform_audit(url: str):
    try:
        async with httpx.AsyncClient() as http:
            res = await http.get(url, headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=True, timeout=15.0)
            res.raise_for_status()

        metrics = scrape_metrics(url, res.text)
        user_msg = f"Audit this data: {metrics.model_dump_json()}"

        ai_res = client.chat.completions.create(
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_msg}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        
        raw_output = ai_res.choices[0].message.content
        log_audit_trace(SYSTEM_PROMPT, user_msg, metrics.model_dump(), raw_output)

        return {"factual_metrics": metrics, "ai_insights": raw_output}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))