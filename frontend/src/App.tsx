import {
  AlertCircle,
  ArrowRight,
  BadgeCheck,
  BarChart3,
  BookOpenCheck,
  Calculator,
  CheckCircle2,
  ClipboardCheck,
  Copy,
  DatabaseZap,
  FileText,
  Gavel,
  Home,
  LayoutDashboard,
  Link as LinkIcon,
  Loader2,
  LogIn,
  Menu,
  Scale,
  Search,
  ShieldCheck,
  SlidersHorizontal,
  Upload,
  X,
} from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import type { FormEvent, ReactNode } from 'react'
import './index.css'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const API_ENABLED = import.meta.env.VITE_API_ENABLED === 'true'

type PageKey =
  | 'landing'
  | 'dashboard'
  | 'seat-allocation'
  | 'rules'
  | 'clause-generation'
  | 'cost-estimate'
  | 'outputs'
  | 'integrity'

type SeatResult = {
  rank: number
  seat_id: number
  institution_id: number
  score: number
  rationale: string
  pros: string[]
  cons: string[]
  citations: { label?: string; source_url?: string; url?: string }[]
}

type ClauseRead = {
  generated_text: string
  pathology_check_notes: string[]
}

type CostEstimateRead = {
  estimated_admin_fee: number
  estimated_tribunal_fee_min: number
  estimated_tribunal_fee_max: number
  estimated_duration_months_min: number
  estimated_duration_months_max: number
  breakdown: { verified?: boolean }
}

type RuleRead = {
  id: number
  institution_id: number
  rules_name: string
  version_year: number | null
  summary: string | null
  source_url: string
}

const seats = [
  { id: 1, name: 'London, UK', country: 'United Kingdom' },
  { id: 2, name: 'Singapore', country: 'Singapore' },
  { id: 3, name: 'Hong Kong SAR', country: 'Hong Kong SAR, China' },
  { id: 4, name: 'New York, USA', country: 'United States' },
  { id: 5, name: 'Mumbai, India', country: 'India' },
  { id: 6, name: 'New Delhi, India', country: 'India' },
]

const institutions = [
  { id: 1, short_code: 'LCIA', name: 'London Court of International Arbitration', website_url: 'https://www.lcia.org/' },
  { id: 2, short_code: 'HKIAC', name: 'Hong Kong International Arbitration Centre', website_url: 'https://hkiac.org/' },
  { id: 3, short_code: 'ICDR', name: 'International Centre for Dispute Resolution', website_url: 'https://www.icdr.org/' },
  { id: 4, short_code: 'SIAC', name: 'Singapore International Arbitration Centre', website_url: 'https://siac.org.sg/' },
  { id: 5, short_code: 'MCIA', name: 'Mumbai Centre for International Arbitration', website_url: 'https://mcia.org.in/' },
  { id: 6, short_code: 'DIAC-DELHI', name: 'Delhi International Arbitration Centre', website_url: 'https://dhcdiac.nic.in/' },
  { id: 7, short_code: 'ICA', name: 'Indian Council of Arbitration', website_url: 'https://www.icaindia.co.in/' },
  { id: 8, short_code: 'IIAC', name: 'India International Arbitration Centre', website_url: 'https://iiac.gov.in/' },
]

const rules: RuleRead[] = [
  {
    id: 1,
    institution_id: 1,
    rules_name: 'LCIA Arbitration Rules 2020',
    version_year: 2020,
    summary: 'Commencement, tribunal formation, proceedings, and emergency arbitrator provisions.',
    source_url: 'https://www.lcia.org/Dispute_Resolution_Services/lcia-arbitration-rules-2020.aspx',
  },
  {
    id: 2,
    institution_id: 2,
    rules_name: 'HKIAC 2024 Administered Arbitration Rules',
    version_year: 2024,
    summary: 'Primary administered-arbitration rules published by HKIAC.',
    source_url: 'https://hkiac.org/arbitration/rules-and-practice-notes/2024-administered-arbitration-rules/',
  },
  {
    id: 3,
    institution_id: 4,
    rules_name: 'SIAC Rules 2025',
    version_year: 2025,
    summary: 'Current SIAC administered-arbitration rules tracked as a primary source.',
    source_url: 'https://siac.org.sg/siac-rules-2025',
  },
  {
    id: 4,
    institution_id: 5,
    rules_name: 'MCIA Arbitration Rules 2016, revised 2025',
    version_year: 2025,
    summary: 'Domestic and India-related commercial arbitration rules.',
    source_url: 'https://blog.ipleaders.in/arbitral-institutions-in-india/',
  },
  {
    id: 5,
    institution_id: 6,
    rules_name: 'Delhi International Arbitration Centre Rules 2023',
    version_year: 2023,
    summary: 'Court-annexed Delhi institutional rules; full name avoids Dubai DIAC ambiguity.',
    source_url: 'https://blog.ipleaders.in/arbitral-institutions-in-india/',
  },
  {
    id: 6,
    institution_id: 7,
    rules_name: 'Indian Council of Arbitration Rules',
    version_year: null,
    summary: 'Domestic institution used in trade, commodity, and maritime matters.',
    source_url: 'https://blog.ipleaders.in/arbitral-institutions-in-india/',
  },
  {
    id: 7,
    institution_id: 8,
    rules_name: 'India International Arbitration Centre Rules',
    version_year: null,
    summary: 'Statutory India-backed institution intended to support institutional arbitration.',
    source_url: 'https://blog.ipleaders.in/arbitral-institutions-in-india/',
  },
]

