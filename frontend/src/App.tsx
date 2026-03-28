import React, { useState } from 'react';
import axios from 'axios';

interface AuditData {
  factual_metrics: {
    word_count: number;
    headings: { h1: number; h2: number; h3: number };
    cta_count: number;
    links_internal: number;
    links_external: number;
    image_count: number;
    images_missing_alt_pct: number;
    meta_title: string;
    meta_description: string;
  };
  ai_insights: string;
}

const renderFormattedText = (text: string) => {
  if (typeof text !== 'string') return text;
  const parts = text.split(/(\*\*.*?\*\*)/g);
  return parts.map((part, index) => 
    part.startsWith('**') && part.endsWith('**') 
      ? <b key={index} style={{ color: '#2D3748' }}>{part.slice(2, -2)}</b> 
      : part
  );
};

// MetricTile redesigned: Left-aligned list style, NO order numbers
const MetricTileListVersion = ({ label, value, icon }: { label: string, value: any, icon: string }) => (
  <div style={{
    padding: '16px', background: '#F8FAFC', borderRadius: '12px', 
    border: '1px solid #EDF2F7', display: 'flex', gap: '15px', 
    alignItems: 'center', marginBottom: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.02)'
  }}>
    <div style={{ flex: 1 }}>
      <strong style={{ display: 'block', color: '#2D3748', fontSize: '15px' }}>
        {renderFormattedText(value || (typeof value === 'number' ? value : "Not extracted"))}
      </strong>
      <p style={{ fontSize: '11px', color: '#718096', margin: '3px 0 0 0', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: '600' }}>
        {label}
      </p>
    </div>
    <div style={{ fontSize: '22px', flexShrink: 0, opacity: 0.8 }}>{icon}</div>
  </div>
);

