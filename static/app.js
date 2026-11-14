/**
 * Skillora AI - Client Application Logic
 * Coordinates UI views, API communications, SVG progress rings,
 * Canvas DNA Spider Chart, Interactive Skill Universe Galaxy Map,
 * Smart Adapt AI, Assessment Runner, and Skill-to-Project Bridge.
 */

const API_BASE = "/api";
const LEARNER_ID = "deeksha";

const state = {
  learnerId: LEARNER_ID,
  profile: null,
  skillsSummary: null,
  skills: [],
  selectedSkill: null,
  careerDna: null,
  careerExplorer: null,
  selectedCareer: "Full Stack Developer",
  learningStages: [],
  projects: [],
  activeProjectId: "project_calculator",
  milestones: [],
  selectedMentorAgent: "AI Mentor Agent",
  activeQuizId: null,
  quizAnswers: {}
};

// DOM Cache
const elements = {
  navItems: document.querySelectorAll(".nav-item"),
  views: document.querySelectorAll(".view-section"),
  pageTitleHeading: document.getElementById("pageTitleHeading"),
  userAvatarLetter: document.getElementById("userAvatarLetter"),
  userDisplayName: document.getElementById("userDisplayName"),
  userRoleBadge: document.getElementById("userRoleBadge"),
  welcomeLearnerName: document.getElementById("welcomeLearnerName"),
  heroCareerGoal: document.getElementById("heroCareerGoal"),
  btnHeroSwitchCareer: document.getElementById("btnHeroSwitchCareer"),
  btnSyncAgents: document.getElementById("btnSyncAgents"),

  // Quick Demo Buttons
  btnDemoLowScore: document.getElementById("btnDemoLowScore"),
  btnDemoHighScore: document.getElementById("btnDemoHighScore"),
  btnDemoRunProject: document.getElementById("btnDemoRunProject"),
  btnDemoSwitchGoal: document.getElementById("btnDemoSwitchGoal"),

  // Stats
  readinessRingCircle: document.getElementById("readinessRingCircle"),
  readinessPercentText: document.getElementById("readinessPercentText"),
  readinessScoreBig: document.getElementById("readinessScoreBig"),
  skillStrengthPercent: document.getElementById("skillStrengthPercent"),
  skillsMasteredCount: document.getElementById("skillsMasteredCount"),
  skillsMissingCount: document.getElementById("skillsMissingCount"),
  streakDaysCount: document.getElementById("streakDaysCount"),

  // Daily Mission
  dailyMissionText: document.getElementById("dailyMissionText"),
  btnToggleMission: document.getElementById("btnToggleMission"),
  missionBtnLabel: document.getElementById("missionBtnLabel"),
  dashboardAgentLogs: document.getElementById("dashboardAgentLogs"),

  // Career DNA
  dnaRadarCanvas: document.getElementById("dnaRadarCanvas"),
  dnaStrengthsList: document.getElementById("dnaStrengthsList"),
  dnaGrowthEdgesList: document.getElementById("dnaGrowthEdgesList"),
  dnaRecommendedPathsContainer: document.getElementById("dnaRecommendedPathsContainer"),

  // Skill Universe
  universeCanvas: document.getElementById("universeCanvas"),
  selectedSkillDrawer: document.getElementById("selectedSkillDrawer"),
  drawerSkillStateBadge: document.getElementById("drawerSkillStateBadge"),
  drawerSkillName: document.getElementById("drawerSkillName"),
  drawerSkillCategory: document.getElementById("drawerSkillCategory"),
  drawerSkillProf: document.getElementById("drawerSkillProf"),
  drawerSkillNotes: document.getElementById("drawerSkillNotes"),
  drawerPrereqsList: document.getElementById("drawerPrereqsList"),
  drawerResourcesList: document.getElementById("drawerResourcesList"),
  btnOpenAddSkillModal: document.getElementById("btnOpenAddSkillModal"),

  // Career Explorer
  careerExplorerCards: document.getElementById("careerExplorerCards"),
  explorerSelectedRoleTitle: document.getElementById("explorerSelectedRoleTitle"),
  explorerSelectedRoleDesc: document.getElementById("explorerSelectedRoleDesc"),
  btnSwitchToThisCareer: document.getElementById("btnSwitchToThisCareer"),
  careerGapTableBody: document.getElementById("careerGapTableBody"),

  // Learning Journey
  learningJourneyContainer: document.getElementById("learningJourneyContainer"),

  // AI Mentor Chat
  agentSelectorCards: document.querySelectorAll(".agent-selector-card"),
  chatMessagesContainer: document.getElementById("chatMessagesContainer"),
  mentorChatForm: document.getElementById("mentorChatForm"),
  chatInputMessage: document.getElementById("chatInputMessage"),
  promptPills: document.querySelectorAll(".prompt-pill"),

  // Skill-to-Project Bridge
  projectSelectorList: document.getElementById("projectSelectorList"),
  activeProjectTitle: document.getElementById("activeProjectTitle"),
  activeProjectSubtitle: document.getElementById("activeProjectSubtitle"),
  activeProjectSkillPill: document.getElementById("activeProjectSkillPill"),
  activeProjectObjectives: document.getElementById("activeProjectObjectives"),
  projectCodeEditor: document.getElementById("projectCodeEditor"),
  btnResetProjectCode: document.getElementById("btnResetProjectCode"),
  btnRunProjectCode: document.getElementById("btnRunProjectCode"),
  projectConsolePanel: document.getElementById("projectConsolePanel"),
  projectLivePreviewBody: document.getElementById("projectLivePreviewBody"),

  // Future Me
  fmCurrentReadiness: document.getElementById("fmCurrentReadiness"),

  // Progress
  progressMilestonesRatio: document.getElementById("progressMilestonesRatio"),
  milestonesContainer: document.getElementById("milestonesContainer"),

  // Modals
  quizModal: document.getElementById("quizModal"),
  quizModalTitle: document.getElementById("quizModalTitle"),
  quizModalTopic: document.getElementById("quizModalTopic"),
  quizAdaptBanner: document.getElementById("quizAdaptBanner"),
  adaptIcon: document.getElementById("adaptIcon"),
  adaptTitle: document.getElementById("adaptTitle"),
  adaptDesc: document.getElementById("adaptDesc"),
  quizQuestionsContainer: document.getElementById("quizQuestionsContainer"),
  quizForm: document.getElementById("quizForm"),
  btnCloseQuizModal: document.getElementById("btnCloseQuizModal"),
  btnCancelQuiz: document.getElementById("btnCancelQuiz"),

  agentHuddleModal: document.getElementById("agentHuddleModal"),
  btnCloseHuddleModal: document.getElementById("btnCloseHuddleModal"),
  btnDoneHuddle: document.getElementById("btnDoneHuddle"),
  huddleLogsContainer: document.getElementById("huddleLogsContainer"),

  addSkillModal: document.getElementById("addSkillModal"),
  btnCloseSkillModal: document.getElementById("btnCloseSkillModal"),
  btnCancelAddSkill: document.getElementById("btnCancelAddSkill"),
  addSkillForm: document.getElementById("addSkillForm"),
  inputSkillName: document.getElementById("inputSkillName"),
  inputSkillCategory: document.getElementById("inputSkillCategory"),
  inputSkillState: document.getElementById("inputSkillState"),
  inputSkillProf: document.getElementById("inputSkillProf"),
  lblSkillProf: document.getElementById("lblSkillProf"),

  toastContainer: document.getElementById("toastContainer")
};