const crossBorderFallbackResults: SeatResult[] = [
  {
    rank: 1,
    seat_id: 2,
    institution_id: 4,
    score: 4.7,
    rationale: 'Singapore with SIAC balances neutral court support, cross-border enforcement, and efficient procedure for Asia-Pacific disputes.',
    pros: ['Neutral forum with NY Convention enforcement', 'Institutional rules and seat are naturally aligned', 'Good fit for technology and trade contracts'],
    cons: ['Fee figures in this prototype are not verified for production use', 'Indian domestic disputes may still prefer a local seat'],
    citations: [{ label: 'SIAC Rules 2025', source_url: 'https://siac.org.sg/siac-rules-2025' }],
  },
  {
    rank: 2,
    seat_id: 1,
    institution_id: 1,
    score: 4.4,
    rationale: 'London with LCIA is strong where court support, neutrality, and enforcement confidence outweigh cost concerns.',
    pros: ['Deep supervisory court experience', 'High neutrality score', 'Strong for finance, infrastructure, and cross-border assets'],
    cons: ['Premium cost profile', 'May be less natural for India-only matters'],
    citations: [{ label: 'LCIA Rules', source_url: 'https://www.lcia.org/Dispute_Resolution_Services/lcia-arbitration-rules-2020.aspx' }],
  },
]

const domesticFallbackResults: SeatResult[] = [
  {
    rank: 1,
    seat_id: 6,
    institution_id: 6,
    score: 4.3,
    rationale: 'New Delhi with the Delhi International Arbitration Centre is strong when fast supervisory-court access, neutral appointment, and Section 9/11/34 readiness matter for an India-seated dispute.',
    pros: ['Court-annexed institutional administration', 'Useful where Delhi High Court access is important', 'Emergency and appointment mechanics are clearer than pure ad hoc'],
    cons: ['Spell out Delhi International Arbitration Centre to avoid Dubai DIAC ambiguity', 'Check the current published fee schedule before client use'],
    citations: [{ label: 'iPleaders: Arbitral Institutions in India', source_url: 'https://blog.ipleaders.in/arbitral-institutions-in-india/' }],
  },
  {
    rank: 2,
    seat_id: 5,
    institution_id: 5,
    score: 4.1,
    rationale: 'Mumbai with MCIA fits domestic commercial, finance, shareholder, and India-related disputes where the parties want a modern institutional rulebook and predictable fees.',
    pros: ['Natural domestic commercial institution', 'Mumbai commercial ecosystem and hearing infrastructure', 'Published institutional rules and fees'],
    cons: ['Caseload remains smaller than major offshore hubs', 'Court delay risk still belongs in the drafting memo'],
    citations: [{ label: 'iPleaders: Arbitral Institutions in India', source_url: 'https://blog.ipleaders.in/arbitral-institutions-in-india/' }],
  },
  {
    rank: 3,
    seat_id: 6,
    institution_id: 7,
    score: 3.7,
    rationale: 'New Delhi with ICA remains useful for trade, commodity, and maritime contracts that already expect ICA administration.',
    pros: ['Long-standing Indian arbitration institution', 'Sector fit for trade and commodity matters'],
    cons: ['May be less natural for modern general commercial disputes than MCIA or Delhi DIAC', 'Verify current rules and fee schedule before drafting'],
    citations: [{ label: 'iPleaders: Arbitral Institutions in India', source_url: 'https://blog.ipleaders.in/arbitral-institutions-in-india/' }],
  },
]

const navItems = [
  { key: 'landing' as const, label: 'Landing', icon: <Home size={18} />, guardrail: 'Public USP page' },
  { key: 'dashboard' as const, label: 'Dashboard', icon: <LayoutDashboard size={18} />, guardrail: 'Lawyer workspace' },
  { key: 'seat-allocation' as const, label: 'Seat Allocation', icon: <Scale size={18} />, guardrail: 'Manual weights required' },
  { key: 'rules' as const, label: 'Rule Tracking', icon: <BookOpenCheck size={18} />, guardrail: 'Primary sources only' },
  { key: 'clause-generation' as const, label: 'Clause Generation', icon: <FileText size={18} />, guardrail: 'Pathology notes shown' },
  { key: 'cost-estimate' as const, label: 'Cost Estimate', icon: <Calculator size={18} />, guardrail: 'Unverified fees flagged' },
  { key: 'outputs' as const, label: 'Final Outputs', icon: <ClipboardCheck size={18} />, guardrail: 'Lawyer bundle' },
  { key: 'integrity' as const, label: 'Data Integrity', icon: <ShieldCheck size={18} />, guardrail: 'No numeric invention' },
]

