import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { Brain, Briefcase, CheckCircle2, Search } from "lucide-react";
import "./styles.css";

type Candidate = {
  name: string;
  email: string;
  skills: string[];
  experience_years: number;
  resume_text: string;
};

type JobRole = {
  title: string;
  required_skills: string[];
  description: string;
};

const candidate: Candidate = {
  name: "Aarav Mehta",
  email: "aarav@example.com",
  skills: ["Python", "FastAPI", "React", "SQL", "Docker"],
  experience_years: 1.2,
  resume_text: "Built placement dashboards using React, FastAPI, SQL, Docker, and AWS basics."
};

const role: JobRole = {
  title: "Full Stack AI Intern",
  required_skills: ["Python", "React", "FastAPI", "SQL", "Docker"],
  description: "Build AI-enabled placement workflows and recruiter dashboards."
};

function localScore() {
  const skills = new Set(candidate.skills.map((skill) => skill.toLowerCase()));
  const matched = role.required_skills.filter((skill) => skills.has(skill.toLowerCase()));
  return Math.round((matched.length / role.required_skills.length) * 100);
}

function App() {
  const [score] = useState(localScore());
  const matchedSkills = useMemo(
    () => role.required_skills.filter((skill) => candidate.skills.includes(skill)),
    []
  );

  return (
    <main>
      <aside>
        <div className="brand">
          <Brain size={28} />
          <span>TalentAI</span>
        </div>
        <nav>
          <button><Search size={18} /> Screening</button>
          <button><Briefcase size={18} /> Roles</button>
          <button><CheckCircle2 size={18} /> Shortlist</button>
        </nav>
      </aside>

      <section className="workspace">
        <header>
          <div>
            <h1>Campus Placement Matching</h1>
            <p>AI-assisted candidate-role fit scoring for placement teams.</p>
          </div>
          <div className="score">{score}%</div>
        </header>

        <div className="grid">
          <article>
            <h2>Candidate</h2>
            <h3>{candidate.name}</h3>
            <p>{candidate.email}</p>
            <div className="chips">
              {candidate.skills.map((skill) => <span key={skill}>{skill}</span>)}
            </div>
          </article>

          <article>
            <h2>Role</h2>
            <h3>{role.title}</h3>
            <p>{role.description}</p>
            <div className="chips required">
              {role.required_skills.map((skill) => <span key={skill}>{skill}</span>)}
            </div>
          </article>

          <article className="wide">
            <h2>AI Recommendation</h2>
            <h3>{score >= 75 ? "Shortlist" : "Review manually"}</h3>
            <p>
              Candidate matches {matchedSkills.length} of {role.required_skills.length} required skills:
              {" "}{matchedSkills.join(", ")}.
            </p>
          </article>
        </div>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