// --- Initialization ---
document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  setupEventListeners();
  loadAllData();
});

// --- Navigation ---
function setupNavigation() {
  const titles = {
    dashboard: "Home Dashboard",
    dna: "Career DNA – Understand Your Potential",
    universe: "My Skill Universe – Interactive Galaxy Map",
    explorer: "Intelligent Career Matching & Explorer",
    journey: "Personalized 4-Stage Learning Journey",
    mentor: "AI Mentor – Your Personal Learning Companion",
    projects: "Skill-to-Project Bridge (Hands-on Mini Projects)",
    futureme: "Future Me – Career Growth Preview",
    progress: "Progress & Achievement Milestones"
  };

  elements.navItems.forEach(item => {
    item.addEventListener("click", () => {
      const view = item.getAttribute("data-view");
      switchView(view);
    });
  });

  elements.btnHeroSwitchCareer?.addEventListener("click", () => switchView("explorer"));
}

function switchView(viewName) {
  elements.navItems.forEach(item => {
    item.classList.toggle("active", item.getAttribute("data-view") === viewName);
  });

  elements.views.forEach(section => {
    section.classList.toggle("active", section.id === `view-${viewName}`);
  });

  const titles = {
    dashboard: "Home Dashboard",
    dna: "Career DNA – Understand Your Potential",
    universe: "My Skill Universe – Interactive Galaxy Map",
    explorer: "Intelligent Career Matching & Explorer",
    journey: "Personalized 4-Stage Learning Journey",
    mentor: "AI Mentor – Your Personal Learning Companion",
    projects: "Skill-to-Project Bridge (Hands-on Mini Projects)",
    futureme: "Future Me – Career Growth Preview",
    progress: "Progress & Achievement Milestones"
  };

  if (elements.pageTitleHeading && titles[viewName]) {
    elements.pageTitleHeading.textContent = titles[viewName];
  }

  // View-specific re-renders
  if (viewName === "dna") {
    setTimeout(renderDnaRadar, 50);
  } else if (viewName === "universe") {
    setTimeout(renderSkillUniverse, 50);
  }
}

// --- Event Listeners Setup ---
function setupEventListeners() {
  // Sync Agents
  elements.btnSyncAgents?.addEventListener("click", triggerAgentHuddle);

  // Daily Mission Toggle
  elements.btnToggleMission?.addEventListener("click", toggleDailyGoal);

  // Quick Demo Buttons
  elements.btnDemoLowScore?.addEventListener("click", runDemoLowScoreScenario);
  elements.btnDemoHighScore?.addEventListener("click", runDemoHighScoreScenario);
  elements.btnDemoRunProject?.addEventListener("click", () => {
    switchView("projects");
    handleRunProjectCode();
  });
  elements.btnDemoSwitchGoal?.addEventListener("click", runDemoSwitchGoalScenario);

  // Mentor Agent Selection
  elements.agentSelectorCards.forEach(card => {
    card.addEventListener("click", () => {
      elements.agentSelectorCards.forEach(c => c.classList.remove("active"));
      card.classList.add("active");
      state.selectedMentorAgent = card.getAttribute("data-agent");
      showToast(`Switched consultation to ${state.selectedMentorAgent}`);
    });
  });

  // Mentor Chat Form
  elements.mentorChatForm?.addEventListener("submit", handleMentorSendMessage);

  // Quick Prompts
  elements.promptPills.forEach(pill => {
    pill.addEventListener("click", () => {
      elements.chatInputMessage.value = pill.getAttribute("data-prompt");
      handleMentorSendMessage(new Event("submit"));
    });
  });

  // Project Bridge
  elements.btnRunProjectCode?.addEventListener("click", handleRunProjectCode);
  elements.btnResetProjectCode?.addEventListener("click", resetActiveProjectCode);

  // Career Explorer Switch
  elements.btnSwitchToThisCareer?.addEventListener("click", handleSwitchCareer);

  // Quiz Modal Close
  elements.btnCloseQuizModal?.addEventListener("click", () => elements.quizModal.classList.remove("active"));
  elements.btnCancelQuiz?.addEventListener("click", () => elements.quizModal.classList.remove("active"));
  elements.quizForm?.addEventListener("submit", handleSubmitQuiz);

  // Huddle Modal Close
  elements.btnCloseHuddleModal?.addEventListener("click", () => elements.agentHuddleModal.classList.remove("active"));
  elements.btnDoneHuddle?.addEventListener("click", () => elements.agentHuddleModal.classList.remove("active"));

  // Add Skill Modal
  elements.btnOpenAddSkillModal?.addEventListener("click", () => elements.addSkillModal.classList.add("active"));
  elements.btnCloseSkillModal?.addEventListener("click", () => elements.addSkillModal.classList.remove("active"));
  elements.btnCancelAddSkill?.addEventListener("click", () => elements.addSkillModal.classList.remove("active"));
  elements.inputSkillProf?.addEventListener("input", e => elements.lblSkillProf.textContent = `${e.target.value}%`);
  elements.addSkillForm?.addEventListener("submit", handleAddSkill);

  // Universe Canvas Interactive Click
  elements.universeCanvas?.addEventListener("click", handleUniverseCanvasClick);
}

// --- Load All Data ---
async function loadAllData() {
  await Promise.all([
    fetchProfile(),
    fetchCareerDna(),
    fetchSkillUniverse(),
    fetchCareerExplorer(),
    fetchLearningJourney(),
    fetchProjects(),
    fetchFutureMe(),
    fetchProgress()
  ]);
}

// --- Profile & Dashboard ---
async function fetchProfile() {
  try {
    const res = await fetch(`${API_BASE}/profile?learner_id=${state.learnerId}`);
    const data = await res.json();
    if (data.profile) {
      state.profile = data.profile;
      state.skillsSummary = data.skills_summary;
      updateProfileUI();
    }
  } catch (err) {
    console.error("Failed to load profile:", err);
  }
}

