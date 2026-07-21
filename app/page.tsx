"use client";

import { useEffect, useMemo, useState } from "react";

type View = "overview" | "household" | "week" | "memories" | "privacy";
type Role = "Parent" | "Child" | "Senior";
type Member = { id: number; name: string; role: Role; initial: string };
type WeekItem = {
  id: number;
  title: string;
  day: string;
  time: string;
  kind: "Event" | "Task";
};
type Memory = { title: string; story: string; photo: string };

const requestExample =
  "Prepare the week: dentist appointment Tuesday at 4 PM, homework Wednesday, groceries Friday and a family meal on Sunday.";

const demoMembers: Member[] = [
  { id: 1, name: "Alex", role: "Parent", initial: "A" },
  { id: 2, name: "Lina", role: "Child", initial: "L" },
  { id: 3, name: "Sam", role: "Senior", initial: "S" },
];

const demoProposal: WeekItem[] = [
  { id: 1, title: "Dentist appointment", day: "Tuesday", time: "4:00 PM", kind: "Event" },
  { id: 2, title: "Homework", day: "Wednesday", time: "After school", kind: "Task" },
  { id: 3, title: "Groceries", day: "Friday", time: "6:00 PM", kind: "Task" },
  { id: 4, title: "Family meal", day: "Sunday", time: "12:30 PM", kind: "Event" },
];

const navigation: { id: View; label: string; mark: string }[] = [
  { id: "overview", label: "Overview", mark: "⌂" },
  { id: "household", label: "Household", mark: "◉" },
  { id: "week", label: "Shared week", mark: "□" },
  { id: "memories", label: "Memories", mark: "◇" },
  { id: "privacy", label: "Control & privacy", mark: "◎" },
];