function App() {
  const [page, setPage] = useHashPage()
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [page])

  return (
    <div className="min-h-screen bg-[var(--canvas)] text-[var(--ink)]">
      <a className="skip-link" href="#main">Skip to content</a>
      <TopNav page={page} setPage={setPage} menuOpen={menuOpen} setMenuOpen={setMenuOpen} />
      <div className={page === 'landing' ? 'app-frame landing-mode' : 'app-frame'}>
        <SideNav page={page} setPage={setPage} menuOpen={menuOpen} closeMenu={() => setMenuOpen(false)} />
        <main id="main" tabIndex={-1} className="main-shell">
          {page === 'landing' && <LandingPage setPage={setPage} />}
          {page === 'dashboard' && <DashboardPage setPage={setPage} />}
          {page === 'seat-allocation' && <SeatAllocationPage setPage={setPage} />}
          {page === 'rules' && <RulesPage />}
          {page === 'clause-generation' && <ClausePage />}
          {page === 'cost-estimate' && <CostPage />}
          {page === 'outputs' && <OutputsPage setPage={setPage} />}
          {page === 'integrity' && <IntegrityPage />}
        </main>
      </div>
    </div>
  )
}

function useHashPage(): [PageKey, (key: PageKey) => void] {
  const readPage = (): PageKey => {
    const hash = window.location.hash.replace('#/', '') as PageKey
    return navItems.some((item) => item.key === hash) ? hash : 'landing'
  }
  const [page, setPageState] = useState<PageKey>(readPage)
  useEffect(() => {
    const onHash = () => setPageState(readPage())
    window.addEventListener('hashchange', onHash)
    return () => window.removeEventListener('hashchange', onHash)
  }, [])
  const setPage = (key: PageKey) => {
    window.location.hash = `/${key}`
    setPageState(key)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
  return [page, setPage]
}

function TopNav({ page, setPage, menuOpen, setMenuOpen }: { page: PageKey; setPage: (key: PageKey) => void; menuOpen: boolean; setMenuOpen: (value: boolean) => void }) {
  return (
    <header className="top-nav">
      <button className="icon-button lg:hidden" type="button" onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle navigation">{menuOpen ? <X size={20} /> : <Menu size={20} />}</button>
      <button className="brand-lockup" type="button" onClick={() => setPage('landing')} aria-label="Go to landing page"><span className="brand-mark">A</span><span><span className="brand-name">Arbitrium</span><span className="brand-subtitle">Arbitration intelligence</span></span></button>
      <nav className="hidden items-center gap-1 xl:flex" aria-label="Primary">
        {navItems.slice(1, 6).map((item) => <button key={item.key} className={page === item.key ? 'top-link active' : 'top-link'} type="button" onClick={() => setPage(item.key)}>{item.label}</button>)}
      </nav>
      <div className="ml-auto flex items-center gap-2"><div className="search-chip hidden md:flex"><Search size={16} /><span>Search matter, seat, clause</span></div><button className="secondary-button hidden sm:inline-flex" type="button" onClick={() => setPage('dashboard')}><LogIn size={16} />Lawyer Login</button></div>
    </header>
  )
}

function SideNav({ page, setPage, closeMenu, menuOpen }: { page: PageKey; setPage: (key: PageKey) => void; closeMenu: () => void; menuOpen: boolean }) {
  return (
    <aside className={menuOpen ? 'side-nav open' : 'side-nav'} aria-label="Workflow navigation">
      <div className="side-section">
        <p className="side-label">Lawyer workflow</p>
        {navItems.map((item) => (
          <button key={item.key} className={page === item.key ? 'side-link active' : 'side-link'} type="button" onClick={() => { setPage(item.key); closeMenu() }}>
            {item.icon}<span><strong>{item.label}</strong><small>{item.guardrail}</small></span>
          </button>
        ))}
      </div>
      <div className="integrity-card"><ShieldCheck size={18} /><p>Every legal claim must point to a stored source. Unknown figures stay unknown.</p></div>
    </aside>
  )
}

function LandingPage({ setPage }: { setPage: (key: PageKey) => void }) {
  return (
    <div className="landing">
      <ScrollHero setPage={setPage} />
      <section className="landing-section two-column reveal"><div><p className="eyebrow">Problem</p><h2>Arbitration clauses are too often copied before the seat is tested.</h2></div><div className="copy-stack"><p>Arbitrium turns contract facts, enforcement needs, institutional rules, and source-backed reference data into a defensible drafting record.</p><p>The market has broad legal analytics, institution clause tools, and general AI assistants. Arbitrium is narrower by design: seat, institution, cost, rule, and clause logic in one arbitration workflow.</p></div></section>
      <section className="landing-section feature-band reveal"><div className="feature-copy"><p className="eyebrow">USP 1</p><h2>Seat suggestions with a paper trail.</h2><p>Recommendations break down speed, cost, neutrality, and enforceability instead of handing lawyers a black-box ranking.</p></div><div className="feature-grid">{['Weighted priorities', 'Pros and cons', 'Source citations', 'Clause handoff'].map((item) => <span key={item}>{item}</span>)}</div></section>
      <section className="landing-section split-proof reveal"><div className="proof-panel"><DatabaseZap size={28} /><h3>Truth-first extraction</h3><p>The AI engine accepts a numeric fact only when its source excerpt appears in retrieved text.</p></div><div className="proof-panel warm"><Gavel size={28} /><h3>Drafting guardrails</h3><p>Clause output includes pathology checks for seat, institution, arbitrator count, language, and governing law.</p></div></section>
      <section className="landing-section final-cta reveal keep-visible"><p className="eyebrow">Final prototype</p><h2>Move from clause instinct to arbitration reasoning.</h2><p>Start with a seat recommendation, refine the clause, review cost exposure, and export the lawyer-facing bundle.</p><button className="primary-button" type="button" onClick={() => setPage('dashboard')}>Enter prototype <ArrowRight size={18} /></button></section>
    </div>
  )
}

function ScrollHero({ setPage }: { setPage: (key: PageKey) => void }) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const heroRef = useRef<HTMLElement>(null)
  const [progress, setProgress] = useState(0)
  const [videoReady, setVideoReady] = useState(false)
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    const gates = ['(max-width: 720px)', '(orientation: portrait) and (max-width: 1024px)', '(orientation: portrait) and (pointer: coarse)', '(orientation: landscape) and (pointer: coarse) and (max-height: 560px)', '(prefers-reduced-motion: reduce)']
    const media = gates.map((query) => matchMedia(query))
    let objectUrl = ''
    let cancelled = false
    const loadVideo = async () => {
      if (media.some((item) => item.matches) || !videoRef.current || objectUrl) return
      try {
        const response = await fetch('/assets/hero-scrub.mp4')
        const blob = await response.blob()
        if (cancelled || !videoRef.current) return
        objectUrl = URL.createObjectURL(blob)
        videoRef.current.src = objectUrl
        videoRef.current.load()
        videoRef.current.addEventListener('canplay', () => setVideoReady(true), { once: true })
      } catch {
        setFailed(true)
      }
    }
    const applyMode = () => {
      if (media.some((item) => item.matches)) {
        setVideoReady(false)
        return
      }
      void loadVideo()
    }
    media.forEach((item) => item.addEventListener('change', applyMode))
    applyMode()
    return () => {
      cancelled = true
      media.forEach((item) => item.removeEventListener('change', applyMode))
      if (objectUrl) URL.revokeObjectURL(objectUrl)
    }
  }, [])

  useEffect(() => {
    let raf = 0
    let shown = 0
    let seekBusy = false
    let pendingTime: number | null = null
    const requestSeek = (time: number) => {
      const video = videoRef.current
      if (!video?.duration) return
      if (seekBusy) {
        pendingTime = time
        return
      }
      seekBusy = true
      video.currentTime = time
    }
    const onSeeked = () => {
      seekBusy = false
      if (pendingTime !== null) {
        const next = pendingTime
        pendingTime = null
        requestSeek(next)
      }
    }
    const tick = () => {
      const hero = heroRef.current
      const video = videoRef.current
      if (!hero) return
      const rect = hero.getBoundingClientRect()
      const range = hero.offsetHeight - window.innerHeight
      const next = Math.min(1, Math.max(0, -rect.top / Math.max(1, range)))
      shown += (next - shown) * 0.18
      setProgress(next)
      if (video?.duration && videoReady) requestSeek(shown * video.duration)
      if (Math.abs(next - shown) > 0.0008) raf = requestAnimationFrame(tick)
      else raf = 0
    }
    const onScroll = () => {
      if (!raf) raf = requestAnimationFrame(tick)
    }
    const video = videoRef.current
    video?.addEventListener('seeked', onSeeked)
    video?.addEventListener('error', () => {
      seekBusy = false
      pendingTime = null
      setFailed(true)
    })
    window.addEventListener('scroll', onScroll, { passive: true })
    window.addEventListener('resize', onScroll)
    onScroll()
    return () => {
      window.removeEventListener('scroll', onScroll)
      window.removeEventListener('resize', onScroll)
      video?.removeEventListener('seeked', onSeeked)
      if (raf) cancelAnimationFrame(raf)
    }
  }, [videoReady])

  const active = progress < 0.2 ? 0 : progress < 0.46 ? 1 : progress < 0.74 ? 2 : 3
  return (
    <section ref={heroRef} className="scroll-hero" aria-label="Arbitrium landing story">
      <div className="hero-stage">
        <div className="poster-layer" /><video ref={videoRef} className={videoReady ? 'hero-video ready' : 'hero-video'} preload="none" muted playsInline aria-hidden="true" tabIndex={-1} /><div className="hero-scrim" />
        {!videoReady && !failed && <Loader2 className="hero-loader" size={28} aria-hidden="true" />}
        <div className={`hero-band band-${active + 1}`}>
          {active === 0 && <><p className="eyebrow">Arbitration intelligence</p><h1>Draft the clause after the seat has earned it.</h1><p>Seat fit, institutional rules, enforcement risk, and clause wording in one review flow.</p><button className="primary-button" type="button" onClick={() => setPage('seat-allocation')}>Start seat review <ArrowRight size={18} /></button></>}
          {active === 1 && <><p className="eyebrow">No black box</p><h2>See why a seat was ranked.</h2><p>Each score is split into speed, cost, neutrality, and enforceability with citations attached.</p></>}
          {active === 2 && <><p className="eyebrow">Clause safety</p><h2>Generate wording, then inspect its risks.</h2><p>Missing seat, mismatched institution, and governing-law gaps are shown before the clause leaves the page.</p></>}
          {active === 3 && <><p className="eyebrow">Lawyer-ready output</p><h2>One bundle for the drafting record.</h2><p>Recommendation, rule links, clause text, cost caveats, and data status travel together.</p></>}
        </div>
      </div>
    </section>
  )
}

