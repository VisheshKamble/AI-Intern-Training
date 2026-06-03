import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_mistralai import ChatMistralAI
import json
import re

# -------------------- Setup --------------------
load_dotenv()

st.set_page_config(
    page_title="CineExtract — Movie Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- Custom CSS --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #13131c;
    --surface2: #1c1c2b;
    --border: #2a2a3d;
    --accent: #e8b84b;
    --accent2: #c45c3a;
    --text: #e8e8f0;
    --muted: #7a7a9a;
    --green: #4ecb71;
    --red: #e05252;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide Streamlit default chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem !important; max-width: 1200px; }

/* ---- Hero header ---- */
.hero {
    text-align: center;
    padding: 3rem 0 2rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1.1;
    margin: 0;
}
.hero-title em {
    font-style: italic;
    color: var(--accent);
}
.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
    margin-top: 0.75rem;
}

/* ---- Cards ---- */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.card-header {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card-header span { color: var(--accent); }

/* ---- Movie result card ---- */
.movie-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1.2;
}
.movie-year {
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    color: var(--accent);
    margin-left: 0.75rem;
    vertical-align: middle;
}
.badge {
    display: inline-block;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    font-size: 0.75rem;
    font-family: 'DM Mono', monospace;
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
}
.badge-accent {
    background: rgba(232, 184, 75, 0.12);
    border-color: rgba(232, 184, 75, 0.35);
    color: var(--accent);
}
.badge-cast {
    background: rgba(196, 92, 58, 0.1);
    border-color: rgba(196, 92, 58, 0.3);
    color: #e88a6a;
}
.rating-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(78, 203, 113, 0.1);
    border: 1px solid rgba(78, 203, 113, 0.3);
    color: var(--green);
    font-family: 'DM Mono', monospace;
    font-size: 0.9rem;
    font-weight: 500;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
}
.director-line {
    font-size: 0.9rem;
    color: var(--muted);
    margin-top: 0.4rem;
}
.director-line strong {
    color: var(--text);
    font-weight: 500;
}
.summary-text {
    font-size: 0.95rem;
    line-height: 1.7;
    color: #b0b0c8;
    border-left: 2px solid var(--accent);
    padding-left: 1rem;
    margin-top: 0.5rem;
}
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.2rem 0;
}
.history-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: border-color 0.2s;
}
.history-item:hover { border-color: var(--accent); }
.history-title { font-weight: 500; font-size: 0.9rem; }
.history-meta { font-size: 0.75rem; color: var(--muted); font-family: 'DM Mono', monospace; }

.status-ok {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(78, 203, 113, 0.1);
    border: 1px solid rgba(78, 203, 113, 0.25);
    color: var(--green);
    font-size: 0.78rem;
    font-family: 'DM Mono', monospace;
    padding: 0.2rem 0.65rem;
    border-radius: 6px;
}
.status-err {
    background: rgba(224, 82, 82, 0.1);
    border: 1px solid rgba(224, 82, 82, 0.25);
    color: var(--red);
}

/* ---- Inputs ---- */
textarea, .stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
}
textarea:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(232,184,75,0.15) !important;
}

/* ---- Buttons ---- */
.stButton > button {
    background: var(--accent) !important;
    color: #0a0a0f !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.5rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stButton > button[kind="secondary"] {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
}

/* ---- Tabs ---- */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    background: transparent !important;
    border: none !important;
    padding: 0.75rem 1.25rem !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 1.5rem 0 0 0 !important;
}

/* ---- Code block ---- */
.stCodeBlock { border-radius: 8px !important; }

/* ---- Expander ---- */
.streamlit-expanderHeader {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    color: var(--muted) !important;
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* ---- Spinner ---- */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ---- Select/Radio ---- */
.stRadio > label, .stSelectbox > label { color: var(--muted) !important; font-size: 0.8rem !important; }
</style>
""", unsafe_allow_html=True)


# -------------------- Model Setup --------------------
@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-2506")

model = get_model()


# -------------------- Schema --------------------
class Movie(BaseModel):
    title: str
    release_year: Optional[int] = None
    genre: List[str] = []
    director: Optional[str] = None
    cast: List[str] = []
    rating: Optional[float] = None
    summary: str
    language: Optional[str] = None
    country: Optional[str] = None
    awards: Optional[str] = None

parser = PydanticOutputParser(pydantic_object=Movie)

SYSTEM_PROMPT = """You are a precise movie information extractor.
Extract every detail from the paragraph that matches the schema.
For fields not mentioned, return null or empty list as appropriate.
Be conservative — only fill fields with information explicitly stated or strongly implied.
{format_instructions}"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{paragraph}")
])