function updateProfileUI() {
  const p = state.profile;
  if (!p) return;

  elements.userAvatarLetter.textContent = p.name.charAt(0);
  elements.userDisplayName.textContent = p.name;
  elements.userRoleBadge.textContent = `${p.career_goal} Aspirant`;
  elements.welcomeLearnerName.textContent = p.name;
  elements.heroCareerGoal.textContent = p.career_goal;

  // Readiness Score
  const score = p.readiness_score || 0;
  elements.readinessScoreBig.textContent = `${score}%`;
  elements.readinessPercentText.textContent = `${score}%`;

  // Circumference of radius 26 circle = 2 * PI * 26 ≈ 163.36
  const circumference = 163.36;
  const offset = circumference - (score / 100) * circumference;
  if (elements.readinessRingCircle) {
    elements.readinessRingCircle.style.strokeDashoffset = offset;
  }

  elements.skillStrengthPercent.textContent = `${p.skill_strength || 45}%`;
  elements.streakDaysCount.textContent = `${p.learning_streak || 6} Days 🔥`;

  if (state.skillsSummary) {
    elements.skillsMasteredCount.textContent = state.skillsSummary.mastered_count || 2;
    elements.skillsMissingCount.textContent = state.skillsSummary.missing_count || 5;
  }

  // Daily Mission
  elements.dailyMissionText.textContent = p.daily_goal || "Master CSS Flexbox layouts";
  if (p.daily_goal_completed) {
    elements.btnToggleMission.classList.add("completed");
    elements.missionBtnLabel.textContent = "Completed Today ✅";
  } else {
    elements.btnToggleMission.classList.remove("completed");
    elements.missionBtnLabel.textContent = "Mark as Completed";
  }

  if (elements.fmCurrentReadiness) {
    elements.fmCurrentReadiness.textContent = `${score}%`;
  }
}

async function toggleDailyGoal() {
  try {
    const res = await fetch(`${API_BASE}/profile/goal/toggle`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ learner_id: state.learnerId })
    });
    const data = await res.json();
    if (data.status === "success") {
      showToast(data.daily_goal_completed ? "Daily mission accomplished! +120 XP earned ✨" : "Mission marked incomplete.");
      await fetchProfile();
    }
  } catch (err) {
    console.error("Error toggling goal:", err);
  }
}

// --- 2. Career DNA ---
async function fetchCareerDna() {
  try {
    const res = await fetch(`${API_BASE}/career-dna?learner_id=${state.learnerId}`);
    const data = await res.json();
    if (data.career_dna) {
      state.careerDna = data.career_dna;
      renderCareerDnaUI();
      renderDnaRadar();
    }
  } catch (err) {
    console.error("Failed to load Career DNA:", err);
  }
}

function renderCareerDnaUI() {
  const dna = state.careerDna;
  if (!dna) return;

  elements.dnaStrengthsList.innerHTML = dna.natural_strengths.map(s => `
    <div class="dna-trait-pill">
      <span style="color: var(--accent-emerald);">✦</span>
      <span>${escapeHtml(s)}</span>
    </div>
  `).join("");

  elements.dnaGrowthEdgesList.innerHTML = dna.growth_edges.map(g => `
    <div class="dna-trait-pill" style="border-left-color: var(--accent-rose);">
      <span style="color: var(--accent-rose);">●</span>
      <span>${escapeHtml(g)}</span>
    </div>
  `).join("");

  elements.dnaRecommendedPathsContainer.innerHTML = dna.recommended_paths.map(path => `
    <div class="dna-path-card">
      <div>
        <h4 style="font-size: 1.05rem; font-weight: 700; color: #fff;">${escapeHtml(path.role)}</h4>
        <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 4px;">${escapeHtml(path.reason)}</p>
      </div>
      <div style="text-align: right;">
        <span style="font-size: 0.72rem; color: var(--text-dim); text-transform: uppercase;">Alignment Fit</span>
        <div class="dna-fit-score">${path.fit_score}%</div>
      </div>
    </div>
  `).join("");
}