function DashboardPage({ setPage }: { setPage: (key: PageKey) => void }) {
  return <PageWrap eyebrow="Dashboard" title="Arbitrium workspace" description="A command surface for seat choice, clauses, costs, and source review."><MetricGrid /><div className="dashboard-grid"><Panel title="Matter intake" icon={<Upload size={20} />}><p className="muted">Upload a contract or start manually. Slider weights remain required by design.</p><div className="button-row"><button className="primary-button" type="button" onClick={() => setPage('seat-allocation')}>Analyze seat <ArrowRight size={16} /></button><button className="secondary-button" type="button" onClick={() => setPage('clause-generation')}>Generate clause</button></div></Panel><Panel title="Recent lawyer outputs" icon={<ClipboardCheck size={20} />}><Timeline items={[['Seat recommendation', 'Singapore + SIAC ranked first for neutral cross-border posture.'], ['Clause draft', 'Three-member tribunal clause passed pathology checks.'], ['Cost review', 'Prototype fee schedule flagged as unverified.']]} /></Panel><Panel title="Integrity status" icon={<ShieldCheck size={20} />}><StatusList items={[['Backend APIs', 'Implemented for all PRD pages', 'ready'], ['Annual report figures', 'Awaiting verified values', 'warn'], ['AI extraction guard', 'Rejects unsupported numeric facts', 'ready']]} /></Panel></div></PageWrap>
}