# -------------------- Session State --------------------
if "history" not in st.session_state:
    st.session_state.history = []  # list of Movie dicts
if "active_movie" not in st.session_state:
    st.session_state.active_movie = None
if "raw_output" not in st.session_state:
    st.session_state.raw_output = None


# -------------------- Hero --------------------
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">▸ AI-Powered Extraction</div>
    <h1 class="hero-title">Cine<em>Extract</em></h1>
    <p class="hero-sub">Paste any film description — get clean, structured movie intelligence</p>
</div>
""", unsafe_allow_html=True)


# -------------------- Layout --------------------
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown('<div class="card-header"><span>01</span> INPUT</div>', unsafe_allow_html=True)

    # Sample paragraphs
    samples = {
        "— choose a sample —": "",
        "The Dark Knight (2008)": "The Dark Knight is a 2008 superhero film directed by Christopher Nolan. Starring Christian Bale as Batman alongside Heath Ledger's Oscar-winning performance as the Joker, Michael Caine, and Maggie Gyllenhaal. Rated 9.0 on IMDb, it's widely considered one of the greatest films ever made. The film explores themes of chaos, morality, and heroism in Gotham City.",
        "Parasite (2019)": "Parasite is a 2019 South Korean black comedy thriller directed by Bong Joon-ho. It stars Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong, and Choi Woo-shik. The film won the Palme d'Or at Cannes and became the first non-English-language film to win the Academy Award for Best Picture. IMDb rating: 8.5.",
        "Inception (2010)": "Inception (2010) is a mind-bending sci-fi thriller helmed by director Christopher Nolan, featuring Leonardo DiCaprio, Joseph Gordon-Levitt, and Elliot Page. The film scored a perfect 8.8 on IMDb and won four Academy Awards. It follows Dom Cobb, a thief who enters the dreams of others to steal secrets from their subconscious.",
    }

    chosen = st.selectbox("Load a sample", list(samples.keys()), label_visibility="collapsed")

    default_text = samples[chosen] if chosen != "— choose a sample —" else ""
    paragraph = st.text_area(
        "Movie description",
        value=default_text,
        height=220,
        placeholder="Paste any paragraph describing a movie — synopsis, review, Wikipedia snippet, anything...",
        label_visibility="collapsed"
    )

    char_count = len(paragraph)
    st.markdown(f'<p style="font-family:\'DM Mono\',monospace;font-size:0.7rem;color:var(--muted);text-align:right">{char_count} chars</p>', unsafe_allow_html=True)

    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
    with col_btn1:
        extract_btn = st.button("⟶ Extract Movie Data", use_container_width=True)
    with col_btn2:
        clear_btn = st.button("Clear", use_container_width=True)
    with col_btn3:
        history_btn = st.button("History", use_container_width=True)

    if clear_btn:
        st.session_state.active_movie = None
        st.session_state.raw_output = None
        st.rerun()

    # ---- Extraction Logic ----
    if extract_btn:
        if not paragraph.strip():
            st.warning("⚠ Please enter a paragraph first.")
        else:
            with st.spinner("Extracting movie intelligence..."):
                try:
                    final_prompt = prompt.invoke({
                        "paragraph": paragraph,
                        "format_instructions": parser.get_format_instructions()
                    })
                    response = model.invoke(final_prompt)
                    raw = response.content

                    # Strip markdown fences if present
                    clean = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
                    movie_data = parser.parse(clean)

                    st.session_state.active_movie = movie_data
                    st.session_state.raw_output = raw

                    # Deduplicate history by title
                    existing_titles = [h["title"] for h in st.session_state.history]
                    if movie_data.title not in existing_titles:
                        st.session_state.history.insert(0, movie_data.dict())

                    st.rerun()

                except Exception as e:
                    st.markdown('<span class="status-ok status-err">✗ Extraction failed</span>', unsafe_allow_html=True)
                    with st.expander("Error details"):
                        st.exception(e)

    # ---- History Panel ----
    if history_btn and st.session_state.history:
        st.markdown("---")
        st.markdown('<div class="card-header"><span>↺</span> RECENT EXTRACTIONS</div>', unsafe_allow_html=True)
        for i, h in enumerate(st.session_state.history[:5]):
            genres = ", ".join(h.get("genre", [])[:2]) or "—"
            year = h.get("release_year") or "?"
            if st.button(f"🎬 {h['title']} ({year})  ·  {genres}", key=f"hist_{i}"):
                st.session_state.active_movie = Movie(**h)
                st.rerun()


with right:
    st.markdown('<div class="card-header"><span>02</span> RESULT</div>', unsafe_allow_html=True)

    movie = st.session_state.active_movie

    if movie is None:
        st.markdown("""
        <div style="
            border: 1px dashed #2a2a3d;
            border-radius: 12px;
            padding: 3rem 2rem;
            text-align: center;
            color: #4a4a6a;
        ">
            <div style="font-size:2.5rem;margin-bottom:1rem">🎞</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.75rem;letter-spacing:0.15em">
                AWAITING EXTRACTION
            </div>
            <div style="font-size:0.85rem;margin-top:0.5rem;color:#3a3a5a">
                Paste a description and hit Extract
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        tab1, tab2, tab3 = st.tabs(["OVERVIEW", "RAW JSON", "EXPORT"])

        with tab1:
            # Title + year + rating row
            rating_html = f'<span class="rating-pill">★ {movie.rating}</span>' if movie.rating else ""
            year_html = f'<span class="movie-year">{movie.release_year}</span>' if movie.release_year else ""
            st.markdown(f"""
            <div style="margin-bottom:1rem">
                <span class="movie-title">{movie.title}</span>{year_html}
                <div style="margin-top:0.5rem">{rating_html}</div>
            </div>
            """, unsafe_allow_html=True)

            if movie.director:
                st.markdown(f'<p class="director-line">Directed by <strong>{movie.director}</strong></p>', unsafe_allow_html=True)

            extra_meta = []
            if movie.language:
                extra_meta.append(f"🌐 {movie.language}")
            if movie.country:
                extra_meta.append(f"📍 {movie.country}")
            if extra_meta:
                st.markdown(f'<p class="director-line">{" &nbsp;·&nbsp; ".join(extra_meta)}</p>', unsafe_allow_html=True)

            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            # Genres
            if movie.genre:
                st.markdown('<div class="section-label">Genres</div>', unsafe_allow_html=True)
                badges = "".join(f'<span class="badge badge-accent">{g}</span>' for g in movie.genre)
                st.markdown(f'<div>{badges}</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

            # Cast
            if movie.cast:
                st.markdown('<div class="section-label">Cast</div>', unsafe_allow_html=True)
                cast_badges = "".join(f'<span class="badge badge-cast">{c}</span>' for c in movie.cast)
                st.markdown(f'<div>{cast_badges}</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

            # Awards
            if movie.awards:
                st.markdown('<div class="section-label">Awards</div>', unsafe_allow_html=True)
                st.markdown(f'<p style="font-size:0.9rem;color:#b0b0c8">🏆 {movie.awards}</p>', unsafe_allow_html=True)

            # Summary
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Summary</div>', unsafe_allow_html=True)
            st.markdown(f'<p class="summary-text">{movie.summary}</p>', unsafe_allow_html=True)

            st.markdown('<br><span class="status-ok">✓ Extraction complete</span>', unsafe_allow_html=True)

        with tab2:
            raw = st.session_state.raw_output or ""
            clean = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
            try:
                parsed_json = json.loads(clean)
                st.json(parsed_json)
            except Exception:
                st.code(raw, language="json")

        with tab3:
            movie_dict = movie.dict()
            json_str = json.dumps(movie_dict, indent=2)

            st.markdown('<div class="section-label">Download as JSON</div>', unsafe_allow_html=True)
            st.download_button(
                label="⬇ Download JSON",
                data=json_str,
                file_name=f"{movie.title.replace(' ', '_').lower()}_data.json",
                mime="application/json",
                use_container_width=True
            )

            st.markdown('<br><div class="section-label">Copy-ready JSON</div>', unsafe_allow_html=True)
            st.code(json_str, language="json")

            # CSV-style flat row
            st.markdown('<br><div class="section-label">Flat Summary (CSV row)</div>', unsafe_allow_html=True)
            flat = {
                "title": movie.title,
                "year": movie.release_year,
                "director": movie.director,
                "genres": " | ".join(movie.genre),
                "cast": " | ".join(movie.cast),
                "rating": movie.rating,
                "language": movie.language,
                "country": movie.country,
            }
            flat_csv = ",".join(str(v or "") for v in flat.values())
            st.code(flat_csv, language="text")