function renderDnaRadar() {
  const canvas = elements.dnaRadarCanvas;
  if (!canvas || !state.careerDna) return;

  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;
  const centerX = width / 2;
  const centerY = height / 2;
  const radius = Math.min(centerX, centerY) - 40;

  ctx.clearRect(0, 0, width, height);

  const traits = [
    { name: "Analytical", val: state.careerDna.analytical_depth || 82 },
    { name: "Systems", val: state.careerDna.system_thinking || 78 },
    { name: "Creative", val: state.careerDna.creative_iteration || 68 },
    { name: "Velocity", val: state.careerDna.execution_velocity || 72 },
    { name: "Debugging", val: state.careerDna.debugging_resilience || 85 },
    { name: "Architecture", val: state.careerDna.architecture_vision || 64 }
  ];

  const totalAxes = traits.length;
  const angleStep = (Math.PI * 2) / totalAxes;

  // Background polygon rings
  const levels = 4;
  for (let l = 1; l <= levels; l++) {
    const r = (radius / levels) * l;
    ctx.beginPath();
    for (let i = 0; i < totalAxes; i++) {
      const angle = i * angleStep - Math.PI / 2;
      const x = centerX + r * Math.cos(angle);
      const y = centerY + r * Math.sin(angle);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.strokeStyle = "rgba(192, 132, 252, 0.15)";
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  // Draw axes & labels
  traits.forEach((t, i) => {
    const angle = i * angleStep - Math.PI / 2;
    const x = centerX + radius * Math.cos(angle);
    const y = centerY + radius * Math.sin(angle);

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(x, y);
    ctx.strokeStyle = "rgba(192, 132, 252, 0.25)";
    ctx.stroke();

    // Axis Label
    const labelX = centerX + (radius + 20) * Math.cos(angle);
    const labelY = centerY + (radius + 20) * Math.sin(angle);
    ctx.font = "11px -apple-system, sans-serif";
    ctx.fillStyle = "#94a3b8";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(`${t.name} (${t.val})`, labelX, labelY);
  });

  // Draw DNA Polygon
  ctx.beginPath();
  traits.forEach((t, i) => {
    const angle = i * angleStep - Math.PI / 2;
    const r = radius * (t.val / 100);
    const x = centerX + r * Math.cos(angle);
    const y = centerY + r * Math.sin(angle);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.closePath();
  ctx.fillStyle = "rgba(192, 132, 252, 0.28)";
  ctx.fill();
  ctx.strokeStyle = "#c084fc";
  ctx.lineWidth = 2.5;
  ctx.stroke();

  // Draw Nodes
  traits.forEach((t, i) => {
    const angle = i * angleStep - Math.PI / 2;
    const r = radius * (t.val / 100);
    const x = centerX + r * Math.cos(angle);
    const y = centerY + r * Math.sin(angle);

    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fillStyle = "#fff";
    ctx.fill();
    ctx.strokeStyle = "#8b5cf6";
    ctx.lineWidth = 2;
    ctx.stroke();
  });
}

// --- 3. My Skill Universe (Interactive Constellation Galaxy) ---
async function fetchSkillUniverse() {
  try {
    const res = await fetch(`${API_BASE}/skill-universe?learner_id=${state.learnerId}`);
    const data = await res.json();
    if (data.skills) {
      state.skills = data.skills;
      if (!state.selectedSkill && state.skills.length > 0) {
        state.selectedSkill = state.skills[0];
      }
      renderSkillUniverse();
      renderSelectedSkillDrawer();
    }
  } catch (err) {
    console.error("Failed to load skill universe:", err);
  }
}

function renderSkillUniverse() {
  const canvas = elements.universeCanvas;
  if (!canvas || !state.skills.length) return;

  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;

  ctx.clearRect(0, 0, width, height);

  // Background star field
  for (let s = 0; s < 45; s++) {
    const sx = (Math.sin(s * 99) * 0.5 + 0.5) * width;
    const sy = (Math.cos(s * 77) * 0.5 + 0.5) * height;
    ctx.beginPath();
    ctx.arc(sx, sy, (s % 3 === 0 ? 1.5 : 1), 0, Math.PI * 2);
    ctx.fillStyle = "rgba(255, 255, 255, 0.35)";
    ctx.fill();
  }

  // Draw connecting constellation lines
  const skillsMap = {};
  state.skills.forEach(sk => skillsMap[sk.name.toLowerCase()] = sk);

  ctx.strokeStyle = "rgba(192, 132, 252, 0.22)";
  ctx.lineWidth = 1.2;

  state.skills.forEach(skill => {
    const x1 = (skill.universe_x / 100) * width;
    const y1 = (skill.universe_y / 100) * height;

    skill.connections.forEach(connName => {
      const target = skillsMap[connName.toLowerCase()];
      if (target) {
        const x2 = (target.universe_x / 100) * width;
        const y2 = (target.universe_y / 100) * height;

        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();
      }
    });
  });

  // Draw skill celestial nodes
  state.skills.forEach(skill => {
    const x = (skill.universe_x / 100) * width;
    const y = (skill.universe_y / 100) * height;
    const isSelected = state.selectedSkill && state.selectedSkill.id === skill.id;

    let nodeColor = "#c084fc";
    let glowColor = "rgba(192, 132, 252, 0.4)";

    if (skill.state === "mastered") {
      nodeColor = "#10b981";
      glowColor = "rgba(16, 185, 129, 0.4)";
    } else if (skill.state === "learning") {
      nodeColor = "#f59e0b";
      glowColor = "rgba(245, 158, 11, 0.4)";
    } else if (skill.state === "recommended") {
      nodeColor = "#38bdf8";
      glowColor = "rgba(56, 189, 248, 0.4)";
    }

    // Outer aura glow
    ctx.beginPath();
    ctx.arc(x, y, isSelected ? 22 : 14, 0, Math.PI * 2);
    ctx.fillStyle = glowColor;
    ctx.fill();

    // Core circle
    ctx.beginPath();
    ctx.arc(x, y, isSelected ? 12 : 8, 0, Math.PI * 2);
    ctx.fillStyle = nodeColor;
    ctx.fill();
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = isSelected ? 2.5 : 1.5;
    ctx.stroke();

    // Node label
    ctx.font = isSelected ? "bold 12px -apple-system, sans-serif" : "10px -apple-system, sans-serif";
    ctx.fillStyle = isSelected ? "#fff" : "#cbd5e1";
    ctx.textAlign = "center";
    ctx.fillText(skill.name, x, y + (isSelected ? 26 : 20));
  });
}

function handleUniverseCanvasClick(e) {
  const canvas = elements.universeCanvas;
  if (!canvas || !state.skills.length) return;

  const rect = canvas.getBoundingClientRect();
  const clickX = e.clientX - rect.left;
  const clickY = e.clientY - rect.top;

  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;

  const realX = clickX * scaleX;
  const realY = clickY * scaleY;

  // Find nearest skill
  let closest = null;
  let minDist = 35;

  state.skills.forEach(skill => {
    const sx = (skill.universe_x / 100) * canvas.width;
    const sy = (skill.universe_y / 100) * canvas.height;
    const dist = Math.hypot(realX - sx, realY - sy);
    if (dist < minDist) {
      closest = skill;
      minDist = dist;
    }
  });

  if (closest) {
    state.selectedSkill = closest;
    renderSkillUniverse();
    renderSelectedSkillDrawer();
  }
}

function renderSelectedSkillDrawer() {
  const sk = state.selectedSkill;
  if (!sk) return;

  elements.drawerSkillName.textContent = sk.name;
  elements.drawerSkillCategory.textContent = `Category: ${sk.category} • Importance: ${sk.importance}`;
  elements.drawerSkillProf.textContent = `${sk.proficiency}%`;
  elements.drawerSkillNotes.textContent = sk.notes || "Audited and verified by Skillora AI.";

  const stateClassMap = {
    mastered: "active",
    learning: "remedial",
    missing: "pending",
    recommended: "fast-tracked"
  };
  elements.drawerSkillStateBadge.className = `stage-badge ${stateClassMap[sk.state] || 'active'}`;
  elements.drawerSkillStateBadge.textContent = sk.state.toUpperCase();

  // Prerequisites
  elements.drawerPrereqsList.innerHTML = sk.prerequisites.length
    ? sk.prerequisites.map(p => `<span class="prompt-pill">${escapeHtml(p)}</span>`).join("")
    : `<span style="font-size: 0.8rem; color: var(--text-dim);">No hard prerequisites.</span>`;

  // Resources
  elements.drawerResourcesList.innerHTML = sk.resources.length
    ? sk.resources.map(r => `
        <a href="${r.url}" target="_blank" style="font-size: 0.82rem; color: var(--accent-cyan); text-decoration: none;">
          🔗 ${escapeHtml(r.title)}
        </a>
      `).join("")
    : `<span style="font-size: 0.8rem; color: var(--text-dim);">Resources in curation.</span>`;
}

// --- 4. Career Explorer & Matching ---
async function fetchCareerExplorer() {
  try {
    const res = await fetch(`${API_BASE}/career-explorer?learner_id=${state.learnerId}`);
    const data = await res.json();
    if (data.analysis) {
      state.careerExplorer = data;
      state.selectedCareer = data.current_career;
      renderCareerExplorerUI();
    }
  } catch (err) {
    console.error("Failed to load career explorer:", err);
  }
}

function renderCareerExplorerUI() {
  const exp = state.careerExplorer;
  if (!exp) return;

  // Render Career Cards
  elements.careerExplorerCards.innerHTML = exp.all_careers.map(carName => {
    const isActive = carName === state.selectedCareer;
    return `
      <div class="career-choice-card ${isActive ? 'active' : ''}" onclick="selectExplorerCareer('${escapeHtml(carName)}')">
        <h4 style="font-size: 0.95rem; font-weight: 700; color: #fff;">${escapeHtml(carName)}</h4>
        <span style="font-size: 0.72rem; color: var(--accent-cyan);">${isActive ? 'Active Goal' : 'Explore Match'}</span>
      </div>
    `;
  }).join("");

  elements.explorerSelectedRoleTitle.textContent = `${state.selectedCareer} Benchmark Analysis`;
  elements.explorerSelectedRoleDesc.textContent = exp.career_details.description || "Comprehensive competency comparison against 2026 hiring expectations.";

  // Render Table
  const comp = exp.career_details.core_competencies || [];
  const skillsMap = {};
  state.skills.forEach(s => skillsMap[s.name.toLowerCase()] = s);

  elements.careerGapTableBody.innerHTML = comp.map(item => {
    const reqLower = item.name.toLowerCase();
    let matchedSkill = null;
    for (let k in skillsMap) {
      if (reqLower.includes(k) || k.includes(reqLower) || reqLower.split(" ").some(w => w.length > 3 && k.includes(w))) {
        matchedSkill = skillsMap[k];
        break;
      }
    }

    const currentProf = matchedSkill ? matchedSkill.proficiency : 0;
    const isMastered = matchedSkill && matchedSkill.state === "mastered";
    const isLearning = matchedSkill && matchedSkill.state === "learning";

    let stateLabel = "Missing Gap";
    let stateColor = "var(--accent-rose)";
    if (isMastered) {
      stateLabel = "Mastered";
      stateColor = "var(--accent-emerald)";
    } else if (isLearning) {
      stateLabel = "Learning";
      stateColor = "var(--accent-amber)";
    }

    return `
      <tr>
        <td style="font-weight: 600; color: #fff;">${escapeHtml(item.name)}</td>
        <td style="color: var(--text-muted);">${escapeHtml(item.category)}</td>
        <td><strong style="color: var(--accent-cyan);">${item.target}%</strong></td>
        <td>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span>${currentProf}%</span>
            <div class="skill-progress-bar-bg" style="width: 70px;">
              <div class="skill-progress-bar-fill" style="width: ${Math.min(currentProf, 100)}%;"></div>
            </div>
          </div>
        </td>
        <td><span class="priority-tag ${item.importance}">${item.importance}</span></td>
        <td><strong style="color: ${stateColor}; font-size: 0.8rem;">${stateLabel}</strong></td>
      </tr>
    `;
  }).join("");
}

window.selectExplorerCareer = function(carName) {
  state.selectedCareer = carName;
  renderCareerExplorerUI();
};

async function handleSwitchCareer() {
  try {
    const res = await fetch(`${API_BASE}/career-explorer/switch`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ learner_id: state.learnerId, career_goal: state.selectedCareer })
    });
    const data = await res.json();
    if (data.status === "success") {
      showToast(`Dream career changed to ${state.selectedCareer}! 5 Agents recalibrating...`);
      await loadAllData();
      switchView("dashboard");
    }
  } catch (err) {
    console.error("Error switching career:", err);
  }
}

// --- 5. Learning Journey (4 Stages: Discover, Develop, Create, Achieve) ---
async function fetchLearningJourney() {
  try {
    const res = await fetch(`${API_BASE}/learning-journey?learner_id=${state.learnerId}`);
    const data = await res.json();
    if (data.stages) {
      state.learningStages = data.stages;
      renderLearningJourney();
    }
  } catch (err) {
    console.error("Failed to load learning journey:", err);
  }
}

function renderLearningJourney() {
  if (!elements.learningJourneyContainer) return;

  elements.learningJourneyContainer.innerHTML = state.learningStages.map(stage => {
    const isActive = stage.status === "active";

    const itemsHtml = stage.items.map(item => {
      const isCompleted = item.completed === 1;
      const isRemedial = item.is_adaptive_remedial === 1;
      const isFastTrack = item.is_adaptive_fasttrack === 1;

      let extraClass = isCompleted ? "completed" : "";
      if (isRemedial) extraClass += " remedial";
      if (isFastTrack) extraClass += " fast-tracked";

      let badgeTag = "";
      if (isRemedial) badgeTag = `<span style="font-size: 0.72rem; color: var(--accent-amber); font-weight:700;">🧠 Smart Adapt Drill</span>`;
      if (isFastTrack) badgeTag = `<span style="font-size: 0.72rem; color: var(--accent-cyan); font-weight:700;">⚡ Fast-Track Elective</span>`;

      let actionBtn = "";
      if (item.item_type === "quiz") {
        actionBtn = `<button class="btn-quiz-trigger" onclick="openAssessmentModal('${item.resource_url}')">Take Diagnostic 📝</button>`;
      } else if (item.item_type === "project") {
        actionBtn = `<button class="btn-quiz-trigger" onclick="openProjectBridge('${item.resource_url}')">Open Project 🛠️</button>`;
      }

      return `
        <div class="task-item ${extraClass}">
          <div class="task-left">
            <div class="task-checkbox ${isCompleted ? 'checked' : ''}" onclick="toggleRoadmapItem('${item.id}')">
              ${isCompleted ? '✓' : ''}
            </div>
            <div>
              <div style="display: flex; align-items: center; gap: 8px;">
                <span class="task-title">${escapeHtml(item.title)}</span>
                ${badgeTag}
              </div>
              <p class="task-desc">${escapeHtml(item.description)}</p>
            </div>
          </div>
          <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 0.76rem; color: var(--text-dim);">${item.estimated_time || '2 hrs'}</span>
            ${actionBtn}
          </div>
        </div>
      `;
    }).join("");

    return `
      <div class="stage-card ${isActive ? 'active' : ''}">
        <div class="stage-header">
          <div>
            <h3 class="card-title">${escapeHtml(stage.title)}</h3>
            <p class="card-subtitle">${escapeHtml(stage.tagline)} • ${escapeHtml(stage.description)}</p>
          </div>
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 0.78rem; color: var(--text-muted);">${stage.duration_hours} hrs</span>
            <span class="stage-badge ${stage.status}">${stage.status.toUpperCase()}</span>
          </div>
        </div>
        <div class="stage-tasks-list">
          ${itemsHtml}
        </div>
      </div>
    `;
  }).join("");
}

async function toggleRoadmapItem(itemId) {
  try {
    const res = await fetch(`${API_BASE}/learning-journey/toggle`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ learner_id: state.learnerId, item_id: itemId })
    });
    const data = await res.json();
    if (data.status === "success") {
      showToast(data.completed ? "Item completed! Career Readiness recalculated." : "Item marked incomplete.");
      await Promise.all([fetchLearningJourney(), fetchProfile(), fetchProgress()]);
    }
  } catch (err) {
    console.error("Error toggling item:", err);
  }
}