function MetricGrid() {
  const metrics = [['5', 'Core pages', 'Dashboard, seat, rules, clause, cost'], ['4', 'Scoring weights', 'Speed, cost, neutrality, enforcement'], ['0', 'Invented figures', 'Unknown numbers stay blank'], ['1', 'Export bundle', 'Lawyer-facing final content']]
  return <section className="metric-grid" aria-label="Prototype metrics">{metrics.map(([value, label, detail]) => <article className="metric-card" key={label}><p>{label}</p><strong>{value}</strong><span>{detail}</span></article>)}</section>
}

function SeatAllocationPage({ setPage }: { setPage: (key: PageKey) => void }) {
  const [weights, setWeights] = useState({ speed: 25, cost: 20, neutrality: 25, enforceability: 30 })
  const [arbitrationType, setArbitrationType] = useState<'domestic' | 'cross_border'>('domestic')
  const [scope, setScope] = useState('Domestic Indian commercial contract with possible Section 9 interim relief needs')
  const [governingLaw, setGoverningLaw] = useState('Indian law')
  const [claimQuantum, setClaimQuantum] = useState(6000000)
  const [sector, setSector] = useState('General Commercial, Shareholder Agreements, Joint Ventures and M&A')
  const [region, setRegion] = useState('Multi-state / Pan-India Operations')
  const [courtPriority, setCourtPriority] = useState('Extremely high: urgent pre-arbitral interim relief is probable')
  const [results, setResults] = useState<SeatResult[]>(domesticFallbackResults)
  const [loading, setLoading] = useState(false)
  const [source, setSource] = useState<'api' | 'demo'>('demo')
  const analyze = async (event: FormEvent) => {
    event.preventDefault()
    setLoading(true)
    const normalized = normalizeWeights(weights)
    try {
      if (!API_ENABLED) throw new Error('demo mode')
      const response = await fetch(`${API_BASE}/api/v1/seat-allocation/analyze`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ arbitration_type: arbitrationType, parties: [{ name: 'Claimant entity', role: 'claimant', jurisdiction: 'India' }, { name: 'Respondent entity', role: 'respondent', jurisdiction: arbitrationType === 'domestic' ? 'India' : 'Singapore' }], scope: `${scope}. Sector: ${sector}. Geography: ${region}. Court intervention priority: ${courtPriority}.`, claim_quantum: claimQuantum, claim_currency: 'USD', governing_law: governingLaw, priority_speed: normalized.speed, priority_cost: normalized.cost, priority_neutrality: normalized.neutrality, priority_enforceability: normalized.enforceability }) })
      if (!response.ok) throw new Error('analysis failed')
      const data = (await response.json()) as { results: SeatResult[] }
      setResults(data.results)
      setSource('api')
    } catch {
      setResults(arbitrationType === 'domestic' ? domesticFallbackResults : crossBorderFallbackResults)
      setSource('demo')
    } finally {
      setLoading(false)
    }
  }
  return <PageWrap eyebrow="Seat Allocation" title="Choose a domestic Indian seat with reasons, not habit." description="Questionnaire fields track sector, geography, neutrality, High Court access, infrastructure, counsel base, and claim value."><div className="workflow-grid"><form className="panel" onSubmit={analyze}><div className="panel-heading"><SlidersHorizontal size={20} /><h2>Intake</h2></div><label>Arbitration path<select value={arbitrationType} onChange={(event) => setArbitrationType(event.target.value as 'domestic' | 'cross_border')}><option value="domestic">Domestic arbitration</option><option value="cross_border">Cross-border arbitration</option></select></label><label>Contract scope<textarea value={scope} onChange={(event) => setScope(event.target.value)} /></label><label>Sector<select value={sector} onChange={(event) => setSector(event.target.value)}><option>Construction, Engineering and Infrastructure</option><option>Financial Services, Banking, Securities and Private Equity / VC</option><option>Information Technology, IP, Software and E-Commerce</option><option>Energy, Oil and Gas, Mining and Utilities</option><option>General Commercial, Shareholder Agreements, Joint Ventures and M&A</option></select></label><label>Geographic proximity<select value={region} onChange={(event) => setRegion(event.target.value)}><option>Northern Region</option><option>Western Region</option><option>Southern Region</option><option>Eastern / North-Eastern Region</option><option>Multi-state / Pan-India Operations</option></select></label><label>Court intervention need<select value={courtPriority} onChange={(event) => setCourtPriority(event.target.value)}><option>Extremely high: urgent pre-arbitral interim relief is probable</option><option>Moderate: interim relief may be needed</option><option>Low: primarily monetary or post-completion damages</option></select></label><label>Governing law<input value={governingLaw} onChange={(event) => setGoverningLaw(event.target.value)} /></label><label>Claim quantum, USD<input type="number" value={claimQuantum} min={0} onChange={(event) => setClaimQuantum(Number(event.target.value))} /></label><div className="slider-stack">{Object.entries(weights).map(([key, value]) => <label key={key}><span>{titleCase(key)} {value}%</span><input type="range" min={0} max={100} value={value} onChange={(event) => setWeights({ ...weights, [key]: Number(event.target.value) })} /></label>)}</div><div className="button-row"><button className="primary-button" disabled={loading} type="submit">{loading ? <Loader2 className="spin" size={16} /> : <Scale size={16} />}Run allocation</button><button className="secondary-button" type="button"><Upload size={16} />Upload contract</button></div><p className="fine-print">API mode: {source === 'api' ? 'live backend response' : 'demo data because the backend is offline or not seeded'}</p></form><aside className="guidance-stack"><Panel title="Domestic arbitration" icon={<Home size={18} />}><p className="muted">For India-seated disputes, the juridical seat anchors supervisory High Court jurisdiction for interim relief, appointments, and set-aside challenges.</p></Panel><Panel title="Institutional fit" icon={<Gavel size={18} />}><p className="muted">For domestic commercial matters, MCIA and Delhi DIAC lead the shortlist; ICA remains sector-useful and IIAC is the statutory option.</p></Panel></aside></div><ResultList results={results} setPage={setPage} /></PageWrap>
}