export default function Home() {
  const [view, setView] = useState<View>("overview");
  const [members, setMembers] = useState<Member[]>([]);
  const [name, setName] = useState("");
  const [role, setRole] = useState<Role>("Parent");
  const [request, setRequest] = useState(requestExample);
  const [proposal, setProposal] = useState<WeekItem[]>([]);
  const [confirmed, setConfirmed] = useState<WeekItem[]>([]);
  const [thinking, setThinking] = useState(false);
  const [photo, setPhoto] = useState("Garden Sunday");
  const [memoryNote, setMemoryNote] = useState("Grandpa taught Lina how to plant rosemary.");
  const [memoryDraft, setMemoryDraft] = useState("");
  const [savedMemory, setSavedMemory] = useState<Memory | null>(null);
  const [toast, setToast] = useState("");

  useEffect(() => {
    let timer: number | undefined;
    try {
      const saved = localStorage.getItem("intellifamilia-demo");
      if (!saved) return;
      const data = JSON.parse(saved);
      timer = window.setTimeout(() => {
        setMembers(data.members ?? []);
        setConfirmed(data.confirmed ?? []);
        setSavedMemory(data.savedMemory ?? null);
      }, 0);
    } catch {
      // A damaged local demo state should never block the experience.
    }
    return () => {
      if (timer !== undefined) window.clearTimeout(timer);
    };
  }, []);

  useEffect(() => {
    localStorage.setItem(
      "intellifamilia-demo",
      JSON.stringify({ members, confirmed, savedMemory }),
    );
  }, [members, confirmed, savedMemory]);

  useEffect(() => {
    if (!toast) return;
    const timer = window.setTimeout(() => setToast(""), 2600);
    return () => window.clearTimeout(timer);
  }, [toast]);

  const progress = useMemo(
    () => [members.length > 0, confirmed.length > 0, Boolean(savedMemory)].filter(Boolean).length,
    [members, confirmed, savedMemory],
  );

  function loadDemo() {
    setMembers(demoMembers);
    setRequest(requestExample);
    setView("household");
    setToast("Synthetic household loaded. No personal data is used.");
  }

  function resetDemo() {
    setMembers([]);
    setConfirmed([]);
    setProposal([]);
    setSavedMemory(null);
    setMemoryDraft("");
    setView("overview");
    localStorage.removeItem("intellifamilia-demo");
    setToast("Demo reset.");
  }

  function addMember(event: React.FormEvent) {
    event.preventDefault();
    const clean = name.trim();
    if (!clean) return;
    setMembers((current) => [
      ...current,
      { id: Date.now(), name: clean, role, initial: clean.slice(0, 1).toUpperCase() },
    ]);
    setName("");
    setToast(`${clean} added as ${role}.`);
  }

  function generateProposal() {
    if (!request.trim()) return;
    setThinking(true);
    setProposal([]);
    window.setTimeout(() => {
      setProposal(demoProposal.map((item) => ({ ...item })));
      setThinking(false);
      setToast("Proposal ready for human review.");
    }, 700);
  }

  function updateProposal(id: number, field: keyof WeekItem, value: string) {
    setProposal((current) =>
      current.map((item) => (item.id === id ? { ...item, [field]: value } : item)),
    );
  }

  function rejectItem(id: number) {
    setProposal((current) => current.filter((item) => item.id !== id));
    setToast("Item rejected. Nothing was saved.");
  }

  function confirmProposal() {
    if (!proposal.length) return;
    setConfirmed(proposal.map((item) => ({ ...item })));
    setProposal([]);
    setToast("Week confirmed and saved on this device.");
  }

  function generateMemory() {
    const detail = memoryNote.trim() || "A quiet family moment worth remembering.";
    setMemoryDraft(
      `${photo}\n\n${detail} What began as a simple moment became a small lesson passed from one generation to the next — the kind of memory a family chooses to keep in its own words.`,
    );
    setToast("Draft created. Edit it before approval.");
  }

  function approveMemory() {
    if (!memoryDraft.trim()) return;
    setSavedMemory({ title: photo, story: memoryDraft, photo });
    setMemoryDraft("");
    setToast("Memory approved and added to the family timeline.");
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <button className="brand" onClick={() => setView("overview")} aria-label="Open overview">
          <span className="brand-mark">IF</span>
          <span>
            <strong>IntelliFamilia</strong>
            <small>Family-owned intelligence</small>
          </span>
        </button>

        <nav aria-label="Main navigation">
          {navigation.map((item) => (
            <button
              key={item.id}
              className={view === item.id ? "nav-item active" : "nav-item"}
              onClick={() => setView(item.id)}
            >
              <span aria-hidden="true">{item.mark}</span>
              {item.label}
            </button>
          ))}
        </nav>

        <div className="trust-card">
          <span className="status-dot" />
          <p>Human confirmation active</p>
          <small>Proposals remain editable until you decide.</small>
        </div>

        <button className="reset-link" onClick={resetDemo}>Reset synthetic demo</button>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">OpenAI Build Week · Demonstration</p>
            <h1>{navigation.find((item) => item.id === view)?.label}</h1>
          </div>
          <div className="top-actions">
            <span className="privacy-pill">Synthetic data only</span>
            <button className="avatar" aria-label="Demo profile">FL</button>
          </div>
        </header>

        {view === "overview" && (
          <div className="page overview-page">
            <section className="hero-panel">
              <div className="hero-copy">
                <p className="eyebrow gold">A calmer way to coordinate</p>
                <h2>The assistant proposes.<br />Your family decides.</h2>
                <p>
                  Organize one shared week and preserve meaningful memories without turning family life
                  into invisible automation.
                </p>
                <div className="hero-actions">
                  <button className="primary" onClick={loadDemo}>Start the safe demo</button>
                  <button className="secondary" onClick={() => setView("privacy")}>See the control model</button>
                </div>
              </div>
              <div className="principle-orbit" aria-label="Consent-first interaction model">
                <span className="orbit-label top">Propose</span>
                <span className="orbit-label right">Review</span>
                <span className="orbit-label bottom">Confirm</span>
                <div className="orbit-core"><strong>Human</strong><small>in control</small></div>
              </div>
            </section>

            <section className="journey-grid" aria-label="Demo progress">
              <article className={members.length ? "journey-card complete" : "journey-card"}>
                <span>01</span><div><h3>Create the household</h3><p>Clear roles across generations.</p></div>
                <button onClick={() => setView("household")}>{members.length ? "Review" : "Begin"}</button>
              </article>
              <article className={confirmed.length ? "journey-card complete" : "journey-card"}>
                <span>02</span><div><h3>Prepare the week</h3><p>Visible proposals before action.</p></div>
                <button onClick={() => setView("week")}>{confirmed.length ? "Review" : "Begin"}</button>
              </article>
              <article className={savedMemory ? "journey-card complete" : "journey-card"}>
                <span>03</span><div><h3>Preserve a memory</h3><p>A draft the family can rewrite.</p></div>
                <button onClick={() => setView("memories")}>{savedMemory ? "Review" : "Begin"}</button>
              </article>
            </section>

            <section className="overview-footer">
              <div><strong>{progress}/3</strong><span>demonstrated journeys complete</span></div>
              <div className="progress-track"><span style={{ width: `${(progress / 3) * 100}%` }} /></div>
              <p>Saved locally for a privacy-safe, repeatable demonstration.</p>
            </section>
          </div>
        )}

        {view === "household" && (
          <div className="page two-column">
            <section className="panel">
              <div className="section-heading">
                <div><p className="eyebrow gold">Journey 01</p><h2>One household, understandable roles</h2></div>
                <span className="step-state">{members.length ? "Ready" : "Set up"}</span>
              </div>
              <p className="lead">Roles clarify access and responsibility. They do not rank a family’s importance.</p>

              <form className="member-form" onSubmit={addMember}>
                <label>
                  First name
                  <input value={name} onChange={(event) => setName(event.target.value)} placeholder="Use a synthetic name" />
                </label>
                <label>
                  Role
                  <select value={role} onChange={(event) => setRole(event.target.value as Role)}>
                    <option>Parent</option><option>Child</option><option>Senior</option>
                  </select>
                </label>
                <button className="primary compact" type="submit">Add member</button>
              </form>

              {!members.length ? (
                <div className="empty-state">
                  <span>◉</span><h3>No family data yet</h3>
                  <p>Add synthetic members manually, or load the safe three-person demo.</p>
                  <button className="secondary" onClick={loadDemo}>Load Alex, Lina and Sam</button>
                </div>
              ) : (
                <div className="member-list">
                  {members.map((member) => (
                    <article className="member-row" key={member.id}>
                      <span className={`member-avatar ${member.role.toLowerCase()}`}>{member.initial}</span>
                      <div><h3>{member.name}</h3><p>{member.role}</p></div>
                      <span className="access-label">{member.role === "Parent" ? "Manage & approve" : member.role === "Child" ? "View & suggest" : "View & contribute"}</span>
                      <button aria-label={`Remove ${member.name}`} onClick={() => setMembers((all) => all.filter((item) => item.id !== member.id))}>×</button>
                    </article>
                  ))}
                </div>
              )}
            </section>

            <aside className="side-panel">
              <p className="eyebrow">Role promise</p>
              <h3>Different access.<br />Equal dignity.</h3>
              <ul className="check-list">
                <li><span>✓</span> Parents approve shared actions</li>
                <li><span>✓</span> Children can see and suggest</li>
                <li><span>✓</span> Seniors get a calm, readable view</li>
                <li><span>✓</span> No hidden tracking or surveillance</li>
              </ul>
              <button className="primary full" onClick={() => setView("week")} disabled={!members.length}>Continue to the week</button>
            </aside>
          </div>
        )}

        {view === "week" && (
          <div className="page">
            <section className="panel week-panel">
              <div className="section-heading">
                <div><p className="eyebrow gold">Journey 02</p><h2>Turn one request into a reviewable week</h2></div>
                <span className="step-state">No silent actions</span>
              </div>
              <div className="composer">
                <label htmlFor="week-request">Describe the week naturally</label>
                <textarea id="week-request" value={request} onChange={(event) => setRequest(event.target.value)} />
                <div className="composer-footer">
                  <span>Everything remains a draft until confirmation.</span>
                  <button className="primary" onClick={generateProposal} disabled={thinking}>{thinking ? "Preparing proposal…" : "Create proposal"}</button>
                </div>
              </div>

              {thinking && <div className="thinking"><span /><span /><span /> Interpreting the request and preparing a visible draft…</div>}

              {proposal.length > 0 && (
                <div className="proposal-area">
                  <div className="proposal-heading"><div><span className="ai-badge">AI draft</span><h3>Review every item</h3></div><p>Edit or reject before confirming.</p></div>
                  <div className="proposal-list">
                    {proposal.map((item) => (
                      <article className="proposal-row" key={item.id}>
                        <span className={`kind-dot ${item.kind.toLowerCase()}`} />
                        <input aria-label="Item title" value={item.title} onChange={(event) => updateProposal(item.id, "title", event.target.value)} />
                        <input aria-label="Day" value={item.day} onChange={(event) => updateProposal(item.id, "day", event.target.value)} />
                        <input aria-label="Time" value={item.time} onChange={(event) => updateProposal(item.id, "time", event.target.value)} />
                        <button className="reject" onClick={() => rejectItem(item.id)}>Reject</button>
                      </article>
                    ))}
                  </div>
                  <div className="confirmation-bar"><p><strong>{proposal.length} items</strong><span>Nothing has been saved yet.</span></p><button className="primary" onClick={confirmProposal}>Confirm and save week</button></div>
                </div>
              )}

              {!proposal.length && confirmed.length > 0 && (
                <div className="confirmed-area">
                  <div className="success-banner"><span>✓</span><div><strong>Week confirmed by a person</strong><p>This state persists after refresh on this device.</p></div></div>
                  <div className="calendar-strip">
                    {confirmed.map((item) => <article key={item.id}><span>{item.day.slice(0, 3)}</span><strong>{item.title}</strong><small>{item.time}</small></article>)}
                  </div>
                  <button className="secondary" onClick={() => setView("memories")}>Continue to memories</button>
                </div>
              )}
            </section>
          </div>
        )}

        {view === "memories" && (
          <div className="page memory-layout">
            <section className="panel">
              <div className="section-heading">
                <div><p className="eyebrow gold">Journey 03</p><h2>Keep the memory human-owned</h2></div>
                <span className="step-state">Editable by design</span>
              </div>
              <p className="lead">Choose a synthetic scene, add a few words, then rewrite or discard the draft.</p>

              <div className="photo-options" role="group" aria-label="Synthetic image choices">
                {["Garden Sunday", "Family Kitchen", "Seaside Walk"].map((option, index) => (
                  <button key={option} className={photo === option ? `photo-option art-${index + 1} selected` : `photo-option art-${index + 1}`} onClick={() => setPhoto(option)}>
                    <span>{index === 0 ? "🌿" : index === 1 ? "🍋" : "☀"}</span><strong>{option}</strong><small>Synthetic scene</small>
                  </button>
                ))}
              </div>

              <label className="note-field">A few words
                <textarea value={memoryNote} onChange={(event) => setMemoryNote(event.target.value)} />
              </label>
              <button className="primary" onClick={generateMemory}>Prepare an editable draft</button>

              {memoryDraft && (
                <div className="draft-editor">
                  <div><span className="ai-badge">AI draft</span><p>Edit freely. Approval is required.</p></div>
                  <textarea value={memoryDraft} onChange={(event) => setMemoryDraft(event.target.value)} />
                  <div className="draft-actions"><button className="text-button" onClick={() => setMemoryDraft("")}>Discard draft</button><button className="primary" onClick={approveMemory}>Approve memory</button></div>
                </div>
              )}
            </section>

            <aside className="memory-preview">
              <p className="eyebrow">Family timeline</p>
              {savedMemory ? (
                <article className="memory-card">
                  <div className={`memory-image ${savedMemory.photo === "Garden Sunday" ? "art-1" : savedMemory.photo === "Family Kitchen" ? "art-2" : "art-3"}`}><span>{savedMemory.photo === "Garden Sunday" ? "🌿" : savedMemory.photo === "Family Kitchen" ? "🍋" : "☀"}</span></div>
                  <div><small>Approved memory</small><h3>{savedMemory.title}</h3><p>{savedMemory.story.replace(`${savedMemory.title}\n\n`, "")}</p></div>
                </article>
              ) : <div className="empty-memory"><span>◇</span><p>An approved memory will appear here — never a hidden draft.</p></div>}
            </aside>
          </div>
        )}

        {view === "privacy" && (
          <div className="page privacy-page">
            <section className="privacy-hero"><p className="eyebrow gold">The product contract</p><h2>Useful intelligence needs visible limits.</h2><p>IntelliFamilia is designed around legibility, consent and reversible choices. The demonstration stores only synthetic information on this device.</p></section>
            <section className="principle-grid">
              <article><span>01</span><h3>Visible proposals</h3><p>The assistant shows what it understood before any meaningful action.</p></article>
              <article><span>02</span><h3>Human confirmation</h3><p>A person can edit, reject or confirm. Silence is never approval.</p></article>
              <article><span>03</span><h3>Family-owned memory</h3><p>Drafts do not enter the family timeline without explicit approval.</p></article>
              <article><span>04</span><h3>Bounded purpose</h3><p>No medical, legal, emergency or surveillance claims are made.</p></article>
            </section>
            <section className="data-panel"><div><span className="shield">◎</span><div><h3>Safe demonstration mode</h3><p>No sign-in. No real family data. No location. No background automation.</p></div></div><button className="secondary" onClick={resetDemo}>Delete local demo data</button></section>
          </div>
        )}
      </section>

      {toast && <div className="toast" role="status"><span>✓</span>{toast}</div>}
    </main>
  );
}