// --- 6. AI Mentor & Multi-Agent Mesh ---
async function handleMentorSendMessage(e) {
  if (e) e.preventDefault();
  const msg = elements.chatInputMessage.value.trim();
  if (!msg) return;

  appendChatMessage(msg, "user");
  elements.chatInputMessage.value = "";

  try {
    const res = await fetch(`${API_BASE}/mentor/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        learner_id: state.learnerId,
        message: msg,
        selected_agent: state.selectedMentorAgent
      })
    });
    const data = await res.json();
    appendChatMessage(data.message, "agent", data.responder);
  } catch (err) {
    appendChatMessage("Network synchronization error. Please try again.", "agent");
  }
}

function appendChatMessage(text, sender, agentName) {
  const container = elements.chatMessagesContainer;
  const msgDiv = document.createElement("div");
  msgDiv.className = `chat-msg ${sender}`;

  const avatar = sender === "user" ? "D" : (agentName ? agentName.charAt(0) : "M");
  const authorLabel = sender === "agent" && agentName
    ? `<div style="font-size: 0.72rem; color: var(--lavender); font-weight: 700; margin-bottom: 4px;">${escapeHtml(agentName)}</div>`
    : "";

  msgDiv.innerHTML = `
    <div class="chat-msg-avatar">${avatar}</div>
    <div class="chat-bubble">
      ${authorLabel}
      ${escapeHtml(text)}
    </div>
  `;

  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;
}

// --- 7. Skill-to-Project Bridge ---
async function fetchProjects() {
  try {
    const res = await fetch(`${API_BASE}/projects?learner_id=${state.learnerId}`);
    const data = await res.json();
    if (data.projects) {
      state.projects = data.projects;
      renderProjectSelectorList();
      loadActiveProject(state.activeProjectId);
    }
  } catch (err) {
    console.error("Failed to load projects:", err);
  }
}

function renderProjectSelectorList() {
  if (!elements.projectSelectorList) return;

  elements.projectSelectorList.innerHTML = state.projects.map(p => {
    const isActive = p.id === state.activeProjectId;
    const isCompleted = p.status === "completed";

    return `
      <div class="project-card ${isActive ? 'active' : ''}" onclick="selectProject('${p.id}')">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <span style="font-size: 0.72rem; text-transform: uppercase; color: var(--accent-cyan); font-weight: 700;">${escapeHtml(p.associated_skill)}</span>
          <span style="font-size: 0.68rem; color: ${isCompleted ? 'var(--accent-emerald)' : 'var(--text-dim)'}; font-weight: 700;">
            ${isCompleted ? 'VERIFIED ✅' : 'IN PROGRESS'}
          </span>
        </div>
        <h4 style="font-size: 0.92rem; font-weight: 700; color: #fff;">${escapeHtml(p.title)}</h4>
        <p style="font-size: 0.76rem; color: var(--text-muted); margin-top: 2px;">${escapeHtml(p.scenario.substring(0, 75))}...</p>
      </div>
    `;
  }).join("");
}

window.selectProject = function(projectId) {
  state.activeProjectId = projectId;
  renderProjectSelectorList();
  loadActiveProject(projectId);
};

window.openProjectBridge = function(projectId) {
  switchView("projects");
  selectProject(projectId);
};

function loadActiveProject(projectId) {
  const p = state.projects.find(proj => proj.id === projectId);
  if (!p) return;

  elements.activeProjectTitle.textContent = p.title;
  elements.activeProjectSubtitle.textContent = p.scenario;
  elements.activeProjectSkillPill.textContent = `Target Skill: ${p.associated_skill}`;
  elements.activeProjectObjectives.innerHTML = `<strong>Demonstrated Objectives:</strong><br>` + p.objectives.map(o => `<div>• ${escapeHtml(o)}</div>`).join("");
  elements.projectCodeEditor.value = p.starter_code;
  elements.projectConsolePanel.innerHTML = `<span style="color: var(--text-dim);">&gt; Console ready for ${p.title}. Click 'Evaluate Project & Test Code'.</span>`;

  renderLiveProjectPreview(projectId);
}

function resetActiveProjectCode() {
  const p = state.projects.find(proj => proj.id === state.activeProjectId);
  if (p) {
    elements.projectCodeEditor.value = p.starter_code;
    showToast("Starter template reloaded.");
  }
}

async function handleRunProjectCode() {
  const code = elements.projectCodeEditor.value;
  elements.projectConsolePanel.innerHTML = `<span style="color: var(--accent-cyan);">&gt; Running test suite and static analysis runner...</span>`;

  try {
    const res = await fetch(`${API_BASE}/projects/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        learner_id: state.learnerId,
        project_id: state.activeProjectId,
        code: code
      })
    });
    const result = await res.json();

    const badge = result.passed
      ? `<span style="color: var(--accent-emerald); font-weight: 700;">PASSED (${result.score}/100)</span>`
      : `<span style="color: var(--accent-rose); font-weight: 700;">NEEDS REVISION (${result.score}/100)</span>`;

    elements.projectConsolePanel.innerHTML = `
      <div style="margin-bottom: 6px;">&gt; Execution Result: ${badge}</div>
      <div style="color: #cbd5e1; margin-bottom: 6px;">&gt; Automated Feedback: ${escapeHtml(result.feedback)}</div>
      <div style="color: var(--accent-cyan); font-size: 0.78rem;">&gt; Validated Constraints: ${result.matched_requirements.join(", ") || 'None'}</div>
    `;

    if (result.passed) {
      showToast("Project verified! Skill upgraded in your Skill Universe 🎉");
    }

    await Promise.all([fetchProfile(), fetchSkillUniverse(), fetchProjects(), fetchProgress()]);
  } catch (err) {
    elements.projectConsolePanel.innerHTML = `<span style="color: var(--accent-rose);">&gt; Execution error: ${err.message}</span>`;
  }
}