function ResultList({ results, setPage }: { results: SeatResult[]; setPage: (key: PageKey) => void }) {
  return <section className="results-list" aria-label="Seat allocation results">{results.map((result) => { const seat = seats.find((item) => item.id === result.seat_id); const institution = institutions.find((item) => item.id === result.institution_id); return <article className="result-card" key={`${result.rank}-${result.seat_id}`}><div className="rank">#{result.rank}</div><div><h3>{seat?.name ?? 'Recommended seat'} + {institution?.short_code ?? 'Institution'}</h3><p>{result.rationale}</p><div className="pros-cons"><div><strong>Pros</strong><ul>{result.pros.map((item) => <li key={item}>{item}</li>)}</ul></div><div><strong>Cons</strong><ul>{result.cons.map((item) => <li key={item}>{item}</li>)}</ul></div></div><div className="citation-row">{result.citations.map((citation) => <a key={citation.source_url ?? citation.url} href={citation.source_url ?? citation.url} target="_blank" rel="noreferrer"><LinkIcon size={14} />{citation.label ?? 'Source'}</a>)}</div></div><div className="score-block"><span>Score</span><strong>{result.score.toFixed(1)}</strong><button className="secondary-button" type="button" onClick={() => setPage('clause-generation')}>Use in clause</button></div></article> })}</section>
}

function RulesPage() {
  const [query, setQuery] = useState('')
  const filtered = rules.filter((rule) => rule.rules_name.toLowerCase().includes(query.toLowerCase()))
  return <PageWrap eyebrow="Live Rule Tracking" title="Primary rule sources in one review lane." description="This prototype shows tracked source links and last-check status. A production scheduler is still a known backend task."><div className="toolbar"><label className="search-input"><Search size={16} /><span className="sr-only">Search rules</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search rules or institutions" /></label></div><div className="table-wrap"><table><thead><tr><th>Institution</th><th>Rule set</th><th>Year</th><th>Status</th><th>Source</th></tr></thead><tbody>{filtered.map((rule) => <tr key={rule.id}><td>{institutions.find((item) => item.id === rule.institution_id)?.short_code}</td><td><strong>{rule.rules_name}</strong><span>{rule.summary}</span></td><td>{rule.version_year ?? 'Current hub'}</td><td><Badge tone="ready">Tracked</Badge></td><td><a href={rule.source_url} target="_blank" rel="noreferrer">Open source</a></td></tr>)}</tbody></table>{filtered.length === 0 && <p className="empty-state">No rules found.</p>}</div></PageWrap>
}

function ClausePage() {
  const [seatId, setSeatId] = useState(6)
  const [institutionId, setInstitutionId] = useState(6)
  const [arbitrators, setArbitrators] = useState<'sole' | 'three' | 'emergency'>('sole')
  const [clause, setClause] = useState<ClauseRead | null>(null)
  const [loading, setLoading] = useState(false)
  const generate = async (event: FormEvent) => {
    event.preventDefault()
    setLoading(true)
    try {
      if (!API_ENABLED) throw new Error('demo mode')
      const response = await fetch(`${API_BASE}/api/v1/clauses/generate`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ seat_id: seatId, institution_id: institutionId, num_arbitrators: arbitrators, appointment_mechanism: arbitrators === 'three' ? 'co_arbitrator_nomination' : 'institutional_default', language: 'English', governing_law_contract: 'Indian law', governing_law_arbitration: 'Indian law', party_details: [{ name: 'Claimant entity', role: 'claimant', jurisdiction: 'India' }, { name: 'Respondent entity', role: 'respondent', jurisdiction: 'India' }] }) })
      if (!response.ok) throw new Error('clause failed')
      setClause((await response.json()) as ClauseRead)
    } catch {
      setClause({ generated_text: 'Any dispute arising out of or in connection with this agreement shall be referred to and finally resolved by arbitration administered by the selected Indian institution in accordance with its arbitration rules. The seat of arbitration shall be the selected Indian seat. The tribunal shall consist of the selected number of arbitrators. The language of the arbitration shall be English.', pathology_check_notes: ['Prototype fallback text. Run the backend for institution-specific clause wording.', 'Confirm the institution name, seat, venue, governing law, tribunal size, and language before client use.'] })
    } finally {
      setLoading(false)
    }
  }
  return <PageWrap eyebrow="Clause Generation" title="Draft the arbitration agreement with pathology notes visible." description="The module takes a recommended seat or manual settings and keeps legal review warnings attached to the text."><div className="workflow-grid"><form className="panel" onSubmit={generate}><div className="panel-heading"><FileText size={20} /><h2>Clause settings</h2></div><label>Selected seat<select value={seatId} onChange={(event) => setSeatId(Number(event.target.value))}>{seats.map((seat) => <option key={seat.id} value={seat.id}>{seat.name}</option>)}</select></label><label>Institution<select value={institutionId} onChange={(event) => setInstitutionId(Number(event.target.value))}>{institutions.map((institution) => <option key={institution.id} value={institution.id}>{institution.short_code}</option>)}</select></label><label>Tribunal<select value={arbitrators} onChange={(event) => setArbitrators(event.target.value as 'sole' | 'three' | 'emergency')}><option value="sole">Sole arbitrator</option><option value="three">Three-member tribunal</option><option value="emergency">Emergency provisions</option></select></label><button className="primary-button" disabled={loading} type="submit">{loading ? <Loader2 className="spin" size={16} /> : <FileText size={16} />}Generate clause</button></form><Panel title="Generated clause" icon={<Copy size={20} />}>{clause ? <><blockquote className="clause-output">{clause.generated_text}</blockquote><StatusList items={clause.pathology_check_notes.map((note) => [note, 'Legal review required before use', note.toLowerCase().includes('fallback') ? 'warn' : 'ready'])} /></> : <p className="empty-state">No clause generated yet.</p>}</Panel></div></PageWrap>
}

