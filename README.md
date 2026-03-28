INSTRUCTIONS TO RUN APPLICATION LOCALLY : 
  1. Open a terminal and enter the backend folder.
    "cd backend"

  2. Start the Virtual Environment

  Mac/Linux
    "python3 -m venv venv
    source venv/bin/activate"

  Windows
    "python -m venv venv
    venv\Scripts\activate"

  3. Download Dependencies

  "pip install
  3. Open a second terminal and enter the frontend folder.
  "cd frontend"

  4. Start the frontend server. 
  "npm start.

Architecture Overview 

  - Backend: FastAPI (Python) handles the web scraping logic and coordinates the AI analysis layer.
  - AI Layer: Integration with the Groq API (Llama-3 model) to process extracted data and generate structured JSON insights.
  - Frontend: A React-based dashboard that displays factual metrics and AI recommendations in a clear, separate format.

AI Design Decisions

  - Structured Output: The system is designed to force the LLM to output valid JSON objects to ensure the frontend can parse recommendations reliably and avoid common rendering errors.
  - Grounding Strategy: The user prompt is constructed by injecting raw scraped data (word counts, heading hierarchies, etc.) directly into the prompt to prevent hallucinations and ensure non-generic insights .

Trade-offs
  - Single Page Scope: To keep the solution well-scoped within the 24-hour timeframe, the tool focuses exclusively on single-page analysis rather than a full site crawl .
  - Simplicity vs. Depth: Prioritized immediate actionable insights and core factual metrics over complex SEO technical audits to maintain engineering clarity.
  
  
Future Improvements
  - Enhanced Scraping: Implementing more robust headless browsing (like Playwright or Selenium) to handle JavaScript-heavy sites more effectively.
  - Persistent History: Adding a database (e.g., Supabase or PostgreSQL) to track audit history over time for recurring users.