// AnalysisBlock: Stretches fully to fill column width
const AnalysisBlock = ({ title, content, color }: { title: string, content: string, color: string }) => (
  <div style={{ 
    padding: '20px', background: '#fff', borderRadius: '12px', 
    borderLeft: `5px solid ${color}`, marginBottom: '18px', 
    boxShadow: '0 2px 5px rgba(0,0,0,0.03)', width: 'auto'
  }}>
    <h4 style={{ margin: '0 0 10px 0', color: '#1A202C', fontSize: '13px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{title}</h4>
    <p style={{ fontSize: '15px', margin: 0, color: '#4A5568', lineHeight: '1.6' }}>
      {renderFormattedText(content || "No specific insights generated.")}
    </p>
  </div>
);

function App() {
  const [url, setUrl] = useState('');
  const [data, setData] = useState<AuditData | null>(null);
  const [loading, setLoading] = useState(false);

  const runAudit = async (e?: React.FormEvent) => {
    if (e) e.preventDefault(); 
    if (!url) return;
    setLoading(true);
    try {
      const response = await fetch(`/api/audit?url=${url}`);      
      const data = await response.json();
      setData(data);
    } catch (error: any) {
      alert(`Audit failed: ${error.response?.data?.detail || "Check backend connection"}`);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '40px 20px', backgroundColor: '#F9FAFB', minHeight: '100vh', fontFamily: 'Inter, sans-serif' }}>
      {/* Container widened to reach page ends */}
      <div style={{ maxWidth: '1600px', margin: '0 auto' }}>
        <h1 style={{ textAlign: 'center', color: '#1A202C', marginBottom: '30px' }}>AI Website Auditor</h1>
        
        <form onSubmit={runAudit} style={{ display: 'flex', gap: '10px', marginBottom: '40px', background: '#fff', padding: '10px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
          <input 
            style={{ flex: 1, padding: '12px', borderRadius: '8px', border: 'none', outline: 'none', fontSize: '16px' }}
            placeholder="https://example.com" 
            value={url} onChange={(e) => setUrl(e.target.value)} 
          />
          <button type="submit" disabled={loading} style={{ padding: '12px 30px', background: '#0062FF', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' }}>
            {loading ? "Analyzing..." : "Run Audit"}
          </button>
        </form>

        {data && (
          /* Grid setup: 3 equal columns for side-by-side view */
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '30px', alignItems: 'start' }}>
            
            {/* COLUMN 1: 📊 FACTUAL METRICS */}
            <section>
              <h2 style={{ fontSize: '1.2rem', color: '#4A5568', marginBottom: '15px' }}>📊 Factual Metrics</h2>
              <div style={{ background: '#fff', padding: '20px', borderRadius: '12px', border: '1px solid #E2E8F0', marginBottom: '18px', boxShadow: '0 2px 5px rgba(0,0,0,0.03)' }}>
                <div style={{ fontSize: '10px', color: '#888', fontWeight: 'bold' }}>META DATA</div>
                <div style={{ fontSize: '13px', marginTop: '8px', color: '#2D3748', fontWeight: '600' }}>{data.factual_metrics.meta_title}</div>
                <div style={{ fontSize: '12px', marginTop: '4px', color: '#718096', lineHeight: 1.4 }}>{data.factual_metrics.meta_description}</div>
              </div>
              
              <MetricTileListVersion label="Word Count" value={data.factual_metrics.word_count} icon="📝" />
              <MetricTileListVersion label="CTA's (Call To Action) Found" value={data.factual_metrics.cta_count} icon="🎯" />
              <MetricTileListVersion label="Headings (H1/H2/H3)" value={`${data.factual_metrics.headings.h1}/${data.factual_metrics.headings.h2}/${data.factual_metrics.headings.h3}`} icon="🏗️" />
              <MetricTileListVersion label="% of Images with Missing Alt Text" value={`${data.factual_metrics.images_missing_alt_pct}%`} icon="⚠️" />
              <MetricTileListVersion label="Internal Links" value={data.factual_metrics.links_internal} icon="🔗" />
              <MetricTileListVersion label="External Links" value={data.factual_metrics.links_external} icon="🌎" />
            </section>

            {/* COLUMN 2: 🤖 AI STRATEGIC ANALYSIS */}
            <section style={{ background: '#fff', padding: '30px', borderRadius: '16px', border: '1px solid #E2E8F0' }}>
              <h2 style={{ marginTop: 0, color: '#0062FF', fontSize: '1.5rem', marginBottom: '20px' }}>🤖 AI Strategic Analysis</h2>
              {(() => {
                try {
                  const insights = typeof data.ai_insights === 'string' ? JSON.parse(data.ai_insights) : data.ai_insights;
                  return (
                    <div>
                      <AnalysisBlock title="SEO Structure" content={insights.seo_structure} color="#0062FF" />
                      <AnalysisBlock title="Messaging Clarity" content={insights.messaging_clarity} color="#805AD5" />
                      <AnalysisBlock title="CTA Usage" content={insights.cta_usage} color="#38A169" />
                      <AnalysisBlock title="Content Depth" content={insights.content_depth} color="#DD6B20" />
                      <AnalysisBlock title="UX & Structural Concerns" content={insights.ux_structural_concerns} color="#E53E3E" />
                    </div>
                  );
                } catch (e) {
                  return <p style={{ color: '#E53E3E' }}>Analysis render error.</p>;
                }
              })()}
            </section>

            {/* COLUMN 3: 🚀 PRIORITY ACTION ITEMS */}
            <section style={{ background: '#fff', padding: '30px', borderRadius: '16px', border: '1px solid #E2E8F0' }}>
              <h2 style={{ marginTop: 0, color: '#2D3748', fontSize: '1.5rem', marginBottom: '20px' }}>🚀 Priority Actions</h2>
              {(() => {
                try {
                  const insights = typeof data.ai_insights === 'string' ? JSON.parse(data.ai_insights) : data.ai_insights;
                  return (
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                      {Array.isArray(insights.recommendations) && insights.recommendations.map((item: any, i: number) => (
                        <li key={i} style={{ padding: '16px', background: '#F8FAFC', marginBottom: '12px', borderRadius: '12px', border: '1px solid #EDF2F7', display: 'flex', gap: '15px' }}>
                          <span style={{ height: '28px', width: '28px', background: '#EBF4FF', color: '#0062FF', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', flexShrink: 0, fontSize: '12px' }}>{i + 1}</span>
                          <div>
                            <strong style={{ display: 'block', color: '#2D3748', fontSize: '14px', marginBottom: '4px' }}>
                              {renderFormattedText(item.insight || item.action || (typeof item === 'string' ? item : "Recommendation"))}
                            </strong>
                            {item.reasoning && (
                              <p style={{ fontSize: '12px', color: '#718096', margin: 0, lineHeight: '1.4' }}>
                                {renderFormattedText(item.reasoning)}
                              </p>
                            )}
                          </div>
                        </li>
                      ))}
                    </ul>
                  );
                } catch (e) {
                  return <p style={{ color: '#E53E3E' }}>Recommendations render error.</p>;
                }
              })()}
            </section>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;