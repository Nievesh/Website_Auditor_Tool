# INSTRUCTIONS TO RUN APPLICATION LOCALLY 
## 1. Open a terminal and enter the backend folder.
```
cd backend
```

## 2. Start the Virtual Environent

  Mac/Linux
```
python3 -m venv venv
source venv/bin/activate
```

  Windows
```
python -m venv venv
venv\Scripts\activate
```

## 3. Install Dependencies

```
pip install -r requirements.txt
```


## 4. Add a `.env` file in the root directory
```
GROQ_API_KEY=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
```

## 5. Start the backend server
    
```
uvicorn app.main:app --reload
```

  
## 6. Open a second terminal and enter the frontend folder
```
cd frontend
```

## 7. Install Dependencies 
```
npm install
```

## 7. Start the frontend server
  ```
npm start
```
   

 ### Application runs at: `http://localhost:3000/`


-----------------------------------------------------------------------------------------------------------------------------------------------------------------
### Architecture Overview 

  - Backend: FastAPI (Python) handles the web scraping logic and coordinates the AI analysis layer.
  - AI Layer: Integration with the Groq API (Llama-3 model) to process extracted data and generate structured JSON insights.
  - Frontend: A React-based dashboard that displays factual metrics and AI recommendations in a clear, separate format.

### AI Design Decisions

  - The system is designed to force the LLM to output valid JSON objects to ensure the frontend can provide recommendations reliably and avoid common rendering errors.
  - The user prompt is constructed by embedding scraped data (word counts, heading hierarchies, etc.) directly into the prompt. This is done to prevent hallucinations and ensure non-generic insights .

### Trade-offs
  -  Prioritized speed and immediate insights/metrics over in-depth, complicated and technical audits to maintain clarity.
  
## Future Improvements with more Time
  - Adding a database (e.g., Supabase or PostgreSQL) to track audit history over time for recurring users.
  - Optimisations towards auditing websites, reducing time taken
  - More Visually Appealing Layout
  - Proper Application Deployment