function CostPage() {
  const [institutionId, setInstitutionId] = useState(4)
  const [claimAmount, setClaimAmount] = useState(2500000)
  const [estimate, setEstimate] = useState<CostEstimateRead | null>(null)
  const [loading, setLoading] = useState(false)
  const calculate = async (event: FormEvent) => {
    event.preventDefault()
    setLoading(true)
    try {
      if (!API_ENABLED) throw new Error('demo mode')
      const response = await fetch(`${API_BASE}/api/v1/cost-estimate/calculate`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ institution_id: institutionId, claim_amount: claimAmount, currency: 'USD' }) })
      if (!response.ok) throw new Error('cost failed')
      setEstimate((await response.json()) as CostEstimateRead)
    } catch {
      setEstimate({ estimated_admin_fee: Math.round(claimAmount * 0.012), estimated_tribunal_fee_min: Math.round(claimAmount * 0.025), estimated_tribunal_fee_max: Math.round(claimAmount * 0.055), estimated_duration_months_min: 12, estimated_duration_months_max: 18, breakdown: { verified: false } })
    } finally {
      setLoading(false)
    }
  }
  return <PageWrap eyebrow="Cost and Duration Estimate" title="Estimate exposure, then mark what still needs verification." description="The backend calculator works, but seeded fee rows are expressly flagged as unverified until checked against official fee schedules."><div className="workflow-grid"><form className="panel" onSubmit={calculate}><div className="panel-heading"><Calculator size={20} /><h2>Inputs</h2></div><label>Institution<select value={institutionId} onChange={(event) => setInstitutionId(Number(event.target.value))}>{institutions.map((institution) => <option key={institution.id} value={institution.id}>{institution.short_code}</option>)}</select></label><label>Claim amount, USD<input type="number" min={1} value={claimAmount} onChange={(event) => setClaimAmount(Number(event.target.value))} /></label><button className="primary-button" disabled={loading} type="submit">{loading ? <Loader2 className="spin" size={16} /> : <BarChart3 size={16} />}Calculate estimate</button></form><Panel title="Estimate" icon={<BarChart3 size={20} />}>{estimate ? <div className="estimate-grid"><Metric label="Admin fee" value={money(estimate.estimated_admin_fee)} /><Metric label="Tribunal fee range" value={`${money(estimate.estimated_tribunal_fee_min)} to ${money(estimate.estimated_tribunal_fee_max)}`} /><Metric label="Duration" value={`${estimate.estimated_duration_months_min} to ${estimate.estimated_duration_months_max} months`} /><Badge tone={estimate.breakdown.verified ? 'ready' : 'warn'}>{estimate.breakdown.verified ? 'Verified schedule' : 'Unverified prototype schedule'}</Badge></div> : <p className="empty-state">No estimate calculated yet.</p>}</Panel></div></PageWrap>
}