// Live Interactive Artifact Preview for Projects
function renderLiveProjectPreview(projectId) {
  const container = elements.projectLivePreviewBody;
  if (!container) return;

  if (projectId === "project_calculator") {
    container.innerHTML = `
      <div style="max-width: 260px; background: rgba(9, 10, 26, 0.9); border: 1px solid var(--border-glow); border-radius: 12px; padding: 16px; margin: 0 auto;">
        <div style="background: rgba(18, 17, 44, 0.9); padding: 12px; border-radius: 8px; text-align: right; font-size: 1.4rem; font-family: var(--font-mono); color: #fff; margin-bottom: 12px;" id="demoCalcScreen">142.50</div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;">
          <button class="demo-chip-btn" onclick="demoCalcKey('C')">C</button>
          <button class="demo-chip-btn" onclick="demoCalcKey('/')">/</button>
          <button class="demo-chip-btn" onclick="demoCalcKey('*')">*</button>
          <button class="demo-chip-btn" onclick="demoCalcKey('-')">-</button>
          <button class="demo-chip-btn" onclick="demoCalcKey('7')">7</button>
          <button class="demo-chip-btn" onclick="demoCalcKey('8')">8</button>
          <button class="demo-chip-btn" onclick="demoCalcKey('9')">9</button>
          <button class="demo-chip-btn" onclick="demoCalcKey('+')">+</button>
          <button class="demo-chip-btn" onclick="demoCalcKey('4')">4</button>
          <button class="demo-chip-btn" onclick="demoCalcKey('5')">5</button>
          <button class="demo-chip-btn" onclick="demoCalcKey('6')">6</button>
          <button class="demo-chip-btn" onclick="demoCalcKey('=')" style="background: var(--primary); color: #fff;">=</button>
        </div>
      </div>
    `;
  } else if (projectId === "project_portfolio") {
    container.innerHTML = `
      <div style="background: rgba(9, 10, 26, 0.85); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
          <div>
            <h4 style="font-size: 1.05rem; font-weight: 700; color: #fff;">Deeksha</h4>
            <p style="font-size: 0.78rem; color: var(--lavender);">Full Stack Software Engineer</p>
          </div>
          <button class="prompt-pill" style="border-color: var(--accent-emerald); color: var(--accent-emerald);">● Available for Work</button>
        </div>
        <div style="display: flex; gap: 8px; margin-bottom: 12px;">
          <span class="prompt-pill" style="font-size: 0.72rem;">Python</span>
          <span class="prompt-pill" style="font-size: 0.72rem;">SQL</span>
          <span class="prompt-pill" style="font-size: 0.72rem;">React</span>
          <span class="prompt-pill" style="font-size: 0.72rem;">Node.js</span>
        </div>
        <p style="font-size: 0.8rem; color: #94a3b8;">Interactive portfolio component state rendered with React props.</p>
      </div>
    `;
  } else if (projectId === "project_backend_api") {
    container.innerHTML = `
      <div style="background: rgba(9, 10, 26, 0.85); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 14px; font-family: var(--font-mono); font-size: 0.8rem;">
        <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 8px;">
          <span style="background: rgba(16, 185, 129, 0.2); color: var(--accent-emerald); padding: 2px 8px; border-radius: 4px; font-weight: 700;">GET</span>
          <span style="color: #fff;">/api/skills</span>
          <span style="color: var(--accent-cyan); margin-left: auto;">200 OK • 18ms</span>
        </div>
        <pre style="color: #94a3b8; font-size: 0.75rem; overflow-x: auto;">
{
  "success": true,
  "count": 2,
  "data": [
    { "id": 1, "name": "Python", "category": "Backend", "proficiency": 70 },
    { "id": 2, "name": "SQL", "category": "Database", "proficiency": 65 }
  ]
}
        </pre>
      </div>
    `;
  } else {
    container.innerHTML = `
      <div style="background: rgba(9, 10, 26, 0.85); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 14px; font-size: 0.8rem;">
        <span style="color: var(--accent-emerald); font-weight: 700;">✓ Schema Verified (3NF Normalized)</span>
        <div style="margin-top: 8px; color: #cbd5e1;">Query Output: Course Completion Velocity</div>
        <div style="color: var(--accent-cyan); font-family: var(--font-mono); margin-top: 4px;">4 Courses Audited • 100% Referential Integrity</div>
      </div>
    `;
  }
}

