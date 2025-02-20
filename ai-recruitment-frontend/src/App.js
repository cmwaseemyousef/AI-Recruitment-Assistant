import React, { useState } from "react";
import axios from "axios";

function App() {
  const [resumeText, setResumeText] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeResume = async () => {
    if (!resumeText.trim()) {
      alert("Please enter resume text.");
      return;
    }
    
    setLoading(true);
    setAnalysis(null);

    try {
      const response = await axios.post("http://127.0.0.1:5000/analyze-resume", {
        resume: resumeText,
      });
      setAnalysis(response.data);
    } catch (error) {
      console.error("Error analyzing resume:", error);
      alert("Failed to analyze resume.");
    }

    setLoading(false);
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>AI Resume Analyzer</h1>
      <textarea
        rows="6"
        cols="50"
        placeholder="Paste your resume here..."
        value={resumeText}
        onChange={(e) => setResumeText(e.target.value)}
      />
      <br />
      <button onClick={analyzeResume} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>

      {analysis && (
        <div>
          <h2>Analysis Result</h2>
          <p>{analysis.resume_analysis}</p>
        </div>
      )}
    </div>
  );
}

export default App;