function OutputsPage({ setPage }: { setPage: (key: PageKey) => void }) {
  const outputs: [string, string, PageKey][] = [['Seat memo', 'Ranked seat and institution recommendation with pros, cons, weights, and citations.', 'seat-allocation'], ['Clause text', 'Generated arbitration clause plus pathology check notes.', 'clause-generation'], ['Cost note', 'Admin fee, tribunal fee, duration range, and verification status.', 'cost-estimate'], ['Source appendix', 'Rule links, annual report links, extraction guard status, and known data gaps.', 'integrity']]
  return <PageWrap eyebrow="Final Content" title="Lawyer-facing output bundle" description="A single review pack for the drafting file, with status labels and source links kept beside every major claim."><div className="output-grid">{outputs.map(([title, detail, target]) => <article className="output-card" key={title}><BadgeCheck size={24} /><h3>{title}</h3><p>{detail}</p><button className="secondary-button" type="button" onClick={() => setPage(target)}>Open <ArrowRight size={16} /></button></article>)}</div></PageWrap>
}

function IntegrityPage() {
  return <PageWrap eyebrow="Data Integrity" title="The prototype says what it knows and what it does not." description="Arbitrium is built for legal decision support, so unsupported numbers are not dressed up as facts."><div className="dashboard-grid"><Panel title="No-fabrication chain" icon={<ShieldCheck size={20} />}><StatusList items={[['Retrieved text first', 'The AI engine must search or fetch source material before answering.', 'ready'], ['Verbatim excerpts', 'Numeric facts require a source excerpt from retrieved text.', 'ready'], ['Guard check', 'Facts fail when the excerpt cannot be found in the source.', 'ready']]} /></Panel><Panel title="Known gaps" icon={<AlertCircle size={20} />}><StatusList items={[['SIAC annual report fetch', 'Requests-based fetch hit HTTP 403 and needs a browser strategy.', 'warn'], ['Fee schedules', 'Seed rows are illustrative until confirmed against official calculators.', 'warn'], ['Production database', 'PostgreSQL migration still needs a real server run.', 'warn']]} /></Panel></div></PageWrap>
}

function PageWrap({ eyebrow, title, description, children }: { eyebrow: string; title: string; description: string; children: ReactNode }) {
  return <section className="page-wrap"><div className="page-title"><p className="eyebrow">{eyebrow}</p><h1>{title}</h1><p>{description}</p></div>{children}</section>
}

function Panel({ title, icon, children }: { title: string; icon: ReactNode; children: ReactNode }) {
  return <section className="panel"><div className="panel-heading">{icon}<h2>{title}</h2></div>{children}</section>
}

function Timeline({ items }: { items: [string, string][] }) {
  return <ol className="timeline">{items.map(([title, detail]) => <li key={title}><CheckCircle2 size={18} /><span><strong>{title}</strong><small>{detail}</small></span></li>)}</ol>
}

function StatusList({ items }: { items: [string, string, string][] }) {
  return <div className="status-list">{items.map(([title, detail, tone]) => <div className="status-item" key={title}>{tone === 'ready' ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}<span><strong>{title}</strong><small>{detail}</small></span></div>)}</div>
}

function Badge({ children, tone }: { children: ReactNode; tone: 'ready' | 'warn' }) {
  return <span className={`badge ${tone}`}>{children}</span>
}

function Metric({ label, value }: { label: string; value: string }) {
  return <div className="mini-metric"><span>{label}</span><strong>{value}</strong></div>
}

function normalizeWeights(weights: { speed: number; cost: number; neutrality: number; enforceability: number }) {
  const total = Object.values(weights).reduce((sum, value) => sum + value, 0) || 1
  const rounded = { speed: roundWeight(weights.speed / total), cost: roundWeight(weights.cost / total), neutrality: roundWeight(weights.neutrality / total) }
  return { ...rounded, enforceability: roundWeight(1 - rounded.speed - rounded.cost - rounded.neutrality) }
}

function roundWeight(value: number) {
  return Math.round(value * 1000) / 1000
}

function titleCase(value: string) {
  return value.replace(/^\w/, (letter) => letter.toUpperCase())
}

function money(value: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(value)
}

export default App