window.demoCalcKey = function(key) {
  const scr = document.getElementById("demoCalcScreen");
  if (!scr) return;
  if (key === "C") scr.textContent = "0";
  else if (key === "=") scr.textContent = "42.00";
  else scr.textContent = (scr.textContent === "0" ? "" : scr.textContent) + key;
};

// --- 8. Future Me ---
async function fetchFutureMe() {
  try {
    const res = await fetch(`${API_BASE}/future-me?learner_id=${state.learnerId}`);
    const data = await res.json();
    if (data.future_me && elements.fmCurrentReadiness) {
      elements.fmCurrentReadiness.textContent = `${data.future_me.current_self.readiness_score}%`;
    }
  } catch (err) {
    console.error("Failed to load future me:", err);
  }
}

// --- 9. Progress & Achievements ---
async function fetchProgress() {
  try {
    const res = await fetch(`${API_BASE}/progress?learner_id=${state.learnerId}`);
    const data = await res.json();
    if (data.milestones) {
      state.milestones = data.milestones;
      renderMilestones();
    }
    if (data.recent_logs && elements.dashboardAgentLogs) {
      elements.dashboardAgentLogs.innerHTML = data.recent_logs.map(log => `
        <div class="log-item">
          <div class="log-meta">
            <span class="log-agent-name">${escapeHtml(log.agent_name)}</span>
            <span class="log-time">${new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
          </div>
          <div class="log-message">${escapeHtml(log.message)}</div>
        </div>
      `).join("");
    }
  } catch (err) {
    console.error("Failed to load progress:", err);
  }
}

function renderMilestones() {
  if (!elements.milestonesContainer) return;

  const achievedCount = state.milestones.filter(m => m.achieved === 1).length;
  elements.progressMilestonesRatio.textContent = `${achievedCount} / ${state.milestones.length}`;

  const iconMap = {
    sparkle: "✨",
    flame: "🔥",
    target: "🎯",
    code: "🛠️",
    trophy: "🏆"
  };

  elements.milestonesContainer.innerHTML = state.milestones.map(m => {
    const isAchieved = m.achieved === 1;
    return `
      <div class="milestone-card ${isAchieved ? 'achieved' : 'locked'}">
        <div class="milestone-icon">${iconMap[m.icon] || "⭐"}</div>
        <h4 style="font-size: 1.05rem; font-weight: 700; color: #fff;">${escapeHtml(m.title)}</h4>
        <p style="font-size: 0.8rem; color: var(--text-muted);">${escapeHtml(m.description)}</p>
        <span style="font-size: 0.72rem; font-weight: 700; color: ${isAchieved ? 'var(--accent-emerald)' : 'var(--text-dim)'}; text-transform: uppercase;">
          ${isAchieved ? 'Achieved ✅' : 'Locked 🔒'}
        </span>
      </div>
    `;
  }).join("");
}

// --- Adaptive Assessment & Smart Adapt AI ---
window.openAssessmentModal = async function(quizId) {
  state.activeQuizId = quizId || "quiz_discover";
  state.quizAnswers = {};
  elements.quizAdaptBanner.style.display = "none";

  try {
    const res = await fetch(`${API_BASE}/assessments/${state.activeQuizId}`);
    const data = await res.json();
    if (data.quiz) {
      const q = data.quiz;
      elements.quizModalTitle.textContent = q.title;
      elements.quizModalTopic.textContent = `${q.topic} • ${q.description}`;

      elements.quizQuestionsContainer.innerHTML = q.questions.map((question, index) => {
        const optionsHtml = question.options.map((opt, optIndex) => `
          <button type="button" class="quiz-option-btn" data-qid="${question.id}" data-opt="${optIndex}" onclick="selectQuizOption('${question.id}', ${optIndex}, this)">
            ${String.fromCharCode(65 + optIndex)}. ${escapeHtml(opt)}
          </button>
        `).join("");

        return `
          <div class="quiz-question-box" id="qbox_${question.id}">
            <h4 style="font-size: 0.94rem; font-weight: 600; color: #fff; margin-bottom: 12px;">
              ${index + 1}. ${escapeHtml(question.question)}
            </h4>
            <div>${optionsHtml}</div>
          </div>
        `;
      }).join("");

      elements.quizModal.classList.add("active");
    }
  } catch (err) {
    console.error("Failed to load quiz:", err);
  }
};

window.selectQuizOption = function(qid, optIndex, btn) {
  state.quizAnswers[qid] = optIndex;
  const parent = btn.parentElement;
  parent.querySelectorAll(".quiz-option-btn").forEach(b => b.classList.remove("selected"));
  btn.classList.add("selected");
};

async function handleSubmitQuiz(e) {
  e.preventDefault();
  if (!state.activeQuizId) return;

  try {
    const res = await fetch(`${API_BASE}/assessments/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        learner_id: state.learnerId,
        quiz_id: state.activeQuizId,
        answers: state.quizAnswers
      })
    });
    const result = await res.json();

    // Display Smart Adapt AI Banner
    elements.quizAdaptBanner.style.display = "flex";
    if (result.smart_adapt_action === "SMART_ADAPT_REMEDIAL") {
      elements.quizAdaptBanner.className = "adapt-banner";
      elements.adaptIcon.textContent = "🧠";
      elements.adaptTitle.textContent = "Smart Adapt AI Activated – Remedial Revision Drills Injected";
      elements.adaptDesc.textContent = `Score: ${result.percentage}%. Detected struggle areas: ${result.struggles.join(", ") || 'Fundamentals'}. Added foundation micro-drills to your journey.`;
      showToast("Smart Adapt AI injected remedial foundation drills!");
    } else if (result.smart_adapt_action === "SMART_ADAPT_FAST_TRACK") {
      elements.quizAdaptBanner.className = "adapt-banner fast-track";
      elements.adaptIcon.textContent = "⚡";
      elements.adaptTitle.textContent = "Fast-Track AI Unlocked – Top Tier Mastery!";
      elements.adaptDesc.textContent = `Outstanding score: ${result.percentage}%! Advanced elective topics unlocked and 'Diagnostic Vanguard' milestone awarded.`;
      showToast("Fast-Track bonus elective unlocked! ⚡");
    } else {
      elements.quizAdaptBanner.className = "adapt-banner fast-track";
      elements.adaptIcon.textContent = "✅";
      elements.adaptTitle.textContent = `Assessment Completed: ${result.percentage}% Score`;
      elements.adaptDesc.textContent = result.smart_adapt_message;
    }

    // Per-question feedback
    if (result.details) {
      result.details.forEach(detail => {
        const box = document.getElementById(`qbox_${detail.id}`);
        if (!box) return;

        const buttons = box.querySelectorAll(".quiz-option-btn");
        buttons.forEach(btn => {
          const opt = parseInt(btn.getAttribute("data-opt"), 10);
          btn.style.pointerEvents = "none";
          if (opt === detail.correct_choice) {
            btn.classList.add("correct");
          } else if (opt === detail.user_choice && !detail.is_correct) {
            btn.classList.add("wrong");
          }
        });

        // Add explanation
        const explDiv = document.createElement("div");
        explDiv.className = "quiz-explanation-box";
        explDiv.innerHTML = `<strong>Concept: ${escapeHtml(detail.concept)}</strong><br>${escapeHtml(detail.explanation)}`;
        box.appendChild(explDiv);
      });
    }

    elements.quizModal.querySelector(".modal-dialog").scrollTop = 0;
    await Promise.all([fetchProfile(), fetchLearningJourney(), fetchProgress()]);
  } catch (err) {
    console.error("Failed to submit assessment:", err);
  }
}

// --- Quick Demo Scenario Runners ---
async function runDemoLowScoreScenario() {
  showToast("Running Demo Scenario: Deliberate <50% score to test Smart Adapt AI...");
  await openAssessmentModal("quiz_discover");
  setTimeout(async () => {
    // Fill wrong choices
    state.quizAnswers = { qd_1: 0, qd_2: 0, qd_3: 0, qd_4: 0, qd_5: 1 };
    await handleSubmitQuiz(new Event("submit"));
  }, 400);
}

async function runDemoHighScoreScenario() {
  showToast("Running Demo Scenario: 100% score to test Fast-Track AI unlock...");
  await openAssessmentModal("quiz_discover");
  setTimeout(async () => {
    // Fill all correct choices
    state.quizAnswers = { qd_1: 1, qd_2: 1, qd_3: 2, qd_4: 1, qd_5: 0 };
    await handleSubmitQuiz(new Event("submit"));
  }, 400);
}

async function runDemoSwitchGoalScenario() {
  state.selectedCareer = "Data Scientist & AI Specialist";
  await handleSwitchCareer();
}

// --- 5-Agent Collaborative Huddle ---
async function triggerAgentHuddle() {
  elements.agentHuddleModal.classList.add("active");
  elements.huddleLogsContainer.innerHTML = `<div style="text-align: center; padding: 24px; color: var(--accent-cyan);">Synchronizing 5-Agent Collaborative Mesh...</div>`;

  try {
    const res = await fetch(`${API_BASE}/agents/collaborate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ learner_id: state.learnerId })
    });
    const data = await res.json();

    if (data.huddle_flow) {
      elements.huddleLogsContainer.innerHTML = data.huddle_flow.map(h => `
        <div style="background: rgba(18, 17, 44, 0.7); border: 1px solid var(--border-subtle); border-left: 3px solid var(--lavender); padding: 12px 16px; border-radius: var(--radius-sm);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <strong style="color: var(--lavender-soft); font-size: 0.88rem;">${escapeHtml(h.agent)}</strong>
            <span style="font-size: 0.72rem; color: var(--accent-emerald); font-weight: 700;">● ${escapeHtml(h.status)}</span>
          </div>
          <div style="font-size: 0.76rem; color: var(--accent-cyan); margin-bottom: 4px;">Role: ${escapeHtml(h.role)}</div>
          <p style="font-size: 0.82rem; color: #cbd5e1; line-height: 1.4;">${escapeHtml(h.output)}</p>
        </div>
      `).join("");
      showToast("5 Specialized AI Agents synchronized!");
      await Promise.all([fetchProfile(), fetchCareerExplorer(), fetchProgress()]);
    }
  } catch (err) {
    elements.huddleLogsContainer.innerHTML = `<div style="color: var(--accent-rose);">Failed to coordinate agent mesh.</div>`;
  }
}

// --- Add Skill Handler ---
async function handleAddSkill(e) {
  e.preventDefault();
  const name = elements.inputSkillName.value.trim();
  const category = elements.inputSkillCategory.value;
  const stateVal = elements.inputSkillState.value;
  const prof = parseInt(elements.inputSkillProf.value, 10);

  if (!name) return;

  try {
    const res = await fetch(`${API_BASE}/skill-universe/toggle`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        learner_id: state.learnerId,
        name: name,
        category: category,
        state: stateVal,
        proficiency: prof
      })
    });
    const data = await res.json();
    if (data.status === "success") {
      showToast(`Skill '${name}' added to your Skill Universe!`);
      elements.addSkillModal.classList.remove("active");
      elements.inputSkillName.value = "";
      await Promise.all([fetchSkillUniverse(), fetchProfile(), fetchCareerExplorer()]);
    }
  } catch (err) {
    console.error("Failed to add skill:", err);
  }
}

// --- Utility Functions ---
function showToast(message) {
  const container = elements.toastContainer;
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerHTML = `
    <span style="color: var(--lavender);">✦</span>
    <span>${escapeHtml(message)}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(20px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 4200);
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
