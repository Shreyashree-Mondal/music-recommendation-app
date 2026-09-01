import random
import html
import re
from urllib.parse import parse_qs, urlparse
import streamlit as st
import mysql.connector
import pandas as pd
from werkzeug.security import check_password_hash
import streamlit.components.v1 as components

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="PulseBeat",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# STYLES
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=DM+Mono:wght@400;500&family=Bebas+Neue&display=swap');

:root {
    --bg: #050508;
    --surface: #0d0d14;
    --surface2: #13131e;
    --surface3: #1a1a28;
    --border: rgba(255,255,255,0.07);
    --border2: rgba(255,255,255,0.12);
    --text: #f8f7ff;
    --muted: #b9b6ff;
    --accent: #7c3aed;
    --accent2: #db2777;
    --accent3: #0891b2;
    --neon-purple: #a78bfa;
    --neon-pink: #f472b6;
    --neon-cyan: #22d3ee;
    --neon-green: #34d399;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    -webkit-font-smoothing: antialiased;
    color: var(--text) !important;
}

.stApp {
    background: var(--bg) !important;
    overflow-x: hidden;
}

.block-container {
    max-width: 1400px;
    padding: 0 1.5rem 6rem;
    position: relative;
    z-index: 2;
}

h1, h2, h3, h4, h5, p, label, span, div {
    color: var(--text) !important;
}

.hero-desc, .song-artist, .np-artist, .form-sub, .chart-label, .comment-time, .m-label, .section-tag, .song-num {
    color: var(--muted) !important;
}

.hero-title, .section-title, .song-title, .form-title, .nav-brand, .np-song, .m-val {
    text-shadow: 0 0 18px rgba(167,139,250,0.18);
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at -10% -10%, rgba(124,58,237,0.18) 0%, transparent 55%),
        radial-gradient(ellipse 60% 40% at 110% 100%, rgba(219,39,119,0.14) 0%, transparent 55%),
        radial-gradient(ellipse 50% 50% at 50% 50%, rgba(8,145,178,0.06) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
    animation: auroraShift 12s ease-in-out infinite alternate;
}

@keyframes auroraShift {
    0%   { filter: hue-rotate(0deg) brightness(1); }
    50%  { filter: hue-rotate(20deg) brightness(1.1); }
    100% { filter: hue-rotate(-10deg) brightness(0.95); }
}

.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(124,58,237,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(124,58,237,0.035) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
    animation: gridDrift 20s linear infinite;
}

@keyframes gridDrift {
    0% { transform: translateY(0); }
    100% { transform: translateY(48px); }
}

#MainMenu, footer, header { visibility: hidden; }

.particles {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    overflow: hidden;
}
.particle {
    position: absolute;
    border-radius: 50%;
    animation: particleDrift linear infinite;
    opacity: 0;
    filter: blur(0.5px);
}
@keyframes particleDrift {
    0%   { transform: translateY(110vh) translateX(0) scale(0) rotate(0deg); opacity: 0; }
    8%   { opacity: 1; }
    92%  { opacity: 0.7; }
    100% { transform: translateY(-10vh) translateX(60px) scale(1.3) rotate(180deg); opacity: 0; }
}

.nav-bar {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.7rem 1.1rem;
    margin: 1rem 0 2rem;
    background: rgba(13,13,20,0.9);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 18px;
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    position: sticky;
    top: 10px;
    z-index: 50;
    box-shadow:
        0 0 0 1px rgba(124,58,237,0.1),
        0 20px 60px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(255,255,255,0.05);
    animation: navSlideDown 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes navSlideDown {
    from { transform: translateY(-20px); opacity: 0; }
    to   { transform: translateY(0);     opacity: 1; }
}

.nav-brand {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 0.06em;
    background: linear-gradient(135deg, #a78bfa, #f472b6, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-right: 1.2rem;
    white-space: nowrap;
    animation: brandPulse 3s ease-in-out infinite;
}

@keyframes brandPulse {
    0%, 100% { filter: drop-shadow(0 0 8px rgba(167,139,250,0.4)); }
    50%       { filter: drop-shadow(0 0 16px rgba(244,114,182,0.5)); }
}

.hero-wrap {
    padding: 3rem 0 2rem;
    animation: heroFadeUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s both;
}

@keyframes heroFadeUp {
    from { transform: translateY(40px); opacity: 0; }
    to   { transform: translateY(0);   opacity: 1; }
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(124,58,237,0.1);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 999px;
    padding: 5px 16px;
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    color: var(--neon-purple) !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.4rem;
}

.hero-eyebrow .dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #a78bfa;
    animation: dotPing 1.4s ease infinite;
    box-shadow: 0 0 0 0 rgba(167,139,250,0.5);
}

@keyframes dotPing {
    0%   { box-shadow: 0 0 0 0 rgba(167,139,250,0.7); }
    70%  { box-shadow: 0 0 0 8px rgba(167,139,250,0); }
    100% { box-shadow: 0 0 0 0 rgba(167,139,250,0); }
}

.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4rem, 9vw, 8rem);
    line-height: 0.9;
    letter-spacing: 0.03em;
    margin-bottom: 1.3rem;
}

.hero-title .grad {
    background: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    background-size: 200% 200%;
    animation: gradientFlow 4s ease infinite;
}

@keyframes gradientFlow {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.hero-desc {
    font-size: 1.05rem;
    color: var(--muted) !important;
    max-width: 380px;
    line-height: 1.7;
    margin-bottom: 1.8rem;
    font-weight: 400;
}

.stat-row {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-top: 1.5rem;
}

.stat-chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 0.45rem 0.9rem;
    font-size: 0.78rem;
    font-family: 'DM Mono', monospace;
    color: var(--muted) !important;
    transition: all 0.25s ease;
}

.stat-chip:hover {
    background: rgba(124,58,237,0.1);
    border-color: rgba(124,58,237,0.3);
    transform: translateY(-2px);
    color: var(--neon-purple) !important;
}

.stat-chip b { color: var(--text) !important; }

.glass-card {
    background: rgba(13,13,20,0.75);
    border: 1px solid var(--border2);
    border-radius: 22px;
    padding: 1.6rem;
    backdrop-filter: blur(14px);
    position: relative;
    overflow: hidden;
    transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.glass-card:hover {
    border-color: rgba(124,58,237,0.4);
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0 20px 50px rgba(124,58,237,0.2);
}

.glass-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(124,58,237,0.05) 0%, transparent 60%);
    pointer-events: none;
}

.section-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--accent) !important;
    margin-bottom: 0.35rem;
}

.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 0.04em;
    margin-bottom: 1.5rem;
    color: var(--text) !important;
}

.section-title .grad {
    background: linear-gradient(90deg, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}

.metric-tile {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.5rem 1.3rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    animation: tileReveal 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes tileReveal {
    from { transform: translateY(30px) scale(0.95); opacity: 0; }
    to   { transform: translateY(0) scale(1);       opacity: 1; }
}

.metric-tile:hover {
    border-color: rgba(124,58,237,0.35);
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(124,58,237,0.15);
}

.metric-tile::after {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 80px; height: 80px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(124,58,237,0.2), transparent 70%);
    animation: orbFloat 4s ease-in-out infinite;
}

@keyframes orbFloat {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50%       { transform: translate(-5px, 5px) scale(1.1); }
}

.m-label {
    font-size: 0.7rem;
    font-family: 'DM Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted) !important;
    margin-bottom: 0.6rem;
}

.m-val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.2rem;
    letter-spacing: 0.04em;
    background: linear-gradient(135deg, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}

.now-playing {
    background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(219,39,119,0.08));
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 20px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    position: relative;
    overflow: hidden;
    animation: nowPlayingIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes nowPlayingIn {
    from { transform: translateX(-20px) scale(0.97); opacity: 0; }
    to   { transform: translateX(0) scale(1);        opacity: 1; }
}

.now-playing::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #a78bfa, #f472b6, #22d3ee);
    border-radius: 0 4px 4px 0;
    animation: borderGlow 2s ease-in-out infinite;
}

@keyframes borderGlow {
    0%, 100% { box-shadow: 0 0 8px rgba(167,139,250,0.5); }
    50%       { box-shadow: 0 0 20px rgba(244,114,182,0.7); }
}

.now-playing::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent, rgba(124,58,237,0.05), transparent);
    animation: scanLine 3s linear infinite;
    pointer-events: none;
}

@keyframes scanLine {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.np-disc {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #db2777);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    animation: discSpin 3s linear infinite;
    flex-shrink: 0;
    box-shadow: 0 0 20px rgba(124,58,237,0.4);
}

@keyframes discSpin { to { transform: rotate(360deg); } }

.np-bars {
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 28px;
}

.np-bar {
    width: 4px;
    background: linear-gradient(180deg, #a78bfa, #f472b6);
    border-radius: 4px;
    animation: eqBounce 0.8s ease-in-out infinite;
}

.np-bar:nth-child(1) { animation-delay: 0s; height: 35%; }
.np-bar:nth-child(2) { animation-delay: 0.12s; height: 100%; }
.np-bar:nth-child(3) { animation-delay: 0.24s; height: 55%; }
.np-bar:nth-child(4) { animation-delay: 0.06s; height: 80%; }
.np-bar:nth-child(5) { animation-delay: 0.18s; height: 45%; }
.np-bar:nth-child(6) { animation-delay: 0.30s; height: 70%; }

@keyframes eqBounce {
    0%, 100% { transform: scaleY(1); }
    50%       { transform: scaleY(0.2); }
}

.np-song   { font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; letter-spacing: 0.05em; color: var(--text) !important; }
.np-artist { font-size: 0.8rem; color: var(--muted) !important; font-family: 'DM Mono', monospace; }

.song-card {
    background: linear-gradient(135deg, rgba(8,10,24,0.99), rgba(16,18,38,0.99));
    border: 1.6px solid rgba(88,216,255,0.42);
    border-radius: 24px;
    padding: 1.6rem;
    margin-bottom: 1.7rem;
    position: relative;
    overflow: hidden;
    transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
    animation: cardSlideIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
    box-shadow: 0 0 0 1px rgba(88,216,255,0.16), 0 20px 48px rgba(0,0,0,0.36), inset 0 0 0 1px rgba(255,255,255,0.02);
}

@keyframes cardSlideIn {
    from { transform: translateY(25px) scale(0.98); opacity: 0; }
    to   { transform: translateY(0) scale(1);       opacity: 1; }
}

.song-card:hover {
    border-color: rgba(88,216,255,0.92);
    background: linear-gradient(135deg, rgba(12,14,30,1), rgba(20,22,44,1));
    transform: translateY(-4px);
    box-shadow: 0 24px 58px rgba(0,0,0,0.44), 0 0 0 1px rgba(88,216,255,0.34), 0 0 32px rgba(124,58,237,0.16);
}

.song-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #7c3aed, #db2777, #0891b2);
    opacity: 0.92;
    transition: opacity 0.35s ease;
}

.song-card::after {
    content: '';
    position: absolute;
    left: 1.2rem;
    right: 1.2rem;
    bottom: 0.9rem;
    height: 1px;
    background: linear-gradient(90deg, rgba(124,58,237,0), rgba(88,216,255,0.9), rgba(244,114,182,0.85), rgba(124,58,237,0));
    box-shadow: 0 0 14px rgba(88,216,255,0.22);
    opacity: 0.9;
}

.song-card:hover::before { opacity: 1; }

.song-num   { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #c4b5fd !important; letter-spacing: 0.14em; margin-bottom: 0.4rem; text-transform: uppercase; }
.song-title { font-family: 'Bebas Neue', sans-serif; font-size: 1.9rem; letter-spacing: 0.05em; color: #f7f3ff !important; margin-bottom: 0.24rem; text-shadow: 0 0 18px rgba(167,139,250,0.22); }
.song-artist { font-size: 0.9rem; font-family: 'DM Mono', monospace; color: #67e8f9 !important; margin-bottom: 1rem; }

.pill {
    display: inline-block;
    background: rgba(124,58,237,0.1);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 999px;
    padding: 3px 11px;
    font-size: 0.68rem;
    font-family: 'DM Mono', monospace;
    color: var(--neon-purple) !important;
    margin-right: 0.3rem;
    margin-bottom: 0.3rem;
    transition: all 0.2s ease;
}

.pill:hover { background: rgba(124,58,237,0.2); transform: scale(1.05); }

.pill.cyan  { background: rgba(8,145,178,0.1); border-color: rgba(8,145,178,0.25); color: var(--neon-cyan) !important; }
.pill.pink  { background: rgba(219,39,119,0.1); border-color: rgba(219,39,119,0.25); color: var(--neon-pink) !important; }
.pill.green { background: rgba(52,211,153,0.1); border-color: rgba(52,211,153,0.25); color: var(--neon-green) !important; }

.stTextInput input,
.stNumberInput input,
textarea,
[data-baseweb="input"] input,
[data-baseweb="base-input"] input,
[data-testid="stTextInputRootElement"] input,
[data-testid="stNumberInputRootElement"] input {
    background: linear-gradient(135deg, rgba(8,11,30,0.99), rgba(18,24,52,0.99)) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #22d3ee !important;
    border-radius: 16px !important;
    border: 1.5px solid rgba(88,216,255,0.9) !important;
    box-shadow: 0 0 0 1px rgba(124,58,237,0.34), 0 0 24px rgba(34,211,238,0.16), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
    transition: all 0.25s ease !important;
    text-shadow: 0 0 1px rgba(255,255,255,0.18) !important;
}

.stTextInput input::placeholder,
textarea::placeholder,
[data-baseweb="input"] input::placeholder,
[data-baseweb="base-input"] input::placeholder {
    color: #d9d6ff !important;
    -webkit-text-fill-color: #d9d6ff !important;
    opacity: 0.88 !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
textarea:focus,
[data-baseweb="input"] input:focus,
[data-baseweb="base-input"] input:focus {
    border-color: rgba(244,114,182,0.95) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.22),
                0 0 34px rgba(244,114,182,0.22),
                0 0 18px rgba(34,211,238,0.14) !important;
    background: linear-gradient(135deg, rgba(10,14,34,1), rgba(20,26,58,1)) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

.stTextInput input[type="password"],
[data-baseweb="input"] input[type="password"] {
    background: linear-gradient(135deg, rgba(8,11,30,0.99), rgba(18,24,52,0.99)) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
textarea:-webkit-autofill,
select:-webkit-autofill {
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #22d3ee !important;
    -webkit-box-shadow: 0 0 0px 1000px #111a33 inset, 0 0 0 1.5px rgba(88,216,255,0.9), 0 0 22px rgba(34,211,238,0.12) !important;
    box-shadow: 0 0 0px 1000px #111a33 inset, 0 0 0 1.5px rgba(88,216,255,0.9), 0 0 22px rgba(34,211,238,0.12) !important;
    transition: background-color 9999s ease-in-out 0s !important;
}

.stTextInput label,
.stNumberInput label,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] * {
    color: #ffffff !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
}

div[data-baseweb="select"] > div {
    background: rgba(13,13,20,0.95) !important;
    color: #eeeeff !important;
    border-radius: 12px !important;
    border: 1px solid rgba(124,58,237,0.35) !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] [data-testid="stSelectbox"] span {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    text-shadow: 0 0 12px rgba(167,139,250,0.25) !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"],
ul[data-baseweb="menu"] {
    background: #1a1a2e !important;
    border: 1px solid rgba(124,58,237,0.3) !important;
    border-radius: 12px !important;
}

[data-baseweb="menu"] li,
[data-baseweb="option"],
[role="option"] {
    background: #1a1a2e !important;
    color: #eeeeff !important;
    -webkit-text-fill-color: #eeeeff !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.9rem !important;
}

[data-baseweb="menu"] li:hover,
[data-baseweb="option"]:hover,
[role="option"]:hover {
    background: rgba(124,58,237,0.18) !important;
    color: #a78bfa !important;
    -webkit-text-fill-color: #a78bfa !important;
}

[data-baseweb="menu"] li[aria-selected="true"],
[role="option"][aria-selected="true"] {
    background: rgba(124,58,237,0.25) !important;
    color: #c4b5fd !important;
    -webkit-text-fill-color: #c4b5fd !important;
}

.stButton > button {
    background: linear-gradient(135deg, rgba(124,58,237,0.18), rgba(219,39,119,0.12)) !important;
    color: #eeeeff !important;
    -webkit-text-fill-color: #eeeeff !important;
    border: 1px solid rgba(124,58,237,0.35) !important;
    border-radius: 12px !important;
    padding: 0.5rem 1.15rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 600 !important;
    transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    backdrop-filter: blur(8px) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stFormSubmitButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, rgba(25,18,46,0.98), rgba(59,19,64,0.96)) !important;
    color: #ff4fd8 !important;
    -webkit-text-fill-color: #ff4fd8 !important;
    border: 1px solid rgba(244,114,182,0.82) !important;
    border-radius: 14px !important;
    padding: 0.72rem 1.2rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.03em !important;
    text-transform: none !important;
    box-shadow:
        0 0 0 1px rgba(244,114,182,0.16) inset,
        0 0 12px rgba(244,114,182,0.28),
        0 0 26px rgba(244,114,182,0.12) !important;
    transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    backdrop-filter: blur(10px) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, rgba(66,18,72,0.98), rgba(120,24,86,0.96)) !important;
    border-color: rgba(244,114,182,0.95) !important;
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow:
        0 12px 28px rgba(244,114,182,0.24),
        0 0 24px rgba(244,114,182,0.42),
        0 0 0 1px rgba(244,114,182,0.22) !important;
    color: #ffd4f3 !important;
    -webkit-text-fill-color: #ffd4f3 !important;
}

.stButton > button:active,
.stFormSubmitButton > button:active {
    transform: translateY(-1px) scale(0.99) !important;
}

.stButton > button p,
.stFormSubmitButton > button p,
.stButton > button span,
.stFormSubmitButton > button span,
.stButton > button div,
.stFormSubmitButton > button div {
    color: inherit !important;
    -webkit-text-fill-color: inherit !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

.stButton > button:disabled,
.stFormSubmitButton > button:disabled {
    background: linear-gradient(135deg, rgba(31,22,47,0.95), rgba(54,28,60,0.92)) !important;
    color: #ffd7f4 !important;
    -webkit-text-fill-color: #ffd7f4 !important;
    border-color: rgba(244,114,182,0.55) !important;
    opacity: 1 !important;
}

.fb-success, .fb-warning, .fb-error {
    border-radius: 12px;
    padding: 0.65rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.84rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'DM Mono', monospace;
    animation: feedbackPop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes feedbackPop {
    from { transform: scale(0.9) translateY(5px); opacity: 0; }
    to   { transform: scale(1) translateY(0);     opacity: 1; }
}

.fb-success { background: rgba(34,211,238,0.07); border: 1px solid rgba(34,211,238,0.22); color: #67e8f9 !important; }
.fb-warning { background: rgba(251,191,36,0.07); border: 1px solid rgba(251,191,36,0.22); color: #fde68a !important; }
.fb-error   { background: rgba(239,68,68,0.07);  border: 1px solid rgba(239,68,68,0.22);  color: #fca5a5 !important; }

.bot-wrap {
    background: var(--surface2);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 20px;
    padding: 1.2rem;
    margin-top: 1.2rem;
    position: relative;
    overflow: hidden;
    animation: botReveal 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes botReveal {
    from { transform: translateY(15px) scale(0.97); opacity: 0; }
    to   { transform: translateY(0) scale(1);       opacity: 1; }
}

.bot-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #7c3aed, #db2777, #0891b2);
    animation: topBarGlow 2s ease infinite;
}

@keyframes topBarGlow {
    0%, 100% { opacity: 0.7; }
    50%       { opacity: 1; }
}

.bot-header {
    display: flex; align-items: center; gap: 0.75rem;
    margin-bottom: 1rem; padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--border);
}

.bot-avatar {
    width: 40px; height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, #7c3aed, #db2777);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
    animation: avatarPulse 2s ease-in-out infinite;
    box-shadow: 0 0 15px rgba(124,58,237,0.3);
}

@keyframes avatarPulse {
    0%, 100% { box-shadow: 0 0 10px rgba(124,58,237,0.3); }
    50%       { box-shadow: 0 0 20px rgba(219,39,119,0.4); }
}

.bot-name { font-family: 'Bebas Neue', sans-serif; font-size: 1.1rem; letter-spacing: 0.06em; color: var(--text) !important; }
.bot-sub  { font-size: 0.7rem; font-family: 'DM Mono', monospace; color: var(--muted) !important; }

.bot-msg-ai {
    background: rgba(124,58,237,0.08);
    border: 1px solid rgba(124,58,237,0.15);
    border-radius: 4px 16px 16px 16px;
    padding: 0.65rem 0.9rem;
    color: var(--text) !important;
    font-size: 0.86rem;
    line-height: 1.55;
    max-width: 85%;
    animation: msgIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

.bot-msg-user {
    background: linear-gradient(135deg, rgba(124,58,237,0.22), rgba(219,39,119,0.18));
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 16px 4px 16px 16px;
    padding: 0.65rem 0.9rem;
    color: var(--text) !important;
    font-size: 0.86rem;
    line-height: 1.55;
    max-width: 85%;
    align-self: flex-end;
    animation: msgIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes msgIn {
    from { transform: scale(0.92) translateY(8px); opacity: 0; }
    to   { transform: scale(1) translateY(0);      opacity: 1; }
}

.bot-scroll {
    max-height: 200px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 0.8rem;
    scrollbar-width: thin;
    scrollbar-color: rgba(124,58,237,0.3) transparent;
}

.form-card {
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: 24px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
    animation: formReveal 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.2s both;
}

@keyframes formReveal {
    from { transform: translateY(30px) scale(0.96); opacity: 0; }
    to   { transform: translateY(0) scale(1);       opacity: 1; }
}

.form-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #7c3aed, #db2777, #0891b2);
    animation: formLineGlow 3s ease-in-out infinite;
}

@keyframes formLineGlow {
    0%, 100% { opacity: 0.6; }
    50%       { opacity: 1; }
}

.form-title { font-family: 'Bebas Neue', sans-serif; font-size: 1.8rem; letter-spacing: 0.05em; margin-bottom: 0.2rem; color: var(--text) !important; }
.form-sub   { font-size: 0.78rem; color: var(--muted) !important; font-family: 'DM Mono', monospace; margin-bottom: 1.5rem; }

.star-rating-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 0;
}

.star-icon {
    font-size: 24px;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    display: inline-block;
    filter: drop-shadow(0 0 0px rgba(167,139,250,0));
}

.star-icon.active {
    filter: drop-shadow(0 0 6px rgba(167,139,250,0.7));
    animation: starPop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes starPop {
    0%   { transform: scale(0.5) rotate(-10deg); }
    60%  { transform: scale(1.3) rotate(5deg); }
    100% { transform: scale(1) rotate(0deg); }
}

.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,58,237,0.4), rgba(219,39,119,0.3), transparent);
    margin: 2rem 0;
    border: none;
    animation: dividerPulse 3s ease-in-out infinite;
}

@keyframes dividerPulse {
    0%, 100% { opacity: 0.5; }
    50%       { opacity: 1; }
}

[data-testid="stDataFrame"] {
    background: var(--surface) !important;
    border-radius: 16px !important;
    border: 1px solid var(--border2) !important;
    overflow: hidden;
}

[data-testid="stExpander"] {
    background: var(--surface) !important;
    border-radius: 16px !important;
    border: 1px solid var(--border2) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stExpander"]:hover {
    border-color: rgba(124,58,237,0.3) !important;
}

.rating-change-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(52,211,153,0.1);
    border: 1px solid rgba(52,211,153,0.3);
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 0.7rem;
    font-family: 'DM Mono', monospace;
    color: var(--neon-green) !important;
    animation: badgePop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes badgePop {
    from { transform: scale(0.7); opacity: 0; }
    to   { transform: scale(1); opacity: 1; }
}


/* ── ANIMATED STAR RATING ── */
@keyframes starSelect {
    0%   { transform: scale(0.6) rotate(-15deg); filter: drop-shadow(0 0 0 transparent); }
    40%  { transform: scale(1.45) rotate(8deg);  filter: drop-shadow(0 0 10px rgba(167,139,250,0.9)); }
    65%  { transform: scale(0.9) rotate(-3deg); }
    100% { transform: scale(1) rotate(0deg);      filter: drop-shadow(0 0 6px rgba(167,139,250,0.55)); }
}
@keyframes starPulse {
    0%, 100% { filter: drop-shadow(0 0 4px rgba(167,139,250,0.4)); }
    50%       { filter: drop-shadow(0 0 12px rgba(244,114,182,0.7)); }
}
@keyframes starIdle {
    0%, 100% { opacity: 0.25; transform: scale(1); }
    50%       { opacity: 0.38; transform: scale(1.05); }
}
.star-active {
    display: inline-block;
    animation: starSelect 0.45s cubic-bezier(0.34,1.56,0.64,1) both, starPulse 2.5s ease-in-out 0.45s infinite;
    cursor: pointer;
    transition: color 0.2s ease;
}
.star-idle {
    display: inline-block;
    animation: starIdle 2s ease-in-out infinite;
    cursor: pointer;
    transition: all 0.2s ease;
}
.star-idle:hover {
    animation: none;
    transform: scale(1.3);
    opacity: 1;
    filter: drop-shadow(0 0 6px rgba(167,139,250,0.6));
}


/* ── ANIMATED STAR RATING ── */
@keyframes starSelect {
    0%   { transform: scale(0.6) rotate(-15deg); filter: drop-shadow(0 0 0 transparent); }
    40%  { transform: scale(1.45) rotate(8deg);  filter: drop-shadow(0 0 10px rgba(167,139,250,0.9)); }
    65%  { transform: scale(0.9) rotate(-3deg); }
    100% { transform: scale(1) rotate(0deg);      filter: drop-shadow(0 0 6px rgba(167,139,250,0.55)); }
}
@keyframes starPulse {
    0%, 100% { filter: drop-shadow(0 0 4px rgba(167,139,250,0.4)); }
    50%       { filter: drop-shadow(0 0 12px rgba(244,114,182,0.7)); }
}
@keyframes starIdle {
    0%, 100% { opacity: 0.25; transform: scale(1); }
    50%       { opacity: 0.38; transform: scale(1.05); }
}
.star-active {
    display: inline-block;
    animation: starSelect 0.45s cubic-bezier(0.34,1.56,0.64,1) both, starPulse 2.5s ease-in-out 0.45s infinite;
    cursor: pointer;
    transition: color 0.2s ease;
}
.star-idle {
    display: inline-block;
    animation: starIdle 2s ease-in-out infinite;
    cursor: pointer;
    transition: all 0.2s ease;
}
.star-idle:hover {
    animation: none;
    transform: scale(1.3);
    opacity: 1;
    filter: drop-shadow(0 0 6px rgba(167,139,250,0.6));
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.35); border-radius: 4px; }

/* FORCE VISIBILITY FOR ALL SUBMIT / PRIMARY BUTTONS */
.stForm [data-testid="stFormSubmitButton"] button,
.stFormSubmitButton button,
button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, rgba(25,18,46,0.98), rgba(59,19,64,0.96)) !important;
    color: #ff4fd8 !important;
    -webkit-text-fill-color: #ff4fd8 !important;
    border: 1px solid rgba(244,114,182,0.82) !important;
    text-shadow: 0 0 10px rgba(244,114,182,0.25) !important;
    font-weight: 800 !important;
}

.stForm [data-testid="stFormSubmitButton"] button:hover,
.stFormSubmitButton button:hover,
button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(135deg, rgba(66,18,72,0.98), rgba(120,24,86,0.96)) !important;
    color: #ffd4f3 !important;
    -webkit-text-fill-color: #ffd4f3 !important;
}

.playlist-admin-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: all 0.3s ease;
    animation: cardSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

.playlist-admin-card:hover {
    border-color: rgba(124,58,237,0.3);
    background: var(--surface3);
}

.delete-btn > button {
    background: rgba(239,68,68,0.1) !important;
    border-color: rgba(239,68,68,0.3) !important;
    color: #fca5a5 !important;
    -webkit-text-fill-color: #fca5a5 !important;
}

.delete-btn > button:hover {
    background: rgba(239,68,68,0.25) !important;
    border-color: rgba(239,68,68,0.6) !important;
    box-shadow: 0 10px 25px rgba(239,68,68,0.2) !important;
    color: #fff !important;
    -webkit-text-fill-color: #fff !important;
}

.rec-card {
    background: linear-gradient(135deg, rgba(13,13,20,0.9), rgba(26,26,40,0.9));
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 20px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
    animation: cardSlideIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

.rec-card:hover {
    border-color: rgba(124,58,237,0.5);
    transform: translateY(-3px);
    box-shadow: 0 16px 40px rgba(124,58,237,0.18);
}

.rec-score-bar {
    height: 4px;
    border-radius: 4px;
    background: linear-gradient(90deg, #7c3aed, #db2777, #22d3ee);
    margin-top: 0.8rem;
    transition: width 1s ease;
}

.stNumberInput input {
    background: #ffffff !important;
    color: #111111 !important;
    -webkit-text-fill-color: #111111 !important;
}

.stSlider label, .stSlider p {
    color: var(--text) !important;
}

.pl-track-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(135deg, rgba(13,13,20,0.96), rgba(24,24,38,0.96));
    border: 1px solid rgba(167,139,250,0.22);
    border-radius: 14px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    transition: all 0.25s ease;
    animation: cardSlideIn 0.35s cubic-bezier(0.34,1.56,0.64,1) both;
}
.pl-track-row:hover {
    border-color: rgba(167,139,250,0.50);
    background: linear-gradient(135deg, rgba(18,18,30,1), rgba(30,20,48,1));
    box-shadow: 0 14px 30px rgba(124,58,237,0.16);
}
.pl-track-info { flex: 1; }
.pl-track-title { font-family: 'Bebas Neue',sans-serif; font-size:1.08rem; letter-spacing:.04em; color:#f8f5ff !important; text-shadow:0 0 10px rgba(167,139,250,0.15); }
.pl-track-artist { font-size:.74rem; color:#b7addc !important; font-family:'DM Mono',monospace; }

.add-song-card {
    background: linear-gradient(135deg, rgba(13,13,20,0.95), rgba(19,19,30,0.95));
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    animation: formReveal 0.6s cubic-bezier(0.34,1.56,0.64,1) both;
}
.add-song-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #34d399, #0891b2, #7c3aed);
    animation: formLineGlow 3s ease-in-out infinite;
}
.add-song-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.05em;
    color: var(--neon-green) !important;
    margin-bottom: 0.2rem;
}
.add-song-sub {
    font-size: 0.74rem;
    color: var(--muted) !important;
    font-family: 'DM Mono', monospace;
    margin-bottom: 1.5rem;
}

.chart-wrap {
    background: var(--surface2);
    border: 1px solid var(--border2);
    border-radius: 20px;
    padding: 1.4rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.2rem;
    animation: tileReveal 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
}
.chart-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #7c3aed, #db2777, #22d3ee);
    opacity: 0.7;
}
.chart-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted) !important;
    margin-bottom: 0.4rem;
}
.chart-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 0.04em;
    color: var(--text) !important;
    margin-bottom: 1rem;
}

/* ── MOOD CARD ── */
.mood-card {
    border-radius: 22px;
    padding: 1.6rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    animation: tileReveal 0.6s cubic-bezier(0.34,1.56,0.64,1) both;
}
.mood-emoji { font-size: 3.5rem; line-height: 1; margin-bottom: .5rem; display: block; }
.mood-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    letter-spacing: .06em;
    line-height: 1;
    margin-bottom: .3rem;
}
.mood-desc {
    font-size: .8rem;
    font-family: 'DM Mono', monospace;
    color: var(--muted) !important;
    margin-bottom: 1rem;
}
.mood-feat-row { display: flex; gap: .7rem; flex-wrap: wrap; }
.mood-feat {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 4px 12px;
    font-size: .68rem;
    font-family: 'DM Mono', monospace;
    color: var(--muted) !important;
}
.mood-feat b { color: var(--text) !important; }

/* ── COMMENT SECTION ── */
.comment-section {
    background: rgba(13,13,20,0.8);
    border: 1px solid rgba(124,58,237,0.18);
    border-radius: 18px;
    padding: 1.2rem 1.4rem;
    margin-top: 1rem;
    animation: botReveal 0.4s cubic-bezier(0.34,1.56,0.64,1) both;
}
.comment-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: .06em;
    color: var(--neon-cyan) !important;
    margin-bottom: .8rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}
.comment-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: .6rem .9rem;
    margin-bottom: .5rem;
    transition: all .2s ease;
}
.comment-item:hover {
    border-color: rgba(124,58,237,0.2);
    background: rgba(124,58,237,0.04);
}
.comment-user {
    font-family: 'DM Mono', monospace;
    font-size: .68rem;
    color: var(--neon-purple) !important;
    margin-bottom: .25rem;
}
.comment-text {
    font-size: .84rem;
    color: var(--text) !important;
    line-height: 1.5;
}
.comment-time {
    font-size: .62rem;
    color: var(--muted) !important;
    font-family: 'DM Mono', monospace;
    margin-top: .2rem;
}
.comment-empty {
    font-size: .78rem;
    color: var(--muted) !important;
    font-family: 'DM Mono', monospace;
    padding: .5rem 0;
    text-align: center;
}


.discover-toolbar {
    background: linear-gradient(135deg, rgba(11,13,30,0.94), rgba(18,20,40,0.94));
    border: 1px solid rgba(124,58,237,0.34);
    border-radius: 22px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04), 0 12px 32px rgba(0,0,0,0.24);
}
.discover-count {
    color: #d9d6ff !important;
    font-size: 0.78rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.08em;
    margin-bottom: 1.4rem;
    text-transform: uppercase;
}
.discover-card-grid-note {
    color: var(--neon-cyan) !important;
    font-size: 0.74rem;
    font-family: 'DM Mono', monospace;
    margin-top: -0.2rem;
    margin-bottom: 1rem;
}


.video-modal-shell {
    position: relative;
    z-index: 40;
    margin: 0 0 1.2rem 0;
}
.video-modal-backdrop {
    position: absolute;
    inset: 0;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(8,8,14,0.88), rgba(18,9,35,0.92));
    border: 1px solid rgba(167,139,250,0.18);
    box-shadow: 0 24px 70px rgba(0,0,0,0.45);
    backdrop-filter: blur(16px);
}
.video-modal-card {
    position: relative;
    z-index: 2;
    padding: 1.05rem 1.2rem 0.6rem;
}
.video-modal-header {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:1rem;
}
.video-modal-kicker {
    font-family:'DM Mono', monospace;
    font-size:0.68rem;
    letter-spacing:0.14em;
    text-transform:uppercase;
    color: var(--neon-cyan) !important;
    margin-bottom:0.25rem;
}
.video-modal-title {
    font-family:'Bebas Neue', sans-serif;
    font-size:1.7rem;
    letter-spacing:0.05em;
    color: #f5f1ff !important;
}
div[data-testid="stFormSubmitButton"] > button {
    color: #ff4dd2 !important;
    -webkit-text-fill-color: #ff4dd2 !important;
    font-weight: 900 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    border: 1px solid rgba(244,114,182,0.68) !important;
    box-shadow: 0 0 16px rgba(244,114,182,0.30), inset 0 0 0 1px rgba(255,255,255,0.04) !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    color: #ff7adb !important;
    -webkit-text-fill-color: #ff7adb !important;
    background: linear-gradient(135deg, rgba(244,114,182,0.22), rgba(124,58,237,0.18)) !important;
    box-shadow: 0 0 22px rgba(244,114,182,0.55), 0 14px 28px rgba(244,114,182,0.18) !important;
}
.stButton > button {
    background-size: 200% 200% !important;
}
.stButton > button:hover {
    animation: playlistHoverGlow 1.6s ease infinite !important;
}
@keyframes playlistHoverGlow {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@media (max-width: 900px) {
    .metric-grid { grid-template-columns: 1fr 1fr; }
    .hero-title { font-size: 3.5rem; }
}


[data-testid="stExpander"] details summary,
[data-testid="stExpander"] details summary *,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #f4f1ff !important;
    -webkit-text-fill-color: #f4f1ff !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

[data-testid="stExpander"] details summary:hover,
[data-testid="stExpander"] details summary:hover *,
[data-testid="stExpander"] summary:hover,
[data-testid="stExpander"] summary:hover * {
    color: #c4b5fd !important;
    -webkit-text-fill-color: #c4b5fd !important;
}

[data-testid="stExpander"] pre,
[data-testid="stExpander"] pre *,
[data-testid="stExpander"] code,
[data-testid="stExpander"] code *,
.stCodeBlock pre,
.stCodeBlock pre *,
.stCodeBlock code,
.stCodeBlock code * {
    background: #0b0f1a !important;
    color: #e2e8f0 !important;
    -webkit-text-fill-color: #e2e8f0 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# PARTICLES
# =========================================================
st.markdown("""
<div class="particles">
    <div class="particle" style="left:4%;width:5px;height:5px;background:#7c3aed;animation-duration:13s;animation-delay:0s;"></div>
    <div class="particle" style="left:12%;width:3px;height:3px;background:#db2777;animation-duration:17s;animation-delay:2s;"></div>
    <div class="particle" style="left:22%;width:6px;height:6px;background:#0891b2;animation-duration:15s;animation-delay:4s;"></div>
    <div class="particle" style="left:35%;width:3px;height:3px;background:#7c3aed;animation-duration:19s;animation-delay:1s;"></div>
    <div class="particle" style="left:48%;width:5px;height:5px;background:#db2777;animation-duration:14s;animation-delay:5.5s;"></div>
    <div class="particle" style="left:60%;width:3px;height:3px;background:#0891b2;animation-duration:18s;animation-delay:3s;"></div>
    <div class="particle" style="left:73%;width:5px;height:5px;background:#7c3aed;animation-duration:16s;animation-delay:6s;"></div>
    <div class="particle" style="left:84%;width:3px;height:3px;background:#db2777;animation-duration:12s;animation-delay:2.5s;"></div>
    <div class="particle" style="left:93%;width:4px;height:4px;background:#0891b2;animation-duration:20s;animation-delay:7s;"></div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# DATABASE
# =========================================================
DB_CONFIG = {
    "host": st.secrets["mysql"]["host"],
    "port": st.secrets["mysql"]["port"],
    "user": st.secrets["mysql"]["user"],
    "password": st.secrets["mysql"]["password"],
    "database": st.secrets["mysql"]["database"],
}

def get_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        ssl_disabled=False
    )

def fetch_df(query, params=None):
    conn = get_connection()
    try:
        return pd.read_sql(query, conn, params=params)
    finally:
        conn.close()

def execute_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()

def scalar(query, params=None, default=0):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        row = cursor.fetchone()
        return row[0] if row else default
    finally:
        cursor.close()
        conn.close()

def render_sql_block(query_text):
    escaped_query = html.escape(str(query_text).strip())
    st.markdown(f"""
    <div style="background:#0b0f1a;color:#e2e8f0;padding:14px 16px;border-radius:14px;
                border:1px solid rgba(124,58,237,0.32);font-family:'DM Mono', monospace;
                font-size:0.84rem;overflow-x:auto;white-space:pre-wrap;line-height:1.65;">
        <pre style="margin:0;background:transparent;color:#e2e8f0;white-space:pre-wrap;">{escaped_query}</pre>
    </div>
    """, unsafe_allow_html=True)


def youtube_embed_url(url):
    if not url:
        return None
    raw = str(url).strip()
    if not raw:
        return None
    if "youtube.com/embed/" in raw:
        return raw if "autoplay=" in raw else (raw + ("&" if "?" in raw else "?") + "autoplay=1&mute=1&rel=0")

    video_id = None
    try:
        parsed = urlparse(raw)
        host = (parsed.netloc or "").lower()
        if "youtu.be" in host:
            video_id = parsed.path.strip("/")
        elif "youtube.com" in host:
            if parsed.path == "/watch":
                video_id = parse_qs(parsed.query).get("v", [None])[0]
            elif parsed.path.startswith("/shorts/"):
                video_id = parsed.path.split("/shorts/", 1)[1].split("/", 1)[0]
            elif parsed.path.startswith("/embed/"):
                video_id = parsed.path.split("/embed/", 1)[1].split("/", 1)[0]
    except Exception:
        pass

    if not video_id:
        match = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{6,})", raw)
        if match:
            video_id = match.group(1)

    if not video_id:
        return raw

    return f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&rel=0"


def open_video_modal(track_id, title, artist, url):
    st.session_state.video_open_track_id = track_id
    st.session_state.video_modal_title = f"{title} — {artist}"
    st.session_state.video_modal_url = youtube_embed_url(url) if url else None


def close_video_modal():
    st.session_state.video_open_track_id = None
    st.session_state.video_modal_title = None
    st.session_state.video_modal_url = None


def render_video_modal():
    modal_url = st.session_state.get("video_modal_url")
    if not modal_url:
        return

    modal_title = html.escape(st.session_state.get("video_modal_title") or "Now watching")
    st.markdown(f"""
    <div class='video-modal-shell'>
        <div class='video-modal-backdrop'></div>
        <div class='video-modal-card'>
            <div class='video-modal-header'>
                <div>
                    <div class='video-modal-kicker'>preview mode</div>
                    <div class='video-modal-title'>{modal_title}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    close_col = st.columns([6, 1])[1]
    with close_col:
        if st.button("✕ close preview", key="close_video_modal_btn"):
            close_video_modal()
            st.rerun()
    components.html(
        f"""
        <div style='position:relative;z-index:60;margin-top:-0.75rem;'>
            <div style='width:100%;max-width:980px;margin:0 auto;border-radius:24px;overflow:hidden;border:1px solid rgba(34,211,238,0.28);box-shadow:0 30px 90px rgba(0,0,0,0.55),0 0 0 1px rgba(244,114,182,0.12) inset;'>
                <iframe
                    width='100%'
                    height='560'
                    src='{modal_url}'
                    title='{modal_title}'
                    frameborder='0'
                    allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'
                    allowfullscreen
                    referrerpolicy='strict-origin-when-cross-origin'>
                </iframe>
            </div>
        </div>
        """,
        height=590,
    )


# =========================================================
# SESSION
# =========================================================
def init_session():
    defaults = {
        "page": "Welcome",
        "logged_in": False,
        "user_id": None,
        "username": None,
        "email": None,
        "admin_logged_in": False,
        "admin_id": None,
        "admin_username": None,
        "current_song_title": None,
        "current_song_artist": None,
        "current_song_genre": None,
        "current_song_link": None,
        "active_bot_track_id": None,
        "bot_messages": {},
        "bot_input_counter": 0,
        "star_selections": {},
        "star_saved": {},
        "pending_burst": None,
        "burst_val": 0,
        "playlist_feedback": {},
        "rating_edit_mode": {},
        "show_toast": None,
        "show_mascot_for": None,
        "video_open_track_id": None,
        "video_modal_url": None,
        "video_modal_title": None,
        "show_caterpillar_for": None,
        "comment_open_track_id": None,
        "show_query_results": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

def go_to(page):
    st.session_state.page = page

def logout_user():
    reset_keys = [
        "logged_in","user_id","username","email","current_song_title",
        "current_song_artist","current_song_genre","current_song_link",
        "active_bot_track_id","bot_messages","bot_input_counter",
        "star_selections","star_saved","pending_burst","burst_val",
        "playlist_feedback","rating_edit_mode","show_toast","show_mascot_for",
        "video_open_track_id","video_modal_url","video_modal_title","show_caterpillar_for","comment_open_track_id",
    ]
    for key in reset_keys:
        if key in ("bot_messages","star_selections","star_saved","playlist_feedback","rating_edit_mode"):
            st.session_state[key] = {}
        elif key == "logged_in":
            st.session_state[key] = False
        elif key in ("bot_input_counter","burst_val"):
            st.session_state[key] = 0
        else:
            st.session_state[key] = None
    st.session_state.page = "Welcome"

def logout_admin():
    st.session_state.admin_logged_in = False
    st.session_state.admin_id = None
    st.session_state.admin_username = None
    st.session_state.page = "Welcome"

def require_user():
    if not st.session_state.logged_in:
        st.warning("Please log in first.")
        return False
    return True

def require_admin():
    if not st.session_state.admin_logged_in:
        st.warning("Please log in as admin first.")
        return False
    return True

# =========================================================
# AUTH
# =========================================================
def create_or_get_user(username, email):
    existing = fetch_df("SELECT user_id, username, email FROM user WHERE email = %s",(email,))
    if not existing.empty:
        row = existing.iloc[0]
        return int(row["user_id"]), row["username"], row["email"], "existing"
    new_id = execute_query("INSERT INTO user (username, email) VALUES (%s, %s)",(username, email))
    return int(new_id), username, email, "created"

def admin_login(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT admin_id, username, email, password_hash FROM admin WHERE email = %s",(email,))
        row = cursor.fetchone()
        if row and check_password_hash(row[3], password):
            return {"success": True, "admin_id": row[0], "username": row[1], "email": row[2]}
        return {"success": False, "message": "Invalid admin credentials."}
    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        cursor.close()
        conn.close()

# =========================================================
# DATA LOADERS
# =========================================================
def load_tracks_with_features():
    return fetch_df("""
        SELECT t.track_id, t.title, a.artist_name,
            COALESCE(GROUP_CONCAT(DISTINCT g.genre_name SEPARATOR ', '), 'Unknown') AS genre_name,
            t.year, t.popularity,
            tm.youtube_link AS Youtube_Link,
            af.energy, af.danceability, af.valence, af.acousticness
        FROM track t
        JOIN artist a ON t.artist_id = a.artist_id
	LEFT JOIN track_media tm ON tm.track_id = t.track_id
        LEFT JOIN track_genre tg ON t.track_id = tg.track_id
        LEFT JOIN genre g ON tg.genre_id = g.genre_id
        LEFT JOIN audio_features af ON t.track_id = af.track_id
        GROUP BY t.track_id, t.title, a.artist_name, t.year, t.popularity, tm.youtube_link,
            af.energy, af.danceability, af.valence, af.acousticness
        ORDER BY t.title
    """)

def load_tracks():
    return fetch_df("""
        SELECT
            t.track_id,
            t.title,
            a.artist_name,
            COALESCE(GROUP_CONCAT(DISTINCT g.genre_name SEPARATOR ', '), 'Unknown') AS genre_name,
            t.year,
            t.popularity,
            tm.youtube_link AS Youtube_Link
        FROM track t
        JOIN artist a
            ON t.artist_id = a.artist_id
        LEFT JOIN track_genre tg
            ON t.track_id = tg.track_id
        LEFT JOIN genre g
            ON tg.genre_id = g.genre_id
        LEFT JOIN track_media tm
            ON t.track_id = tm.track_id
        GROUP BY
            t.track_id,
            t.title,
            a.artist_name,
            t.year,
            t.popularity,
            tm.youtube_link
        ORDER BY t.title;
    """)


def load_user_playlists(user_id):
    return fetch_df(
        "SELECT playlist_id, playlist_name, created_at FROM playlist WHERE user_id=%s ORDER BY created_at DESC",
        (user_id,))

def load_all_playlists():
    return fetch_df("""
        SELECT p.playlist_id, p.playlist_name, u.username, u.email, p.created_at,
               COUNT(pt.track_id) AS track_count
        FROM playlist p
        JOIN user u ON p.user_id = u.user_id
        LEFT JOIN playlist_track pt ON p.playlist_id = pt.playlist_id
        GROUP BY p.playlist_id, p.playlist_name, u.username, u.email, p.created_at
        ORDER BY p.created_at DESC
    """)

def create_playlist(user_id, name):
    try:
        execute_query("INSERT INTO playlist (user_id, playlist_name) VALUES (%s, %s)",(user_id, name))
        return True, "Playlist created."
    except Exception as e:
        return False, str(e)

def delete_playlist(playlist_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM playlist_track WHERE playlist_id = %s", (playlist_id,))
        cursor.execute("DELETE FROM playlist WHERE playlist_id = %s", (playlist_id,))
        conn.commit()
        return True, "Playlist deleted."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def add_song_to_playlist(playlist_id, track_id):
    try:
        if scalar("SELECT COUNT(*) FROM playlist_track WHERE playlist_id=%s AND track_id=%s",(playlist_id, track_id)):
            return False, "warning", "Already in this playlist."
        execute_query("INSERT INTO playlist_track (playlist_id, track_id) VALUES (%s, %s)",(playlist_id, track_id))
        return True, "success", "Added to playlist ✓"
    except Exception as e:
        return False, "error", str(e)

def remove_song_from_playlist(playlist_id, track_id):
    try:
        execute_query(
            "DELETE FROM playlist_track WHERE playlist_id=%s AND track_id=%s",
            (playlist_id, track_id)
        )
        return True, "Track removed from playlist."
    except Exception as e:
        return False, str(e)

def load_playlist_tracks(playlist_id):
    return fetch_df("""
        SELECT pt.track_id, t.title, a.artist_name, pt.added_at
        FROM playlist_track pt
        JOIN track t ON pt.track_id = t.track_id
        JOIN artist a ON t.artist_id = a.artist_id
        WHERE pt.playlist_id = %s ORDER BY pt.added_at DESC
    """, (playlist_id,))

def play_song(user_id, track_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user_listening_history (user_id, track_id) VALUES (%s, %s)",(user_id, track_id))
        cursor.execute("""
            INSERT INTO user_listening_summary (user_id, track_id, play_count, last_listened)
            VALUES (%s, %s, 1, CURRENT_TIMESTAMP)
            ON DUPLICATE KEY UPDATE play_count = play_count + 1, last_listened = CURRENT_TIMESTAMP
        """, (user_id, track_id))
        conn.commit()
        return True, "Playing."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def rate_song(user_id, track_id, rating):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO user_rating (user_id, track_id, rating, rated_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            ON DUPLICATE KEY UPDATE rating = VALUES(rating), rated_at = CURRENT_TIMESTAMP
        """, (user_id, track_id, rating))
        conn.commit()
        return True, "Rating saved."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def get_existing_rating(user_id, track_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT rating FROM user_rating WHERE user_id=%s AND track_id=%s",
            (user_id, track_id)
        )
        row = cursor.fetchone()
        return int(row[0]) if row else None
    finally:
        cursor.close()
        conn.close()

def load_user_summary(user_id):
    return fetch_df("""
        SELECT s.track_id, t.title, a.artist_name, s.play_count, s.last_listened
        FROM user_listening_summary s
        JOIN track t ON s.track_id = t.track_id
        JOIN artist a ON t.artist_id = a.artist_id
        WHERE s.user_id = %s ORDER BY s.play_count DESC, s.last_listened DESC
    """, (user_id,))

def load_user_history(user_id):
    return fetch_df("""
        SELECT h.history_id, t.title, a.artist_name, h.listen_time
        FROM user_listening_history h
        JOIN track t ON h.track_id = t.track_id
        JOIN artist a ON t.artist_id = a.artist_id
        WHERE h.user_id = %s ORDER BY h.listen_time DESC
    """, (user_id,))

def load_user_ratings(user_id):
    return fetch_df("""
        SELECT r.track_id, t.title, a.artist_name, r.rating, r.rated_at
        FROM user_rating r
        JOIN track t ON r.track_id = t.track_id
        JOIN artist a ON t.artist_id = a.artist_id
        WHERE r.user_id = %s ORDER BY r.rated_at DESC
    """, (user_id,))

def load_all_users():
    return fetch_df("SELECT user_id, username, email, created_at FROM user ORDER BY user_id")

# =========================================================
# MOOD DETECTION
# =========================================================
def get_user_mood_profile(user_id):
    return fetch_df("""
        SELECT
            AVG(af.energy)       AS avg_energy,
            AVG(af.valence)      AS avg_valence,
            AVG(af.danceability) AS avg_dance,
            COUNT(*)             AS track_count
        FROM user_listening_summary uls
        JOIN audio_features af ON uls.track_id = af.track_id
        WHERE uls.user_id = %s
    """, (user_id,))

def classify_mood(avg_energy, avg_valence, avg_dance):
    e = float(avg_energy) if avg_energy else 50
    v = float(avg_valence) if avg_valence else 50
    d = float(avg_dance) if avg_dance else 50
    if v < 35 and e < 45:
        return ("Melancholic", "😢", "low energy, low mood — deep in the feels", "#6366f1", "#1e1b4b")
    elif v < 42 and e < 60:
        return ("Sad", "😔", "you've been listening to sad songs lately", "#8b5cf6", "#1e1233")
    elif v >= 65 and e >= 65 and d >= 60:
        return ("Euphoric", "🤩", "pure hype energy — no cap you're thriving", "#f59e0b", "#2d1a00")
    elif v >= 60 and e >= 55:
        return ("Happy", "😄", "good vibes only — happiness is the main theme", "#34d399", "#022c22")
    elif e >= 70 and d >= 65:
        return ("Energetic", "⚡", "high energy music — fully locked in mode", "#f472b6", "#2d0a1e")
    elif e < 50 and d < 50 and v >= 45:
        return ("Chill", "😌", "relaxed and laid back — chill era activated", "#22d3ee", "#082030")
    elif e >= 50 and v >= 45 and d >= 50:
        return ("Vibey", "🎶", "balanced vibes — steady and smooth", "#a78bfa", "#1a0a3d")
    else:
        return ("Neutral", "😐", "mixed listening habits — eclectic taste", "#9ca3af", "#111827")

# =========================================================
# SOCIAL COMMENTS
# =========================================================
def ensure_comments_table():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS track_comment (
                comment_id   INT AUTO_INCREMENT PRIMARY KEY,
                track_id     INT NOT NULL,
                user_id      INT NOT NULL,
                username     VARCHAR(100) NOT NULL,
                comment_text TEXT NOT NULL,
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_track (track_id),
                INDEX idx_user (user_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        conn.commit()
    except Exception:
        pass
    finally:
        cursor.close()
        conn.close()

def post_comment(track_id, user_id, username, text):
    try:
        ensure_comments_table()
        execute_query(
            "INSERT INTO track_comment (track_id, user_id, username, comment_text) VALUES (%s,%s,%s,%s)",
            (track_id, user_id, username, text.strip())
        )
        return True, "Comment posted!"
    except Exception as e:
        return False, str(e)

def load_comments(track_id):
    try:
        ensure_comments_table()
        return fetch_df(
            "SELECT comment_id, username, comment_text, created_at FROM track_comment WHERE track_id=%s ORDER BY created_at DESC LIMIT 50",
            (track_id,)
        )
    except Exception:
        return pd.DataFrame()

def get_comment_count(track_id):
    try:
        ensure_comments_table()
        return scalar("SELECT COUNT(*) FROM track_comment WHERE track_id=%s", (track_id,))
    except Exception:
        return 0

# =========================================================
# TRACK MANAGEMENT
# =========================================================
def update_track_features(track_id, energy, danceability, valence, acousticness):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM audio_features WHERE track_id = %s", (track_id,))
        exists = cursor.fetchone()[0]
        if exists:
            cursor.execute("""
                UPDATE audio_features
                SET energy=%s, danceability=%s, valence=%s, acousticness=%s
                WHERE track_id=%s
            """, (energy, danceability, valence, acousticness, track_id))
        else:
            cursor.execute("""
                INSERT INTO audio_features (track_id, energy, danceability, valence, acousticness)
                VALUES (%s, %s, %s, %s, %s)
            """, (track_id, energy, danceability, valence, acousticness))
        conn.commit()
        return True, "Audio features updated successfully."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def update_track_info(track_id, title, year, popularity, youtube_link):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE track
            SET title=%s, year=%s, popularity=%s
            WHERE track_id=%s
        """, (title, year, popularity, track_id))

        clean_link = (youtube_link or '').strip()
        if clean_link:
            cursor.execute("""
                INSERT INTO track (track_id,Title,Artist_ID,Year,Popularity youtube_link)
                VALUES (%s, %s, %s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE youtube_link = VALUES(youtube_link)
            """, (track_id, clean_link))
        else:
            cursor.execute("DELETE FROM track WHERE track_id = %s", (track_id,))

        conn.commit()
        return True, "Track info updated."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def delete_track(track_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for tbl in ["user_listening_history", "user_listening_summary", "user_rating",
                    "playlist_track", "track_genre", "audio_features", "recommendation", "track"]:
            cursor.execute(f"DELETE FROM {tbl} WHERE track_id = %s", (track_id,))
        cursor.execute("DELETE FROM track WHERE track_id = %s", (track_id,))
        conn.commit()
        return True, "Track deleted successfully."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def get_or_create_artist(artist_name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT artist_id FROM artist WHERE artist_name = %s", (artist_name,))
        row = cursor.fetchone()
        if row:
            return row[0]
        cursor.execute("INSERT INTO artist (artist_name) VALUES (%s)", (artist_name,))
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()

def load_all_genres():
    return fetch_df("SELECT genre_id, genre_name FROM genre ORDER BY genre_name")

def add_new_song(title, artist_name, genre_names, year, popularity, youtube_link,
                 energy, danceability, valence, acousticness):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        artist_id = get_or_create_artist(artist_name.strip())
        cursor.execute("""
            INSERT INTO track (title, artist_id, year, popularity)
            VALUES (%s, %s, %s, %s)
        """, (title.strip(), artist_id, year or None, popularity))
        track_id = cursor.lastrowid

        clean_link = (youtube_link or '').strip()
        if clean_link:
            cursor.execute(
                "INSERT INTO track (Track_ID,Artist_ID,Year,Popularity,Title, youtube_link) VALUES (%s, %s,%s,%s,%s,%s)",
                (track_id, clean_link)
            )

        for gname in genre_names:
            gname = gname.strip()
            if gname:
                cursor.execute("SELECT genre_id FROM genre WHERE genre_name = %s", (gname,))
                row = cursor.fetchone()
                if row:
                    genre_id = row[0]
                else:
                    cursor.execute("INSERT INTO genre (genre_name) VALUES (%s)", (gname,))
                    genre_id = cursor.lastrowid
                cursor.execute(
                    "INSERT IGNORE INTO track_genre (track_id, genre_id) VALUES (%s, %s)",
                    (track_id, genre_id)
                )
        cursor.execute("""
            INSERT INTO audio_features (track_id, energy, danceability, valence, acousticness)
            VALUES (%s, %s, %s, %s, %s)
        """, (track_id, energy, danceability, valence, acousticness))
        conn.commit()
        return True, f"Song '{title}' added successfully! (track_id: {track_id})", track_id
    except Exception as e:
        conn.rollback()
        return False, str(e), None
    finally:
        cursor.close()
        conn.close()

# =========================================================
# ANALYTICS DATA LOADERS (NEW SET)
# =========================================================
def load_total_tracks_count():
    return scalar("SELECT COUNT(*) FROM track")

def load_artist_song_counts():
    """Artists ranked by number of songs in catalog."""
    return fetch_df("""
        SELECT a.artist_name, COUNT(t.track_id) AS song_count
        FROM artist a
        JOIN track t ON a.artist_id = t.artist_id
        GROUP BY a.artist_id, a.artist_name
        ORDER BY song_count DESC
        LIMIT 15
    """)

def load_user_playlist_counts():
    """Users ranked by number of playlists they own."""
    return fetch_df("""
        SELECT u.username, COUNT(p.playlist_id) AS playlist_count
        FROM user u
        LEFT JOIN playlist p ON u.user_id = p.user_id
        GROUP BY u.user_id, u.username
        HAVING playlist_count > 0
        ORDER BY playlist_count DESC
        LIMIT 15
    """)

def load_least_rated_tracks():
    """Tracks with the lowest average rating (min 1 rating)."""
    return fetch_df("""
        SELECT t.title, a.artist_name,
               AVG(ur.rating) AS avg_rating,
               COUNT(ur.rating) AS rating_count
        FROM track t
        JOIN artist a ON t.artist_id = a.artist_id
        JOIN user_rating ur ON t.track_id = ur.track_id
        GROUP BY t.track_id, t.title, a.artist_name
        HAVING rating_count >= 1
        ORDER BY avg_rating ASC, rating_count DESC
        LIMIT 10
    """)

def load_all_users():
    return fetch_df("SELECT user_id, username, email, created_at FROM user ORDER BY user_id")

# =========================================================
# CHART RENDERER — FIXED with proper colored fills
# =========================================================
def render_bar_chart(labels, values, title, color_start="#7c3aed", color_end="#22d3ee",
                     height=320, max_label_len=18):
    """Animated horizontal bar chart with properly visible colored bars."""
    if not labels or not values:
        st.markdown(
            "<div style='color:#7070a0;font-size:.82rem;font-family:DM Mono,monospace;"
            "padding:1rem;'>no data available yet</div>",
            unsafe_allow_html=True)
        return

    safe_labels = [str(l)[:max_label_len] for l in labels]
    float_vals  = [float(v) for v in values]
    max_val     = max(float_vals) if float_vals else 1

    def lerp_color(c1, c2, t):
        r1,g1,b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
        r2,g2,b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
        return (
            int(r1+(r2-r1)*t),
            int(g1+(g2-g1)*t),
            int(b1+(b2-b1)*t)
        )

    rows_html = ""
    for i, (lbl, val) in enumerate(zip(safe_labels, float_vals)):
        pct   = (val / max_val * 100) if max_val > 0 else 0
        t     = i / max(len(safe_labels) - 1, 1)
        r,g,b = lerp_color(color_start, color_end, t)
        col   = f"rgb({r},{g},{b})"
        col_a = f"rgba({r},{g},{b},0.35)"
        delay = i * 55
        rows_html += f"""
        <div class="row" style="animation-delay:{delay}ms">
          <div class="lbl" title="{lbl}">{lbl}</div>
          <div class="track">
            <div class="fill"
                 data-pct="{pct:.2f}"
                 style="background: linear-gradient(90deg, {col}, {col_a});
                        box-shadow: 0 0 12px {col}88;">
            </div>
          </div>
          <div class="num">{val:,.0f}</div>
        </div>"""

    components.html(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&display=swap');
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ background: #0d0d18; font-family: 'DM Mono', monospace; overflow-x: hidden; }}

.wrap {{
    padding: 6px 4px;
    max-height: {height - 14}px;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-width: thin;
    scrollbar-color: rgba(124,58,237,0.4) transparent;
}}
.wrap::-webkit-scrollbar {{ width: 4px; }}
.wrap::-webkit-scrollbar-thumb {{ background: rgba(124,58,237,0.4); border-radius: 4px; }}

@keyframes rowIn {{
    from {{ opacity: 0; transform: translateX(-14px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
}}

.row {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 11px;
    animation: rowIn 0.45s ease both;
}}

.lbl {{
    font-size: 11.5px;
    color: #a0a0c8;
    width: 140px;
    flex-shrink: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    letter-spacing: 0.02em;
}}

.track {{
    flex: 1;
    background: rgba(255,255,255,0.06);
    border-radius: 6px;
    height: 22px;
    position: relative;
    overflow: hidden;
}}

.fill {{
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 0%;
    border-radius: 6px;
    transition: width 1s cubic-bezier(0.34, 1.2, 0.64, 1);
    min-width: 4px;
}}

.num {{
    font-size: 11.5px;
    color: #eeeeff;
    width: 56px;
    text-align: right;
    flex-shrink: 0;
    font-weight: 500;
}}
</style>
</head>
<body>
<div class="wrap" id="wrap">
{rows_html}
</div>
<script>
(function() {{
    // Trigger bar animations after a short delay
    setTimeout(function() {{
        var fills = document.querySelectorAll('.fill');
        fills.forEach(function(f) {{
            var pct = parseFloat(f.getAttribute('data-pct')) || 0;
            f.style.width = pct + '%';
        }});
    }}, 150);
}})();
</script>
</body></html>""", height=height)


def render_stat_big(label, value, color="#a78bfa", sub=""):
    """Large single-number stat display inside chart-wrap."""
    components.html(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{background:#0d0d18;font-family:'DM Mono',monospace;overflow:hidden;}}
.wrap{{
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    height:160px;
    animation:popIn .6s cubic-bezier(.34,1.56,.64,1) both;
}}
@keyframes popIn{{
    from{{transform:scale(.5);opacity:0;}}
    to{{transform:scale(1);opacity:1;}}
}}
.num{{
    font-family:'Bebas Neue',sans-serif;
    font-size:5rem;
    letter-spacing:.04em;
    color:{color};
    text-shadow: 0 0 30px {color}88;
    line-height:1;
}}
.lbl{{
    font-size:.72rem;
    color:#7070a0;
    text-transform:uppercase;
    letter-spacing:.16em;
    margin-top:.4rem;
}}
.sub{{
    font-size:.65rem;
    color:#505070;
    margin-top:.2rem;
    letter-spacing:.08em;
}}
</style></head><body>
<div class="wrap">
    <div class="num">{value}</div>
    <div class="lbl">{label}</div>
    {"<div class='sub'>" + sub + "</div>" if sub else ""}
</div>
</body></html>""", height=170)


# =========================================================
# RECOMMENDATIONS
# =========================================================
def calculate_recommendation_score(
    row,
    avg_energy_n,
    avg_dance_n,
    avg_valence_n,
    avg_acoustic_n
):
    energy = (
        float(row["energy"]) if pd.notna(row["energy"]) else 50.0
    ) / 100.0

    dance = (
        float(row["danceability"]) if pd.notna(row["danceability"]) else 50.0
    ) / 100.0

    valence = (
        float(row["valence"]) if pd.notna(row["valence"]) else 50.0
    ) / 100.0

    acoustic = (
        float(row["acousticness"]) if pd.notna(row["acousticness"]) else 50.0
    ) / 100.0

    audio_sim = (
        (1.0 - abs(energy - avg_energy_n))
        + (1.0 - abs(dance - avg_dance_n))
        + (1.0 - abs(valence - avg_valence_n))
        + (1.0 - abs(acoustic - avg_acoustic_n))
    ) / 4.0

    popularity_score = (
        float(row["popularity"])
        if pd.notna(row["popularity"])
        else 0.0
    ) / 100.0

    rating_score = (
        float(row["user_rating"]) / 5.0
        if pd.notna(row["user_rating"])
        else 0.5
    )

    final_score = (
        0.5 * audio_sim
        + 0.3 * popularity_score
        + 0.2 * rating_score
    )

    return round(max(0.0, min(1.0, final_score)), 4)

def generate_recommendations(user_id, top_n=10):
    conn = get_connection()
    genre_pref_query = """
        SELECT g.genre_id, g.genre_name, SUM(uls.play_count) AS total_plays
        FROM user_listening_summary uls
        JOIN track_genre tg ON uls.track_id = tg.track_id
        JOIN genre g ON tg.genre_id = g.genre_id
        WHERE uls.user_id = %s
        GROUP BY g.genre_id, g.genre_name
        ORDER BY total_plays DESC
    """
    genre_pref = pd.read_sql(genre_pref_query, conn, params=(user_id,))
    user_profile_query = """
        SELECT
            AVG(af.energy)       AS avg_energy,
            AVG(af.danceability) AS avg_danceability,
            AVG(af.valence)      AS avg_valence,
            AVG(af.acousticness) AS avg_acousticness
        FROM user_listening_summary uls
        JOIN audio_features af ON uls.track_id = af.track_id
        WHERE uls.user_id = %s
    """
    user_profile = pd.read_sql(user_profile_query, conn, params=(user_id,))
    if genre_pref.empty:
        conn.close()
        return False, "No listening history found. Play some songs first."
    fav_genres = genre_pref["genre_id"].tolist()
    placeholders = ",".join(["%s"] * len(fav_genres))
    candidate_query = f"""
        SELECT
            t.track_id, t.title, a.artist_name, g.genre_name, t.popularity,
            af.energy, af.danceability, af.valence, af.acousticness,
            COALESCE(ur.rating, NULL) AS user_rating
        FROM track t
        JOIN artist a ON t.artist_id = a.artist_id
        JOIN track_genre tg ON t.track_id = tg.track_id
        JOIN genre g ON tg.genre_id = g.genre_id
        LEFT JOIN audio_features af ON t.track_id = af.track_id
        LEFT JOIN user_rating ur ON t.track_id = ur.track_id AND ur.user_id = %s
        WHERE tg.genre_id IN ({placeholders})
          AND t.track_id NOT IN (
              SELECT track_id FROM user_listening_summary WHERE user_id = %s
          )
    """
    params = [user_id] + fav_genres + [user_id]
    candidates = pd.read_sql(candidate_query, conn, params=params)
    if candidates.empty:
        conn.close()
        return False, "No new candidate songs found for recommendation."

    avg_energy_n   = (float(user_profile.loc[0, "avg_energy"])       if pd.notna(user_profile.loc[0, "avg_energy"])       else 50.0) / 100.0
    avg_dance_n    = (float(user_profile.loc[0, "avg_danceability"])  if pd.notna(user_profile.loc[0, "avg_danceability"])  else 50.0) / 100.0
    avg_valence_n  = (float(user_profile.loc[0, "avg_valence"])       if pd.notna(user_profile.loc[0, "avg_valence"])       else 50.0) / 100.0
    avg_acoustic_n = (float(user_profile.loc[0, "avg_acousticness"])  if pd.notna(user_profile.loc[0, "avg_acousticness"])  else 50.0) / 100.0


    candidates["recommendation_score"] = candidates.apply(
    	lambda row: calculate_recommendation_score(
        	row,
        	avg_energy_n,
        	avg_dance_n,
        	avg_valence_n,
        	avg_acoustic_n
    	),
    axis=1
)
    candidates = candidates.sort_values(by="recommendation_score", ascending=False).head(top_n)

    cursor = conn.cursor()
    cursor.execute("DELETE FROM recommendation WHERE user_id = %s", (user_id,))
    for _, row in candidates.iterrows():
        cursor.execute("""
            INSERT INTO recommendation (user_id, track_id, recommendation_score, generated_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        """, (user_id, int(row["track_id"]), float(row["recommendation_score"])))
    conn.commit()
    conn.close()
    return True, "Recommendations generated successfully."

def load_recommendations(user_id):
    return fetch_df("""
        SELECT
            r.recommendation_id,
            t.track_id,
            t.title,
            a.artist_name,
            COALESCE(GROUP_CONCAT(DISTINCT g.genre_name ORDER BY g.genre_name SEPARATOR ', '), 'Unknown') AS genre_name,
            r.recommendation_score,
            r.generated_at,
            tm.youtube_link AS Youtube_Link
        FROM recommendation r
        JOIN track t ON r.track_id = t.track_id
	LEFT JOIN track_media tm ON tm.track_id = t.track_id
        JOIN artist a ON t.artist_id = a.artist_id
        LEFT JOIN track_genre tg ON t.track_id = tg.track_id
        LEFT JOIN genre g ON tg.genre_id = g.genre_id
        
        WHERE r.user_id = %s
        GROUP BY r.recommendation_id, t.track_id, t.title, a.artist_name,
                 r.recommendation_score, r.generated_at, tm.youtube_link
        ORDER BY r.recommendation_score DESC, r.generated_at DESC
    """, (user_id,))

# =========================================================
# BOT
# =========================================================
BOT_INTROS = [
    "bestie 🎧 **{title}** by **{artist}** just dropped on the queue. such a serve for {genre} rn no cap.",
    "omg **{title}** hits different. **{artist}** really cooked with this one fr fr.",
    "**{title}** is giving main character energy rn. not me being obsessed with this {genre} era.",
    "the way **{artist}** went OFF on **{title}** like…the audacity to be this good??",
]
BOT_REPLIES = [
    "okay so **{title}** gives me very much late night drive vibes. want me to build a whole vibe around it?",
    "**{artist}** understood the assignment. this {genre} mood needs more songs that slap the same way.",
    "the way this track lives rent free in my head now. should we make a whole playlist or..?",
    "bestie this is literally the sound of 3am crying in a good way. i'm obsessed. want recs?",
    "**{title}** is SO that girl. peak {genre} energy. more songs like this? say less.",
]

def bot_intro(title, artist, genre):
    return random.choice(BOT_INTROS).format(title=title, artist=artist, genre=genre or "music")

def bot_reply(title, artist, genre):
    return random.choice(BOT_REPLIES).format(
        title=title or "this track", artist=artist or "this artist", genre=genre or "music")

# =========================================================
# MASCOT
# =========================================================
MASCOT_QUOTES = [
    "yesss added! this playlist just leveled up 🔥",
    "track secured. we are SO eating tonight bestie",
    "your taste? immaculate fr fr. added!",
    "playlist blessed. no skip energy only.",
    "added to the queue! this is the way bestie.",
    "another one! 🎧 DJ Khaled would be proud.",
    "slay! that track belongs on every playlist.",
]

def render_dancing_mascot(song_title: str):
    quote = random.choice(MASCOT_QUOTES)
    components.html(f"""
    <html><head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@500&display=swap');
    *{{margin:0;padding:0;box-sizing:border-box;}}
    body{{background:transparent;overflow:hidden;font-family:'DM Mono',monospace;}}
    .wrap{{width:100%;height:220px;display:flex;align-items:center;justify-content:center;gap:28px;
           background:rgba(5,5,8,0.96);border:1px solid rgba(124,58,237,0.45);border-radius:20px;
           position:relative;overflow:hidden;}}
    .wrap::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;
                  background:linear-gradient(90deg,#7c3aed,#db2777,#22d3ee,#7c3aed);
                  background-size:200% 100%;animation:barMove 2s linear infinite;}}
    @keyframes barMove{{0%{{background-position:0% 0%;}}100%{{background-position:200% 0%;}}}}
    .wrap::after{{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;
                 background:linear-gradient(90deg,#22d3ee,#7c3aed,#db2777,#22d3ee);
                 background-size:200% 100%;animation:barMove 2s linear infinite reverse;}}
    .bg-glow{{position:absolute;inset:0;
              background:radial-gradient(ellipse at 35% 50%,rgba(124,58,237,0.12),transparent 65%);
              pointer-events:none;animation:glowPulse 2s ease-in-out infinite;}}
    @keyframes glowPulse{{0%,100%{{opacity:.6;}}50%{{opacity:1;}}}}
    .mascot-area{{position:relative;display:flex;flex-direction:column;align-items:center;}}
    .mascot{{font-size:72px;line-height:1;display:block;text-align:center;
             transform-origin:bottom center;animation:dance 0.42s ease-in-out infinite alternate;
             filter:drop-shadow(0 0 18px rgba(167,139,250,0.7));}}
    @keyframes dance{{
        0%  {{transform:rotate(-20deg) translateY(2px) scale(0.97);}}
        30% {{transform:rotate(0deg) translateY(-16px) scale(1.1);}}
        60% {{transform:rotate(14deg) translateY(-8px) scale(1.06);}}
        100%{{transform:rotate(-10deg) translateY(-18px) scale(1.12);}}
    }}
    .note{{position:absolute;font-size:18px;opacity:0;animation:floatNote 1.8s ease-out infinite;pointer-events:none;color:#a78bfa;}}
    .n1{{left:55px;top:5px;animation-delay:0s;}}
    .n2{{left:-18px;top:22px;animation-delay:.6s;color:#f472b6;}}
    .n3{{left:62px;top:45px;animation-delay:1.2s;color:#22d3ee;}}
    .n4{{left:-8px;top:55px;animation-delay:.3s;}}
    @keyframes floatNote{{0%{{opacity:0;transform:translateY(0) rotate(-10deg) scale(0.7);}}25%{{opacity:1;}}100%{{opacity:0;transform:translateY(-60px) rotate(25deg) scale(1.1);}}}}
    .mascot-shadow{{width:50px;height:10px;background:radial-gradient(ellipse,rgba(124,58,237,0.5),transparent 70%);border-radius:50%;margin-top:4px;animation:shadowPulse .42s ease-in-out infinite alternate;}}
    @keyframes shadowPulse{{0%{{transform:scaleX(1);opacity:.7;}}100%{{transform:scaleX(0.6);opacity:.3;}}}}
    .bubble{{background:linear-gradient(135deg,rgba(13,13,20,0.97),rgba(26,26,40,0.97));border:1px solid rgba(124,58,237,0.45);border-radius:20px 20px 20px 6px;padding:14px 20px;max-width:300px;position:relative;animation:bubblePop .5s cubic-bezier(.34,1.56,.64,1) both;box-shadow:0 8px 32px rgba(124,58,237,0.2);}}
    @keyframes bubblePop{{from{{transform:scale(.6) translateX(-10px);opacity:0;}}to{{transform:scale(1) translateX(0);opacity:1;}}}}
    .bubble::before{{content:'';position:absolute;left:-10px;top:18px;border:6px solid transparent;border-right-color:rgba(124,58,237,0.45);}}
    .song-added{{font-family:'Bebas Neue',sans-serif;font-size:1.05rem;letter-spacing:.08em;color:#34d399;margin-bottom:6px;text-shadow:0 0 12px rgba(52,211,153,.6);}}
    .quote-text{{font-size:.8rem;color:#eeeeff;line-height:1.5;}}
    .song-name{{font-size:.72rem;color:#a78bfa;font-family:'DM Mono',monospace;margin-top:8px;border-top:1px solid rgba(124,58,237,0.2);padding-top:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:260px;}}
    .confetti-wrap{{position:absolute;inset:0;pointer-events:none;overflow:hidden;}}
    .cf{{position:absolute;animation:cfFall ease forwards;opacity:0;border-radius:2px;}}
    @keyframes cfFall{{0%{{opacity:1;transform:translateY(0) rotate(0deg) scale(1);}}100%{{opacity:0;transform:translateY(-120px) rotate(600deg) scale(.4);}}}}
    </style>
    </head>
    <body>
    <div class="wrap">
        <div class="bg-glow"></div>
        <div class="confetti-wrap" id="cc"></div>
        <div class="mascot-area">
            <span class="note n1">&#9835;</span>
            <span class="note n2">&#9833;</span>
            <span class="note n3">&#9836;</span>
            <span class="note n4">&#9834;</span>
            <span class="mascot">&#x1F916;</span>
            <div class="mascot-shadow"></div>
        </div>
        <div class="bubble">
            <div class="song-added">&#10010; added to playlist!</div>
            <div class="quote-text">{quote}</div>
            <div class="song-name">&#9835; {song_title}</div>
        </div>
    </div>
    <script>
    const cc=document.getElementById('cc');
    const colors=['#a78bfa','#f472b6','#22d3ee','#34d399','#fbbf24','#fb923c'];
    const shapes=['50%','2px','50%','4px','50%','2px'];
    for(let i=0;i<32;i++){{
        const el=document.createElement('div');el.className='cf';
        const size=(5+Math.random()*8)+'px';
        el.style.cssText=`left:${{Math.random()*100}}%;bottom:20px;width:${{size}};height:${{size}};background:${{colors[i%6]}};border-radius:${{shapes[i%6]}};animation-delay:${{Math.random()*.8}}s;animation-duration:${{1+Math.random()*1}}s;box-shadow:0 0 6px ${{colors[i%6]}}88;`;
        cc.appendChild(el);
    }}
    </script>
    </body></html>
    """, height=230)

# =========================================================
# STAR BURST ANIMATION
# =========================================================
def render_star_burst_if_pending():
    if not st.session_state.pending_burst:
        return
    val = st.session_state.burst_val
    label = {1:"kinda mid ngl",2:"lowkey fire",3:"it slaps fr",4:"absolute banger",5:"GOATED NO SKIP 🔥"}.get(val,"rated!")
    action_word = "updated" if st.session_state.get("burst_was_update") else "locked in"
    components.html(f"""
    <html><head><style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@500&display=swap');
    *{{margin:0;padding:0;box-sizing:border-box;}}
    body{{background:transparent;overflow:hidden;}}
    .wrap{{width:100%;height:270px;display:flex;flex-direction:column;align-items:center;justify-content:center;
           background:rgba(5,5,8,0.95);border:1px solid rgba(124,58,237,0.4);border-radius:20px;
           position:relative;overflow:hidden;}}
    .wrap::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;
                  background:linear-gradient(90deg,#7c3aed,#db2777,#0891b2);
                  animation:lineGlow 2s ease-in-out infinite;}}
    @keyframes lineGlow{{0%,100%{{opacity:.6;}}50%{{opacity:1;}}}}
    .confetti-container{{position:absolute;inset:0;pointer-events:none;overflow:hidden;}}
    .confetti{{position:absolute;width:8px;height:8px;border-radius:2px;animation:confettiFall 1.5s ease forwards;opacity:0;}}
    @keyframes confettiFall{{0%{{transform:translateY(-20px) rotate(0deg) scale(0);opacity:0;}}20%{{opacity:1;}}100%{{transform:translateY(280px) rotate(720deg) scale(0.5);opacity:0;}}}}
    .stars{{font-size:52px;letter-spacing:6px;margin-bottom:10px;position:relative;z-index:1;animation:starsBurst .5s cubic-bezier(0.34,1.56,0.64,1) both;}}
    @keyframes starsBurst{{0%{{transform:scale(.2) rotate(-15deg);opacity:0;}}60%{{transform:scale(1.2) rotate(5deg);}}100%{{transform:scale(1) rotate(0deg);opacity:1;}}}}
    .label{{font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:.06em;color:#eeeeff;position:relative;z-index:1;animation:labelFade .4s ease .2s both;}}
    @keyframes labelFade{{from{{opacity:0;transform:translateY(10px);}}to{{opacity:1;transform:translateY(0);}}}}
    .sub{{font-size:.75rem;color:#7070a0;font-family:'DM Mono',monospace;margin-top:6px;position:relative;z-index:1;animation:labelFade .4s ease .35s both;}}
    </style></head><body>
    <div class="wrap">
        <div class="confetti-container" id="cc"></div>
        <div class="stars">{"⭐"*val}{"☆"*(5-val)}</div>
        <div class="label">{label}</div>
        <div class="sub">rating {action_word} ✓</div>
    </div>
    <script>
    const colors=['#a78bfa','#f472b6','#22d3ee','#34d399','#fbbf24'];
    const cc=document.getElementById('cc');
    for(let i=0;i<24;i++){{
        const el=document.createElement('div');el.className='confetti';
        el.style.cssText=`left:${{Math.random()*100}}%;background:${{colors[i%5]}};animation-delay:${{Math.random()*0.8}}s;animation-duration:${{1+Math.random()}}s;border-radius:${{Math.random()>.5?'50%':'2px'}};`;
        cc.appendChild(el);
    }}
    </script>
    </body></html>
    """, height=280)
    st.session_state.pending_burst = None
    st.session_state.burst_val = 0
    if "burst_was_update" in st.session_state:
        del st.session_state["burst_was_update"]

# =========================================================
# STAR RATING
# =========================================================
def render_star_rating(track_id):
    tid = int(track_id)
    s_key = f"star_{tid}"
    d_key = f"done_{tid}"
    e_key = f"edit_{tid}"

    if s_key not in st.session_state.star_selections:
        existing = get_existing_rating(st.session_state.user_id, tid)
        st.session_state.star_selections[s_key] = existing if existing is not None else 0
        st.session_state.star_saved[d_key] = existing is not None
        st.session_state.rating_edit_mode[e_key] = False

    current = st.session_state.star_selections[s_key]
    saved   = st.session_state.star_saved.get(d_key, False)
    editing = st.session_state.rating_edit_mode.get(e_key, False)
    labels  = {0:"",1:"mid tbh",2:"lowkey fire",3:"it slaps",4:"big banger",5:"NO SKIP 🔥"}

    if saved and not editing:
        star_str = "⭐" * current + "☆" * (5 - current)
        cols = st.columns([3, 2, 2])
        with cols[0]:
            st.markdown(
                f"<div style='font-size:22px;padding-top:4px;letter-spacing:4px;'>{star_str}"
                f"<span style='font-size:.75rem;color:var(--neon-green);font-family:DM Mono,monospace;"
                f"margin-left:10px;vertical-align:middle;border:1px solid rgba(52,211,153,0.3);"
                f"background:rgba(52,211,153,0.08);border-radius:999px;padding:2px 10px;'>"
                f"{labels.get(current,'')}</span></div>",
                unsafe_allow_html=True)
        with cols[1]:
            if st.button("✏ change rating", key=f"edit_btn_{tid}"):
                st.session_state.rating_edit_mode[e_key] = True
                st.session_state.star_saved[d_key] = False
                st.rerun()
        return

    cols = st.columns([1,1,1,1,1,2,2])
    for i in range(1, 6):
        filled = (i <= current)
        color  = "#a78bfa" if filled else "rgba(255,255,255,0.2)"
        size   = "30px" if filled else "22px"
        shadow = "drop-shadow(0 0 6px rgba(167,139,250,0.7))" if filled else "none"
        with cols[i-1]:
            st.markdown(
                f"<div style='font-size:{size};color:{color};text-align:center;"
                f"transition:all .2s;filter:{shadow};cursor:pointer;'>★</div>",
                unsafe_allow_html=True)
            if st.button(f"{i}", key=f"sstar_{tid}_{i}"):
                st.session_state.star_selections[s_key] = i
                st.session_state.star_saved[d_key] = False
                st.rerun()

    with cols[5]:
        if current > 0:
            st.markdown(
                f"<div style='font-size:.8rem;color:var(--neon-purple);padding-top:7px;"
                f"font-weight:600;font-family:DM Mono,monospace;'>{labels[current]}</div>",
                unsafe_allow_html=True)

    with cols[6]:
        if current > 0:
            is_update = editing
            btn_label = "update ✓" if is_update else "save rating"
            if st.button(btn_label, key=f"save_star_{tid}"):
                ok, msg = rate_song(st.session_state.user_id, tid, current)
                if ok:
                    st.session_state.star_saved[d_key] = True
                    st.session_state.rating_edit_mode[e_key] = False
                    st.session_state.pending_burst = tid
                    st.session_state.burst_val = current
                    st.session_state["burst_was_update"] = is_update
                    st.rerun()
                else:
                    st.error(msg)

# =========================================================
# HELPERS
# =========================================================
def show_feedback(kind, message):
    icons = {"success":"✓","warning":"⚠","error":"✕"}
    css   = {"success":"fb-success","warning":"fb-warning","error":"fb-error"}
    st.markdown(
        f'<div class="{css.get(kind, "fb-success")}"><span>{icons.get(kind, "•")}</span> {message}</div>',
        unsafe_allow_html=True)

def render_inline_bot(track_id, title, artist, genre):
    tid = int(track_id)
    msgs_key = str(tid)
    if msgs_key not in st.session_state.bot_messages:
        st.session_state.bot_messages[msgs_key] = []
    msgs    = st.session_state.bot_messages[msgs_key]
    counter = st.session_state.bot_input_counter

    st.markdown(f"""
    <div class='bot-wrap'>
        <div class='bot-header'>
            <div class='bot-avatar'>🤖</div>
            <div>
                <div class='bot-name'>PulseBeat AI</div>
                <div class='bot-sub'>vibing to {title}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='bot-scroll'>", unsafe_allow_html=True)
    for role, text in msgs[-10:]:
        css = "bot-msg-ai" if role == "ai" else "bot-msg-user"
        st.markdown(f"<div class='{css}'>{text}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    inp_col, send_col, close_col = st.columns([5,1,1])
    with inp_col:
        user_text = st.text_input(
            "msg", label_visibility="collapsed",
            placeholder="ask anything about this track…",
            key=f"bot_inp_{tid}_{counter}")
    with send_col:
        if st.button("send", key=f"bot_send_{tid}_{counter}"):
            if user_text.strip():
                msgs.append(("user", user_text.strip()))
                msgs.append(("ai", bot_reply(title, artist, genre)))
                st.session_state.bot_messages[msgs_key] = msgs
                st.session_state.bot_input_counter += 1
                st.rerun()
    with close_col:
        if st.button("✕", key=f"bot_close_{tid}_{counter}"):
            st.session_state.active_bot_track_id = None
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_comment_section(track_id, title):
    """Render comments section — visible to all logged-in users."""
    tid = int(track_id)
    comment_count = get_comment_count(tid)
    comments_df   = load_comments(tid)

    st.markdown(f"""
    <div class='comment-section'>
        <div class='comment-header'>
            💬 community takes
            <span style='font-size:.7rem;color:var(--muted);font-family:DM Mono,monospace;
                         margin-left:.5rem;'>{comment_count} comment{'s' if comment_count != 1 else ''}</span>
        </div>
    """, unsafe_allow_html=True)

    # Post new comment
    c_input, c_btn = st.columns([5, 1])
    with c_input:
        new_comment = st.text_input(
            "comment",
            label_visibility="collapsed",
            placeholder=f"share your take on {title}…",
            key=f"comment_input_{tid}"
        )
    with c_btn:
        if st.button("post", key=f"comment_post_{tid}"):
            if new_comment.strip():
                ok, msg = post_comment(tid, st.session_state.user_id, st.session_state.username, new_comment.strip())
                if ok:
                    st.rerun()
                else:
                    show_feedback("error", msg)
            else:
                show_feedback("warning", "write something first!")

    # Display existing comments
    if not comments_df.empty:
        st.markdown("<div style='margin-top:.8rem;max-height:280px;overflow-y:auto;scrollbar-width:thin;'>", unsafe_allow_html=True)
        for _, row in comments_df.iterrows():
            time_str = str(row["created_at"])[:16]
            is_mine  = (row["username"] == st.session_state.username)
            name_color = "#f472b6" if is_mine else "#a78bfa"
            badge = " <span style='font-size:.58rem;background:rgba(244,114,182,0.1);border:1px solid rgba(244,114,182,0.3);border-radius:999px;padding:1px 7px;color:#f472b6;'>you</span>" if is_mine else ""
            st.markdown(f"""
            <div class='comment-item'>
                <div class='comment-user' style='color:{name_color} !important;'>
                    @{row['username']}{badge}
                </div>
                <div class='comment-text'>{row['comment_text']}</div>
                <div class='comment-time'>{time_str}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div class='comment-empty'>no comments yet — be the first to share your vibe 🎵</div>",
            unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_mood_card(user_id):
    """Render the user's current mood based on their listening audio features."""
    profile_df = get_user_mood_profile(user_id)
    if profile_df.empty or int(profile_df.iloc[0]["track_count"] or 0) == 0:
        st.markdown("""
        <div style='background:rgba(124,58,237,0.06);border:1px solid rgba(124,58,237,0.15);
                    border-radius:18px;padding:1.4rem 1.6rem;margin-bottom:1.5rem;'>
            <div style='font-family:DM Mono,monospace;font-size:.72rem;letter-spacing:.14em;
                        text-transform:uppercase;color:var(--muted);margin-bottom:.4rem;'>// your vibe</div>
            <div style='font-family:Bebas Neue,sans-serif;font-size:1.6rem;letter-spacing:.04em;
                        color:var(--muted);'>play songs to unlock your mood profile 🎧</div>
        </div>
        """, unsafe_allow_html=True)
        return

    row         = profile_df.iloc[0]
    avg_energy  = float(row["avg_energy"]  or 50)
    avg_valence = float(row["avg_valence"] or 50)
    avg_dance   = float(row["avg_dance"]   or 50)
    track_count = int(row["track_count"]   or 0)

    mood_label, mood_emoji, mood_desc, mood_color, bg_color = classify_mood(avg_energy, avg_valence, avg_dance)

    # Feature bar mini
    def feat_bar(name, val, color):
        pct = min(100, max(0, float(val)))
        return f"""
        <div style='margin-bottom:6px;'>
            <div style='display:flex;justify-content:space-between;margin-bottom:3px;'>
                <span style='font-size:.82rem;color:#f4f1ff;font-family:DM Mono,monospace;font-weight:700;letter-spacing:.04em;text-shadow:0 0 8px rgba(255,255,255,.08);'>{name}</span>
                <span style='font-size:.84rem;color:{color};font-family:DM Mono,monospace;font-weight:800;text-shadow:0 0 10px {color}88;'>{pct:.0f}</span>
            </div>
            <div style='height:10px;background:rgba(255,255,255,0.10);border:1px solid rgba(255,255,255,0.08);border-radius:999px;overflow:hidden;box-shadow:inset 0 0 0 1px rgba(255,255,255,0.02);'>
                <div style='height:100%;width:{pct:.0f}%;background:{color};border-radius:999px;
                            box-shadow:0 0 14px {color}88, 0 0 24px {color}33;transition:width 1s ease;'></div>
            </div>
        </div>"""

    components.html(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&family=Outfit:wght@400;600&display=swap');
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{background:#050508;font-family:'DM Mono',monospace;overflow:hidden;}}
.card{{
    background: linear-gradient(135deg, {bg_color}, rgba(13,13,20,0.95));
    border: 1px solid {mood_color}44;
    border-radius: 20px;
    padding: 1.4rem 2.8rem 1.6rem 1.8rem;
    position: relative;
    overflow: hidden;
    animation: cardIn .6s cubic-bezier(.34,1.56,.64,1) both;
}}
@keyframes cardIn{{from{{transform:translateY(20px) scale(.97);opacity:0;}}to{{transform:translateY(0) scale(1);opacity:1;}}}}
.card::before{{
    content:'';position:absolute;top:0;left:0;right:0;height:3px;
    background:linear-gradient(90deg,{mood_color},{mood_color}88,transparent);
    animation:lineGlow 2s ease-in-out infinite;
}}
@keyframes lineGlow{{0%,100%{{opacity:.7;}}50%{{opacity:1;}}}}
.card::after{{
    content:'';position:absolute;top:-40px;right:-40px;width:160px;height:160px;
    border-radius:50%;
    background:radial-gradient(circle,{mood_color}22,transparent 70%);
    pointer-events:none;
    animation:orbFloat 4s ease-in-out infinite;
}}
@keyframes orbFloat{{0%,100%{{transform:scale(1);}}50%{{transform:scale(1.15);}}}}
.tag{{font-size:.72rem;letter-spacing:.20em;text-transform:uppercase;color:#d7c7ff;
      margin-bottom:.65rem;font-weight:700;text-shadow:0 0 12px rgba(167,139,250,.28);}}
.top{{display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem;}}
.emoji{{font-size:3.2rem;line-height:1;
        animation:emojiBounce 2s ease-in-out infinite;}}
@keyframes emojiBounce{{0%,100%{{transform:translateY(0) rotate(-3deg);}}50%{{transform:translateY(-6px) rotate(3deg);}}}}
.mood-name{{font-family:'Bebas Neue',sans-serif;font-size:2.6rem;letter-spacing:.06em;
            color:{mood_color};text-shadow:0 0 20px {mood_color}66;line-height:1;}}
.mood-desc{{font-size:.95rem;color:#f1eeff;margin-top:.35rem;line-height:1.5;font-weight:500;}}
.divider{{height:1px;background:linear-gradient(90deg,{mood_color}88,rgba(255,255,255,.08),transparent);margin:1.15rem 0;box-shadow:0 0 12px {mood_color}44;}}
.feats-title{{font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;color:#bcaeff;margin-bottom:1rem;font-weight:700;}}
.count-badge{{
    display:inline-flex;align-items:center;gap:.4rem;margin-top:1rem;
    background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
    border-radius:999px;padding:3px 12px;
    font-size:.82rem;color:#d9d3ff;font-weight:700;
}}
</style></head><body>
<div class="card">
    <div class="tag">// your current vibe</div>
    <div class="top">
        <div class="emoji">{mood_emoji}</div>
        <div>
            <div class="mood-name">{mood_label}</div>
            <div class="mood-desc">{mood_desc}</div>
        </div>
    </div>
    <div class="divider"></div>
    <div class="feats-title">based on your listening · audio features avg</div>
    {feat_bar("Energy", avg_energy, mood_color)}
    {feat_bar("Valence (happiness)", avg_valence, "#f472b6")}
    {feat_bar("Danceability", avg_dance, "#22d3ee")}
    <div class="count-badge">
        <span>🎵</span>
        <span>from {track_count} track{'s' if track_count != 1 else ''} in your history</span>
    </div>
</div>
</body></html>""", height=350)


# =========================================================
# NAV
# =========================================================
def render_nav():
    if st.session_state.logged_in:
        st.markdown("<div class='nav-bar'>", unsafe_allow_html=True)
        st.markdown("<span class='nav-brand'>PulseBeat</span>", unsafe_allow_html=True)
        cols = st.columns([1,1,1,1,1,1,1,2])
        items = [
            ("Dashboard","Home"),
            ("Song Parlor","discover"),
            ("My Songbooks","playlists"),
            ("Listening Diary","history"),
            ("Little Reviews","reviews"),
            ("For You","for you ✨"),
        ]
        for i,(page,label) in enumerate(items):
            if cols[i].button(label, key=f"nav_{label}"):
                go_to(page); st.rerun()
        if cols[6].button("logout", key="nav_logout"):
            logout_user(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.admin_logged_in:
        st.markdown("<div class='nav-bar'>", unsafe_allow_html=True)
        st.markdown("<span class='nav-brand'>PulseBeat Admin</span>", unsafe_allow_html=True)
        c1, c2, c3, c4, c5, c6, _ = st.columns([1,1,1,1,1,1,2])
        if c1.button("dashboard"):    go_to("House Ledger"); st.rerun()
        if c2.button("analytics"):    go_to("Admin Analytics"); st.rerun()
        if c3.button("playlists"):    go_to("Admin Playlists"); st.rerun()
        if c4.button("songs"):        go_to("Admin Songs"); st.rerun()
        if c5.button("sql lab"):      go_to("SQL Queries & Insights"); st.rerun()
        if c6.button("logout"):       logout_admin(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# PAGES
# =========================================================
def page_welcome():
    hero1, hero2, hero3 = st.columns([1.1, 1, 0.9], gap="large")

    with hero1:
        st.markdown("""
        <div class="hero-wrap">
            <div class="hero-eyebrow"><span class="dot"></span>now streaming · gen z edition</div>
            <div class="hero-title">
                Your music.<br>Your <span class="grad">vibe.</span><br>No rules.
            </div>
            <div class="hero-desc">
                A next-gen music space where you rate, playlist, and actually talk about the songs you're obsessed with.
            </div>
            <div class="stat-row">
                <div class="stat-chip"><b>100%</b> vibe-based</div>
                <div class="stat-chip"><b>Mood Checker</b>✅</div>
                <div class="stat-chip"><b>∞</b> playlists</div>
                <div class="stat-chip"><b>✨</b> for you recs</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with hero2:
        st.markdown("""
        <div class="form-card">
            <div class="form-title">drop in 👋</div>
            <div class="form-sub">// guest access — no pw needed</div>
        """, unsafe_allow_html=True)
        with st.form("user_form"):
            username = st.text_input("your name", placeholder="what do we call you?")
            email    = st.text_input("email", placeholder="your@email.com")
            if st.form_submit_button("enter the app →"):
                if not username.strip() or not email.strip():
                    st.warning("fill in both fields bestie")
                else:
                    uid, uname, uemail, _ = create_or_get_user(username.strip(), email.strip())
                    st.session_state.update(
                        logged_in=True, user_id=uid, username=uname,
                        email=uemail, page="Dashboard")
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with hero3:
        st.markdown("""
        <div class="form-card" style="margin-bottom:0;">
            <div class="form-title">admin 🔐</div>
            <div class="form-sub">// house keeper access</div>
        """, unsafe_allow_html=True)
        with st.form("admin_form"):
            aemail = st.text_input("admin email", placeholder="admin@pulsebeat.io")
            apwd   = st.text_input("password", type="password", placeholder="••••••••")
            if st.form_submit_button("open ledger →"):
                result = admin_login(aemail.strip(), apwd)
                if result["success"]:
                    st.session_state.update(
                        admin_logged_in=True, admin_id=result["admin_id"],
                        admin_username=result["username"], page="House Ledger")
                    st.rerun()
                else:
                    st.error(result["message"])
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr class='glow-divider'>", unsafe_allow_html=True)

    feat1, feat2, feat3, feat4 = st.columns(4, gap="medium")
    feats = [
        ("🎵","discover tracks","browse the full catalog. search by vibe, genre, whatever hits."),
        ("📋","build playlists","curate your playlists like the main character you are."),
        ("🤖","ai companion","chat about any song with your built-in AI music bestie."),
        ("✨","for you","get personalised recs based on what you actually listen to."),
    ]
    for col,(icon,title,desc) in zip([feat1,feat2,feat3,feat4], feats):
        col.markdown(f"""
        <div class="glass-card" style="text-align:center;padding:2rem 1.2rem;">
            <div style="font-size:2rem;margin-bottom:.8rem;">{icon}</div>
            <div style="font-family:'Bebas Neue',sans-serif;font-size:1.2rem;letter-spacing:.04em;margin-bottom:.5rem;">{title}</div>
            <div style="font-size:.83rem;color:var(--muted);line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


def page_dashboard():
    if not require_user(): return

    summary_df   = load_user_summary(st.session_state.user_id)
    ratings_df   = load_user_ratings(st.session_state.user_id)
    playlists_df = load_user_playlists(st.session_state.user_id)
    total_plays  = int(summary_df["play_count"].sum()) if not summary_df.empty else 0

    st.markdown(f"""
    <div style="padding-top:1.5rem;margin-bottom:2rem;animation:heroFadeUp .6s cubic-bezier(0.34,1.56,0.64,1) both;">
        <div class="section-tag">// your dashboard</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:3.5rem;letter-spacing:0.04em;color:var(--text);">
            hey {st.session_state.username} 👾
        </div>
        <div style="color:var(--muted);font-size:.85rem;font-family:'DM Mono',monospace;margin-top:.3rem;">
            what are we vibing to today?
        </div>
    </div>
    <div class="metric-grid">
        <div class="metric-tile" style="animation-delay:.05s;">
            <div class="m-label">playlists</div>
            <div class="m-val">{len(playlists_df)}</div>
        </div>
        <div class="metric-tile" style="animation-delay:.12s;">
            <div class="m-label">ratings</div>
            <div class="m-val">{len(ratings_df)}</div>
        </div>
        <div class="metric-tile" style="animation-delay:.19s;">
            <div class="m-label">total plays</div>
            <div class="m-val">{total_plays}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MOOD CARD ──
    st.markdown("<div class='section-tag' style='margin-bottom:.4rem;'>// your mood profile</div>", unsafe_allow_html=True)
    render_mood_card(st.session_state.user_id)


    # ── ANIMATED WAVEFORM HERO ──
    components.html("""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&display=swap');
*{margin:0;padding:0;box-sizing:border-box;}
html,body{background:#050508;overflow:hidden;font-family:'DM Mono',monospace;}
.hero{
    width:100%;height:110px;
    display:flex;align-items:flex-end;justify-content:center;gap:3px;
    padding-bottom:10px;position:relative;
}
.hero::before{
    content:'';position:absolute;inset:0;
    background:radial-gradient(ellipse 70% 80% at 50% 100%,rgba(124,175,237,0.18),transparent 20%);
    pointer-events:none;
}
.bar{
    width:4px;border-radius:4px 4px 0 0;
    animation:wave ease-in-out infinite;
    transform-origin:bottom center;
}
@keyframes wave{
    0%,100%{transform:scaleY(0.15);}
    50%{transform:scaleY(1);}
}
</style>
</head>
<body>
<div class="hero" id="wv"></div>
<script>
const wv=document.getElementById('wv');
const colors=['#7c3aed','#8b3aed','#9c3aed','#a855f7','#c084fc','#db2777','#ec4899','#f472b6',
               '#f472b6','#ec4899','#db2777','#c084fc','#a855f7','#9c3aed','#8b3aed','#7c3aed',
               '#0891b2','#0ea5e9','#22d3ee','#34d3ee','#22d3ee','#0ea5e9','#0891b2',
               '#7c3aed','#a855f7','#db2777','#f472b6','#c084fc','#8b3aed','#7c3aed',
               '#0891b2','#22d3ee','#34d3ee','#0891b2'];
const n=colors.length;
for(let i=0;i<n;i++){
    const b=document.createElement('div');
    b.className='bar';
    const maxH=40+Math.random()*60;
    b.style.cssText=`height:${maxH}px;background:${colors[i]};animation-duration:${0.6+Math.random()*1.2}s;animation-delay:${(i/n*1.5).toFixed(2)}s;box-shadow:0 0 8px ${colors[i]}88;`;
    wv.appendChild(b);
}
</script>
</body></html>""", height=120)


    # ── ANIMATED WAVEFORM HERO ──
    components.html("""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&display=swap');
*{margin:0;padding:0;box-sizing:border-box;}
html,body{background:#050508;overflow:hidden;font-family:'DM Mono',monospace;}
.hero{
    width:100%;height:110px;
    display:flex;align-items:flex-end;justify-content:center;gap:3px;
    padding-bottom:10px;position:relative;
}
.hero::before{
    content:'';position:absolute;inset:0;
    background:radial-gradient(ellipse 70% 80% at 50% 100%,rgba(124,58,237,0.18),transparent 70%);
    pointer-events:none;
}
.bar{
    width:4px;border-radius:4px 4px 0 0;
    animation:wave ease-in-out infinite;
    transform-origin:bottom center;
}
@keyframes wave{
    0%,100%{transform:scaleY(0.15);}
    50%{transform:scaleY(1);}
}
</style>
</head>
<body>
<div class="hero" id="wv"></div>
<script>
const wv=document.getElementById('wv');
const colors=['#7c3aed','#8b3aed','#9c3aed','#a855f7','#c084fc','#db2777','#ec4899','#f472b6',
               '#f472b6','#ec4899','#db2777','#c084fc','#a855f7','#9c3aed','#8b3aed','#7c3aed',
               '#0891b2','#0ea5e9','#22d3ee','#34d3ee','#22d3ee','#0ea5e9','#0891b2',
               '#7c3aed','#a855f7','#db2777','#f472b6','#c084fc','#8b3aed','#7c3aed',
               '#0891b2','#22d3ee','#34d3ee','#0891b2'];
const n=colors.length;
for(let i=0;i<n;i++){
    const b=document.createElement('div');
    b.className='bar';
    const maxH=40+Math.random()*60;
    b.style.cssText=`height:${maxH}px;background:${colors[i]};animation-duration:${0.6+Math.random()*1.2}s;animation-delay:${(i/n*1.5).toFixed(2)}s;box-shadow:0 0 8px ${colors[i]}88;`;
    wv.appendChild(b);
}
</script>
</body></html>""", height=120)

    if st.session_state.current_song_title:
        st.markdown(f"""
        <style>
        @keyframes pulseRing {{
            0%   {{ transform: scale(0.85); box-shadow: 0 0 0 0 rgba(167,139,250,0.6); }}
            70%  {{ transform: scale(1);    box-shadow: 0 0 0 14px rgba(167,139,250,0); }}
            100% {{ transform: scale(0.85); box-shadow: 0 0 0 0 rgba(167,139,250,0); }}
        }}
        @keyframes lastPlayedSlideIn {{
            from {{ transform: translateX(-24px) scale(0.95); opacity: 0; }}
            to   {{ transform: translateX(0) scale(1); opacity: 1; }}
        }}
        @keyframes vinylSpin {{
            0%   {{ transform: rotate(0deg) scale(1); }}
            50%  {{ transform: rotate(180deg) scale(1.05); }}
            100% {{ transform: rotate(360deg) scale(1); }}
        }}
        @keyframes textGlow {{
            0%, 100% {{ text-shadow: 0 0 8px rgba(167,139,250,0.3); }}
            50%       {{ text-shadow: 0 0 18px rgba(244,114,182,0.6); }}
        }}
        .lp-ring {{
            width: 56px; height: 56px; border-radius: 50%;
            background: linear-gradient(135deg, #7c3aed, #db2777);
            display: flex; align-items: center; justify-content: center;
            font-size: 22px; flex-shrink: 0;
            animation: pulseRing 2.2s ease-in-out infinite;
        }}
        .lp-badge {{
            display: inline-flex; align-items: center; gap: 6px;
            background: rgba(52,211,153,0.1);
            border: 1px solid rgba(52,211,153,0.35);
            border-radius: 999px; padding: 4px 14px;
            font-size: 0.72rem; font-family: 'DM Mono', monospace;
            color: #34d399;
            animation: badgePop .4s cubic-bezier(.34,1.56,.64,1) both;
        }}
        .lp-badge-dot {{
            width: 6px; height: 6px; border-radius: 50%;
            background: #34d399;
            animation: dotPing 1.8s ease infinite;
            box-shadow: 0 0 0 0 rgba(52,211,153,0.5);
        }}
        @keyframes dotPing {{
            0%   {{ box-shadow: 0 0 0 0 rgba(52,211,153,0.7); }}
            70%  {{ box-shadow: 0 0 0 7px rgba(52,211,153,0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(52,211,153,0); }}
        }}
        .lp-song  {{ font-family: 'Bebas Neue',sans-serif; font-size:1.5rem; letter-spacing:.05em;
                     color:var(--text) !important; animation: textGlow 3s ease-in-out infinite; }}
        .lp-artist {{ font-size:.8rem; color:var(--muted) !important; font-family:'DM Mono',monospace; }}
        .lp-wrap {{
            background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(219,39,119,0.08));
            border: 1px solid rgba(124,58,237,0.3); border-radius: 20px;
            padding: 1.3rem 1.6rem; margin-bottom: 2rem;
            display: flex; align-items: center; gap: 1.2rem;
            position: relative; overflow: hidden;
            animation: lastPlayedSlideIn 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
        }}
        .lp-wrap::before {{
            content:''; position:absolute; left:0; top:0; bottom:0; width:4px;
            background: linear-gradient(180deg,#a78bfa,#f472b6,#22d3ee);
            border-radius: 0 4px 4px 0;
        }}
        </style>
        <div class="lp-wrap">
            <div class="lp-ring">🎵</div>
            <div style="margin-left:.4rem;">
                <div class="lp-song">{st.session_state.current_song_title}</div>
                <div class="lp-artist">{st.session_state.current_song_artist}</div>
            </div>
            <div style="margin-left:auto;">
                <div class="lp-badge"><div class="lp-badge-dot"></div>last played</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if not summary_df.empty:
        st.markdown("<div class='section-tag' style='margin-top:1.5rem;'>// your top tracks</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>most <span class='grad'>played</span></div>", unsafe_allow_html=True)
        st.dataframe(summary_df.head(5), use_container_width=True)


def page_browse_songs():
    if not require_user(): return

    render_star_burst_if_pending()

    if st.session_state.get("show_mascot_for"):
        render_dancing_mascot(st.session_state.show_mascot_for)
        st.session_state.show_mascot_for = None

    st.markdown("<div class='section-tag'>// explore music</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>song <span class='grad'>discover</span></div>", unsafe_allow_html=True)

    tracks_df = load_tracks()
    if tracks_df.empty:
        st.info("no tracks found."); return

    st.markdown("<div class='discover-toolbar'>", unsafe_allow_html=True)
    c1, c2 = st.columns([2,1])
    with c1:
        search = st.text_input("search", placeholder="🔍 search by title, artist or genre…", label_visibility="collapsed")
    with c2:
        all_genres = set()
        for val in tracks_df["genre_name"].dropna():
            for g in val.split(","):
                all_genres.add(g.strip())
        genre_options  = ["all genres"] + sorted(all_genres)
        selected_genre = st.selectbox("genre", genre_options, label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    df = tracks_df.copy()
    if search.strip():
        mask = (
            df["title"].str.contains(search.strip(), case=False, na=False) |
            df["artist_name"].str.contains(search.strip(), case=False, na=False) |
            df["genre_name"].str.contains(search.strip(), case=False, na=False)
        )
        df = df[mask]
    if selected_genre != "all genres":
        df = df[df["genre_name"].str.contains(selected_genre, case=False, na=False)]

    playlists_df = load_user_playlists(st.session_state.user_id)
    playlist_map = {row["playlist_name"]: int(row["playlist_id"]) for _, row in playlists_df.iterrows()} if not playlists_df.empty else {}

    st.markdown(
        f"<div class='discover-count'>{len(df)} tracks found</div>",
        unsafe_allow_html=True)

    for idx, (_, row) in enumerate(df.iterrows()):
        tid      = int(row["track_id"])
        has_link = pd.notna(row["Youtube_Link"]) and str(row["Youtube_Link"]).strip()
        bot_open = (st.session_state.active_bot_track_id == tid)
        comment_open = (st.session_state.comment_open_track_id == tid)
        fb_key   = f"plfb_{tid}"
        video_open = (st.session_state.video_open_track_id == tid)
        comment_count = get_comment_count(tid)

        st.markdown(f"<div class='song-card' style='animation-delay:{min(idx*0.04, 0.4):.2f}s;'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='song-num'>track {str(idx+1).zfill(2)}</div>
        <div class='song-title'>{row['title']}</div>
        <div class='song-artist'>{row['artist_name']}</div>
        <div style='margin-bottom:.8rem;'>
            <span class='pill'>{row['genre_name']}</span>
            <span class='pill cyan'>{row['year'] if pd.notna(row['year']) else 'unknown'}</span>
            <span class='pill pink'>★ {row['popularity'] if pd.notna(row['popularity']) else '—'}</span>
        </div>
        """, unsafe_allow_html=True)

        if video_open and has_link:
            st.video(row["Youtube_Link"])
        elif not has_link:
            st.markdown(
                "<div style='color:var(--muted);font-size:.76rem;font-family:DM Mono,monospace;padding:.4rem 0;'>"
                "no youtube link available</div>", unsafe_allow_html=True)

        act1, act2, act3, act4 = st.columns(4)
        with act1:
            is_current = (st.session_state.current_song_title == row["title"])
            if is_current and video_open:
                if st.button("⏹ stop", key=f"play_{tid}"):
                    st.session_state.video_open_track_id = None
                    st.session_state.current_song_title  = None
                    st.session_state.current_song_artist = None
                    st.session_state.current_song_genre  = None
                    st.session_state.current_song_link   = None
                    st.rerun()
            else:
                if st.button("▶ play", key=f"play_{tid}"):
                    ok, _ = play_song(st.session_state.user_id, tid)
                    if ok:
                        st.session_state.current_song_title  = row["title"]
                        st.session_state.current_song_artist = row["artist_name"]
                        st.session_state.current_song_genre  = row["genre_name"]
                        st.session_state.current_song_link   = row["Youtube_Link"] if has_link else None
                        st.session_state.video_open_track_id = tid if has_link else None
                        st.session_state.active_bot_track_id = tid
                        st.session_state.bot_messages[str(tid)] = [("ai", bot_intro(row["title"], row["artist_name"], row["genre_name"]))]
                        st.session_state.playlist_feedback   = {}
                        st.rerun()

        with act2:
            if playlist_map:
                chosen = st.selectbox("playlist", list(playlist_map.keys()), key=f"pl_{tid}", label_visibility="collapsed")
                if st.button("+ add to playlist", key=f"add_{tid}"):
                    ok, kind, msg = add_song_to_playlist(playlist_map[chosen], tid)
                    st.session_state.playlist_feedback[fb_key] = (kind, msg)
                    if ok:
                        st.session_state.show_mascot_for = row["title"]
                    st.rerun()
            else:
                st.markdown(
                    "<div style='color:var(--muted);font-size:.76rem;padding-top:8px;"
                    "font-family:DM Mono,monospace;'>create a playlist first</div>",
                    unsafe_allow_html=True)

        with act3:
            bot_label = "🤖 hide ai" if bot_open else "🤖 ask ai"
            if st.button(bot_label, key=f"bot_toggle_{tid}"):
                if bot_open:
                    st.session_state.active_bot_track_id = None
                else:
                    st.session_state.active_bot_track_id = tid
                    msgs_key = str(tid)
                    if msgs_key not in st.session_state.bot_messages or not st.session_state.bot_messages[msgs_key]:
                        st.session_state.bot_messages[msgs_key] = [("ai", bot_intro(row["title"], row["artist_name"], row["genre_name"]))]
                st.rerun()

        with act4:
            cmt_label = f"💬 hide ({comment_count})" if comment_open else f"💬 comments ({comment_count})"
            if st.button(cmt_label, key=f"cmt_toggle_{tid}"):
                if comment_open:
                    st.session_state.comment_open_track_id = None
                else:
                    st.session_state.comment_open_track_id = tid
                st.rerun()

        if fb_key in st.session_state.playlist_feedback:
            kind, msg = st.session_state.playlist_feedback[fb_key]
            show_feedback(kind, msg)

        st.markdown("""
        <div style='margin-top:1rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.06);'>
            <div style='font-size:.68rem;color:var(--muted);text-transform:uppercase;
                        letter-spacing:.14em;margin-bottom:.5rem;font-family:DM Mono,monospace;'>
                rate this track
            </div>
        </div>
        """, unsafe_allow_html=True)
        render_star_rating(tid)

        if bot_open:
            render_inline_bot(tid, row["title"], row["artist_name"], row["genre_name"])

        if comment_open:
            render_comment_section(tid, row["title"])

        st.markdown("</div>", unsafe_allow_html=True)


def page_recommendations():
    if not require_user(): return

    st.markdown("<div class='section-tag'>// personalised for you</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>your <span class='grad'>for you</span> picks</div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='color:var(--muted);font-size:.84rem;font-family:DM Mono,monospace;margin-bottom:1.5rem;'>"
        "based on your listening history · audio features · ratings</div>",
        unsafe_allow_html=True)

    if st.session_state.get("video_modal_url"):
        render_video_modal()

    col_gen, col_n, _ = st.columns([2, 1, 3])
    with col_n:
        top_n = st.number_input("how many?", min_value=5, max_value=50, value=10, step=5, label_visibility="collapsed")
    with col_gen:
        if st.button("✨ generate fresh recommendations", key="gen_recs"):
            with st.spinner("cooking up your vibe…"):
                ok, msg = generate_recommendations(st.session_state.user_id, int(top_n))
            if ok:
                show_feedback("success", msg)
                st.rerun()
            else:
                show_feedback("error", msg)

    recs_df = load_recommendations(st.session_state.user_id)

    if recs_df.empty:
        st.markdown("""
        <div style='background:rgba(124,58,237,0.06);border:1px solid rgba(124,58,237,0.2);
                    border-radius:20px;padding:2.5rem;text-align:center;margin-top:1.5rem;'>
            <div style='font-size:3rem;margin-bottom:1rem;'>🎧</div>
            <div style='font-family:Bebas Neue,sans-serif;font-size:1.8rem;letter-spacing:.04em;margin-bottom:.5rem;'>
                no recs yet bestie
            </div>
            <div style='color:var(--muted);font-size:.84rem;font-family:DM Mono,monospace;line-height:1.6;'>
                play some songs in discover first, then hit generate to get your personalised picks
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(
        f"<div style='color:var(--muted);font-size:.74rem;font-family:DM Mono,monospace;"
        f"letter-spacing:.08em;margin-bottom:1.2rem;'>{len(recs_df)} tracks recommended · "
        f"generated {str(recs_df['generated_at'].iloc[0])[:16] if not recs_df.empty else ''}</div>",
        unsafe_allow_html=True)

    playlists_df = load_user_playlists(st.session_state.user_id)
    playlist_map = {row["playlist_name"]: int(row["playlist_id"]) for _, row in playlists_df.iterrows()} if not playlists_df.empty else {}

    for idx, (_, row) in enumerate(recs_df.iterrows()):
        tid = int(row["track_id"])
        score = float(row["recommendation_score"])
        score_pct = int(score * 100)
        has_link = pd.notna(row.get("Youtube_Link")) and str(row.get("Youtube_Link","")).strip()
        fb_key = f"recfb_{tid}"
        is_open = st.session_state.get("video_open_track_id") == tid and st.session_state.get("video_modal_url")

        if score >= 0.75:
            score_color = "#34d399"
        elif score >= 0.5:
            score_color = "#a78bfa"
        else:
            score_color = "#f472b6"

        st.markdown(f"""
        <div class='rec-card' style='animation-delay:{min(idx*0.05, 0.5):.2f}s;'>
            <div style='display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;'>
                <div style='flex:1;'>
                    <div style='font-size:.65rem;color:var(--muted);font-family:DM Mono,monospace;
                                letter-spacing:.1em;margin-bottom:.3rem;'>rec #{str(idx+1).zfill(2)}</div>
                    <div style='font-family:Bebas Neue,sans-serif;font-size:1.5rem;letter-spacing:.04em;
                                color:var(--text);margin-bottom:.2rem;'>{row['title']}</div>
                    <div style='font-size:.8rem;color:var(--muted);font-family:DM Mono,monospace;
                                margin-bottom:.6rem;'>{row['artist_name']}</div>
                    <div>
                        <span class='pill'>{row['genre_name']}</span>
                    </div>
                </div>
                <div style='text-align:right;flex-shrink:0;'>
                    <div style='font-family:Bebas Neue,sans-serif;font-size:2.2rem;
                                color:{score_color};line-height:1;'>{score_pct}%</div>
                    <div style='font-size:.66rem;color:var(--muted);font-family:DM Mono,monospace;
                                letter-spacing:.1em;'>match score</div>
                </div>
            </div>
            <div class='rec-score-bar' style='width:{score_pct}%;'></div>
        </div>
        """, unsafe_allow_html=True)

        left, right = st.columns([1.3, 2.2])
        with left:
            watch_label = "✕ close" if is_open else "▶ watch"
            if has_link and st.button(watch_label, key=f"recwatch_{tid}"):
                if is_open:
                    close_video_modal()
                else:
                    open_video_modal(tid, row["title"], row["artist_name"], row["Youtube_Link"])
                st.rerun()
            elif not has_link:
                st.markdown(
                    "<div style='color:var(--muted);font-size:.76rem;padding-top:8px;font-family:DM Mono,monospace;'>no preview available</div>",
                    unsafe_allow_html=True)

        with right:
            if playlist_map:
                sel_col, add_col = st.columns([1.25, 1])
                with sel_col:
                    chosen = st.selectbox("playlist", list(playlist_map.keys()), key=f"recpl_{tid}", label_visibility="collapsed")
                with add_col:
                    if st.button("+ add to playlist", key=f"recadd_{tid}"):
                        ok, kind, msg = add_song_to_playlist(playlist_map[chosen], tid)
                        st.session_state.playlist_feedback[fb_key] = (kind, msg)
                        if ok:
                            st.session_state.show_mascot_for = row["title"]
                        st.rerun()
            else:
                st.markdown(
                    "<div style='color:var(--muted);font-size:.76rem;padding-top:8px;font-family:DM Mono,monospace;'>create a playlist first</div>",
                    unsafe_allow_html=True)

        if fb_key in st.session_state.playlist_feedback:
            kind, msg = st.session_state.playlist_feedback[fb_key]
            show_feedback(kind, msg)

        st.markdown("<div style='margin-bottom:.5rem;'></div>", unsafe_allow_html=True)


def page_my_playlists():
    if not require_user(): return

    st.markdown("<div class='section-tag'>// your music</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>your <span class='grad'>playlists</span></div>", unsafe_allow_html=True)

    with st.form("playlist_form"):
        st.markdown("<div style='color:#f5f1ff;font-family:DM Mono,monospace;font-size:.8rem;margin-bottom:.35rem;letter-spacing:.08em;'>playlist name</div>", unsafe_allow_html=True)
        name = st.text_input("playlist name", placeholder="name your playlist…", label_visibility="collapsed")
        if st.form_submit_button("create playlist →"):
            if not name.strip():
                st.warning("give it a name first!")
            else:
                ok, msg = create_playlist(st.session_state.user_id, name.strip())
                if ok: st.success(msg); st.rerun()
                else:  st.error(msg)

    playlists_df = load_user_playlists(st.session_state.user_id)
    if playlists_df.empty:
        st.markdown(
            "<div style='color:var(--muted);font-family:DM Mono,monospace;font-size:.84rem;"
            "padding:1.5rem 0;'>no playlists yet — create one above 👆</div>",
            unsafe_allow_html=True)
        return

    for _, playlist in playlists_df.iterrows():
        pid = int(playlist["playlist_id"])
        with st.expander(f"🎵  {playlist['playlist_name']}"):
            tracks = load_playlist_tracks(pid)
            if tracks.empty:
                st.markdown(
                    "<div style='color:var(--muted);font-size:.82rem;font-family:DM Mono,monospace;'>"
                    "empty playlist — add songs from discover</div>", unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<div style='color:var(--muted);font-size:.72rem;font-family:DM Mono,monospace;"
                    f"letter-spacing:.08em;margin-bottom:.8rem;'>{len(tracks)} tracks</div>",
                    unsafe_allow_html=True)
                for _, track in tracks.iterrows():
                    tid_pl = int(track["track_id"])
                    rm_key = f"rm_{pid}_{tid_pl}"

                    col_info, col_del = st.columns([5, 1])
                    with col_info:
                        st.markdown(f"""
                        <div class='pl-track-row'>
                            <div class='pl-track-info'>
                                <div class='pl-track-title'>{track['title']}</div>
                                <div class='pl-track-artist'>{track['artist_name']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_del:
                        st.markdown("<div class='delete-btn' style='padding-top:4px;'>", unsafe_allow_html=True)
                        if st.button("🗑 remove", key=rm_key):
                            ok, msg = remove_song_from_playlist(pid, tid_pl)
                            if ok:
                                show_feedback("success", f"'{track['title']}' removed.")
                                st.rerun()
                            else:
                                show_feedback("error", msg)
                        st.markdown("</div>", unsafe_allow_html=True)


def page_my_listening():
    if not require_user(): return

    st.markdown("<div class='section-tag'>// your listening</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>play <span class='grad'>history</span></div>", unsafe_allow_html=True)

    summary_df = load_user_summary(st.session_state.user_id)
    history_df = load_user_history(st.session_state.user_id)

    st.markdown("<div style='font-family:Bebas Neue,sans-serif;font-size:1.5rem;letter-spacing:.04em;margin-bottom:.7rem;'>top tracks</div>", unsafe_allow_html=True)
    if not summary_df.empty:
        st.dataframe(summary_df, use_container_width=True)
    else:
        st.markdown("<div style='color:var(--muted);font-size:.82rem;font-family:DM Mono,monospace;'>nothing played yet</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-family:Bebas Neue,sans-serif;font-size:1.5rem;letter-spacing:.04em;margin:1.5rem 0 .7rem;'>full history</div>", unsafe_allow_html=True)
    if not history_df.empty:
        st.dataframe(history_df, use_container_width=True)
    else:
        st.markdown("<div style='color:var(--muted);font-size:.82rem;font-family:DM Mono,monospace;'>no history yet</div>", unsafe_allow_html=True)


def page_my_ratings():
    if not require_user(): return

    st.markdown("<div class='section-tag'>// your opinions matter</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>your <span class='grad'>reviews</span></div>", unsafe_allow_html=True)

    ratings_df = load_user_ratings(st.session_state.user_id)
    if not ratings_df.empty:
        st.markdown("<div style='margin-bottom:1rem;'>", unsafe_allow_html=True)
        for _, row in ratings_df.iterrows():
            rating_val = int(row["rating"])
            stars = "⭐" * rating_val + "☆" * (5 - rating_val)
            labels = {1:"mid tbh",2:"lowkey fire",3:"it slaps",4:"big banger",5:"NO SKIP 🔥"}
            lbl = labels.get(rating_val,"")
            st.markdown(f"""
            <div style='background:var(--surface2);border:1px solid var(--border);border-radius:14px;
                        padding:1rem 1.2rem;margin-bottom:.7rem;
                        transition:all .3s ease;
                        animation:cardSlideIn .4s cubic-bezier(.34,1.56,.64,1) both;'>
                <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:.4rem;'>
                    <div style='font-family:Bebas Neue,sans-serif;font-size:1.2rem;letter-spacing:.04em;'>{row['title']}</div>
                    <div style='font-size:.7rem;background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.25);
                                border-radius:999px;padding:2px 10px;color:#34d399;font-family:DM Mono,monospace;'>{lbl}</div>
                </div>
                <div style='font-size:.76rem;color:var(--muted);font-family:DM Mono,monospace;margin-bottom:.5rem;'>{row['artist_name']}</div>
                <div style='font-size:20px;letter-spacing:3px;'>{stars}</div>
                <div style='font-size:.7rem;color:var(--muted);font-family:DM Mono,monospace;margin-top:.4rem;'>
                    rated {str(row['rated_at'])[:10]} · go to discover to update your rating
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div style='color:var(--muted);font-size:.82rem;font-family:DM Mono,monospace;padding:1rem 0;'>"
            "no ratings yet — start reviewing tracks in discover ⭐</div>", unsafe_allow_html=True)


# =========================================================
# ADMIN: DASHBOARD
# =========================================================
def page_admin_dashboard():
    if not require_admin(): return

    st.markdown("<div class='section-tag'>// admin panel</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>house <span class='grad'>ledger</span></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='color:var(--muted);font-size:.82rem;font-family:DM Mono,monospace;margin-bottom:1.5rem;'>"
        f"logged in as <span style='color:#a78bfa;'>{st.session_state.admin_username}</span></div>",
        unsafe_allow_html=True)

    users_df     = load_all_users()
    tracks_df    = load_tracks()
    playlists_df = load_all_playlists()

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-tile">
            <div class="m-label">total users</div>
            <div class="m-val">{len(users_df)}</div>
        </div>
        <div class="metric-tile" style="animation-delay:.08s;">
            <div class="m-label">total tracks</div>
            <div class="m-val">{len(tracks_df)}</div>
        </div>
        <div class="metric-tile" style="animation-delay:.16s;">
            <div class="m-label">total playlists</div>
            <div class="m-val">{len(playlists_df)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='glow-divider'>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Bebas Neue,sans-serif;font-size:1.5rem;letter-spacing:.04em;margin-bottom:.7rem;'>all users</div>", unsafe_allow_html=True)
    st.dataframe(users_df, use_container_width=True)

    st.markdown("<hr class='glow-divider'>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:Bebas Neue,sans-serif;font-size:1.5rem;letter-spacing:.04em;margin-bottom:.7rem;'>all tracks</div>", unsafe_allow_html=True)
    st.dataframe(tracks_df, use_container_width=True)


# =========================================================
# ADMIN: ANALYTICS  — REBUILT WITH 4 FOCUSED CHARTS
# =========================================================
def page_admin_analytics():
    if not require_admin(): return

    st.markdown("<div class='section-tag'>// admin · insights</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>platform <span class='grad'>analytics</span></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='color:var(--muted);font-size:.82rem;font-family:DM Mono,monospace;margin-bottom:2rem;'>"
        "key metrics: catalog size · artist rankings · curation leaders · lowest rated tracks</div>",
        unsafe_allow_html=True)

    # ── ROW 1: Total Tracks (big stat) + Artist with Most Songs ──
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.markdown("""
        <div class='chart-wrap' style='text-align:center;'>
            <div class='chart-label'>// catalog size</div>
            <div class='chart-title'>Total Tracks</div>
        """, unsafe_allow_html=True)
        total_tracks = load_total_tracks_count()
        render_stat_big("tracks in catalog", total_tracks, color="#a78bfa", sub="all time")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='chart-wrap'>
            <div class='chart-label'>// artist rankings</div>
            <div class='chart-title'>Artists with Most Songs</div>
        """, unsafe_allow_html=True)
        artist_counts = load_artist_song_counts()
        if not artist_counts.empty:
            render_bar_chart(
                artist_counts["artist_name"].tolist(),
                artist_counts["song_count"].tolist(),
                "Songs per Artist",
                color_start="#7c3aed",
                color_end="#f472b6",
                height=300
            )
        else:
            st.markdown(
                "<div style='color:var(--muted);font-size:.8rem;font-family:DM Mono,monospace;'>"
                "no artist data available</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr class='glow-divider'>", unsafe_allow_html=True)

    # ── ROW 2: Users with Most Playlists ──
    st.markdown("""
    <div class='chart-wrap'>
        <div class='chart-label'>// curation leaderboard</div>
        <div class='chart-title'>Users with Most Playlists</div>
    """, unsafe_allow_html=True)
    pl_counts = load_user_playlist_counts()
    if not pl_counts.empty:
        render_bar_chart(
            pl_counts["username"].tolist(),
            pl_counts["playlist_count"].tolist(),
            "Playlists per User",
            color_start="#0891b2",
            color_end="#34d399",
            height=280
        )
    else:
        st.markdown(
            "<div style='color:var(--muted);font-size:.8rem;font-family:DM Mono,monospace;'>"
            "no playlist data yet — users need to create playlists first</div>",
            unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr class='glow-divider'>", unsafe_allow_html=True)

    # ── ROW 3: Least Rated Tracks ──
    st.markdown("""
    <div class='chart-wrap'>
        <div class='chart-label'>// quality check</div>
        <div class='chart-title'>Least Rated Tracks</div>
    """, unsafe_allow_html=True)
    least_rated = load_least_rated_tracks()
    if not least_rated.empty:
        # Bar chart of avg ratings
        labels_lr = [f"{r['title'][:16]} — {r['artist_name'][:10]}" for _, r in least_rated.iterrows()]
        vals_lr   = [float(r["avg_rating"]) for _, r in least_rated.iterrows()]
        render_bar_chart(
            labels_lr, vals_lr,
            "Least Rated Tracks",
            color_start="#ef4444",
            color_end="#f97316",
            height=300,
            max_label_len=28
        )

        # Also show a detail table
        st.markdown("<div style='margin-top:1rem;'>", unsafe_allow_html=True)
        for _, row in least_rated.iterrows():
            avg    = float(row["avg_rating"])
            cnt    = int(row["rating_count"])
            stars  = int(round(avg))
            star_s = "⭐" * stars + "☆" * (5 - stars)
            bar_w  = int(avg / 5 * 100)
            st.markdown(f"""
            <div style='margin-bottom:8px;padding:10px 14px;
                        background:rgba(239,68,68,0.05);
                        border:1px solid rgba(239,68,68,0.18);
                        border-radius:12px;'>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;'>
                    <div>
                        <span style='font-family:Bebas Neue,sans-serif;font-size:1rem;
                                     letter-spacing:.04em;color:#eeeeff;'>{row['title'][:28]}</span>
                        <span style='font-size:.68rem;color:var(--muted);
                                     font-family:DM Mono,monospace;margin-left:8px;'>{row['artist_name'][:18]}</span>
                    </div>
                    <span style='font-size:.72rem;color:#ef4444;
                                 font-family:DM Mono,monospace;'>{avg:.1f} ★ ({cnt} rating{'s' if cnt!=1 else ''})</span>
                </div>
                <div style='font-size:14px;letter-spacing:2px;margin-bottom:4px;'>{star_s}</div>
                <div style='height:4px;background:rgba(255,255,255,0.06);border-radius:4px;overflow:hidden;'>
                    <div style='height:100%;width:{bar_w}%;
                                background:linear-gradient(90deg,#ef4444,#f97316);border-radius:4px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            "<div style='color:var(--muted);font-size:.8rem;font-family:DM Mono,monospace;'>"
            "no ratings yet — users need to rate songs first</div>",
            unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# ADMIN: PLAYLISTS
# =========================================================
def page_admin_playlists():
    if not require_admin(): return

    st.markdown("<div class='section-tag'>// admin · playlist management</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>manage <span class='grad'>playlists</span></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='color:var(--muted);font-size:.82rem;font-family:DM Mono,monospace;margin-bottom:1.5rem;'>"
        "view and delete any user's playlists</div>",
        unsafe_allow_html=True)

    playlists_df = load_all_playlists()

    if playlists_df.empty:
        st.markdown(
            "<div style='color:var(--muted);font-family:DM Mono,monospace;font-size:.84rem;padding:1rem 0;'>"
            "no playlists exist yet</div>", unsafe_allow_html=True)
        return

    search_user = st.text_input("filter by username", placeholder="🔍 filter playlists by user…", label_visibility="collapsed")
    if search_user.strip():
        playlists_df = playlists_df[playlists_df["username"].str.contains(search_user.strip(), case=False, na=False)]

    st.markdown(
        f"<div style='color:var(--muted);font-size:.74rem;font-family:DM Mono,monospace;letter-spacing:.08em;margin-bottom:1rem;'>"
        f"{len(playlists_df)} playlists</div>", unsafe_allow_html=True)

    for _, pl in playlists_df.iterrows():
        pid   = int(pl["playlist_id"])
        pname = pl["playlist_name"]
        uname = pl["username"]
        tc    = int(pl["track_count"])
        cat   = str(pl["created_at"])[:10]

        col_info, col_tracks, col_del = st.columns([4, 1, 1])

        with col_info:
            st.markdown(f"""
            <div class='playlist-admin-card'>
                <div style='font-size:1.5rem;'>🎵</div>
                <div style='flex:1;'>
                    <div style='font-family:Bebas Neue,sans-serif;font-size:1.1rem;letter-spacing:.04em;color:var(--text);'>{pname}</div>
                    <div style='font-size:.74rem;color:var(--muted);font-family:DM Mono,monospace;'>
                        by <span style='color:#a78bfa;'>{uname}</span> · {tc} tracks · {cat}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_tracks:
            if st.button(f"view ({tc})", key=f"view_pl_{pid}"):
                st.session_state[f"admin_view_pl_{pid}"] = not st.session_state.get(f"admin_view_pl_{pid}", False)
                st.rerun()

        with col_del:
            st.markdown("<div class='delete-btn'>", unsafe_allow_html=True)
            if st.button("🗑 delete", key=f"del_pl_{pid}"):
                st.session_state[f"confirm_del_{pid}"] = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.get(f"confirm_del_{pid}", False):
            st.markdown(f"""
            <div style='background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.3);
                        border-radius:12px;padding:.8rem 1rem;margin:.4rem 0;
                        font-family:DM Mono,monospace;font-size:.82rem;color:#fca5a5;
                        animation:feedbackPop .3s cubic-bezier(.34,1.56,.64,1) both;'>
                ⚠ delete "<b style='color:#fff;'>{pname}</b>" by {uname}? no undo.
            </div>
            """, unsafe_allow_html=True)
            c_yes, c_no, _ = st.columns([1,1,4])
            with c_yes:
                if st.button("yes, delete", key=f"yes_del_{pid}"):
                    ok, msg = delete_playlist(pid)
                    if ok:
                        st.session_state[f"confirm_del_{pid}"] = False
                        show_feedback("success", f"'{pname}' deleted successfully.")
                        st.rerun()
                    else:
                        show_feedback("error", msg)
            with c_no:
                if st.button("cancel", key=f"no_del_{pid}"):
                    st.session_state[f"confirm_del_{pid}"] = False
                    st.rerun()

        if st.session_state.get(f"admin_view_pl_{pid}", False):
            tracks = load_playlist_tracks(pid)
            if not tracks.empty:
                st.dataframe(tracks[["title","artist_name","added_at"]], use_container_width=True)
            else:
                st.markdown(
                    "<div style='color:var(--muted);font-size:.8rem;font-family:DM Mono,monospace;padding:.4rem 0;'>empty playlist</div>",
                    unsafe_allow_html=True)

        st.markdown("<hr class='glow-divider' style='margin:0.6rem 0;'>", unsafe_allow_html=True)


# =========================================================
# ADMIN: SONG MANAGEMENT
# =========================================================
def page_admin_songs():
    if not require_admin(): return

    st.markdown("<div class='section-tag'>// admin · song management</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>manage <span class='grad'>songs</span></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='add-song-card'>
        <div class='add-song-title'>➕ Add New Song</div>
        <div class='add-song-sub'>// fill in track info + audio features · artist &amp; genre will be created if new</div>
    """, unsafe_allow_html=True)

    existing_genres_df   = load_all_genres()
    existing_genre_names = existing_genres_df["genre_name"].tolist() if not existing_genres_df.empty else []

    with st.form("add_song_form"):
        st.markdown(
            "<div style='font-family:Bebas Neue,sans-serif;font-size:1rem;letter-spacing:.04em;"
            "color:var(--neon-cyan);margin-bottom:.6rem;'>track info</div>",
            unsafe_allow_html=True)

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            new_title   = st.text_input("song title *", placeholder="Enter song title")
        with r1c2:
            new_artist  = st.text_input("artist name *", placeholder="Enter artist name")

        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1:
            new_year    = st.text_input("year", placeholder="e.g. 2023")
        with r2c2:
            new_pop     = st.number_input("popularity (0–100)", min_value=0, max_value=100, value=50)
        with r2c3:
            new_yt      = st.text_input("youtube link", placeholder="https://youtube.com/watch?v=...")

        selected_genres  = st.multiselect("existing genres", options=existing_genre_names,
                                           label_visibility="collapsed", placeholder="pick from existing genres…")
        new_genre_text   = st.text_input("new genres", placeholder="add new genres separated by commas",
                                          label_visibility="collapsed")

        st.markdown(
            "<div style='font-family:Bebas Neue,sans-serif;font-size:1rem;letter-spacing:.04em;"
            "color:var(--neon-purple);margin:.8rem 0 .4rem;'>audio features (0–100)</div>",
            unsafe_allow_html=True)

        af1, af2, af3, af4 = st.columns(4)
        with af1:
            new_energy    = st.number_input("⚡ energy", min_value=0.0, max_value=100.0, value=50.0, step=0.5)
        with af2:
            new_dance     = st.number_input("💃 danceability", min_value=0.0, max_value=100.0, value=50.0, step=0.5)
        with af3:
            new_valence   = st.number_input("😊 valence", min_value=0.0, max_value=100.0, value=50.0, step=0.5)
        with af4:
            new_acoustic  = st.number_input("🎸 acousticness", min_value=0.0, max_value=100.0, value=50.0, step=0.5)

        submit_song = st.form_submit_button("🎵 add song to catalog →")

    if submit_song:
        if not new_title.strip():
            show_feedback("error", "song title is required!")
        elif not new_artist.strip():
            show_feedback("error", "artist name is required!")
        else:
            all_genres = list(selected_genres)
            if new_genre_text.strip():
                extra = [g.strip() for g in new_genre_text.split(",") if g.strip()]
                all_genres.extend(extra)
            if not all_genres:
                all_genres = ["Unknown"]

            ok, msg, new_tid = add_new_song(
                title=new_title, artist_name=new_artist, genre_names=all_genres,
                year=new_year.strip() or None, popularity=int(new_pop),
                youtube_link=new_yt, energy=new_energy, danceability=new_dance,
                valence=new_valence, acousticness=new_acoustic
            )
            if ok:
                show_feedback("success", msg)
                st.balloons()
                st.rerun()
            else:
                show_feedback("error", f"failed to add song: {msg}")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr class='glow-divider'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='color:var(--muted);font-size:.82rem;font-family:DM Mono,monospace;margin-bottom:1.5rem;'>"
        "edit audio features, update track info, or delete songs from the catalog</div>",
        unsafe_allow_html=True)

    tracks_df = load_tracks_with_features()
    if tracks_df.empty:
        st.info("no tracks found.")
        return

    search = st.text_input("search tracks", placeholder="🔍 search by title or artist…", label_visibility="collapsed")
    if search.strip():
        mask = (
            tracks_df["title"].str.contains(search.strip(), case=False, na=False) |
            tracks_df["artist_name"].str.contains(search.strip(), case=False, na=False)
        )
        tracks_df = tracks_df[mask]

    st.markdown(
        f"<div style='color:var(--muted);font-size:.74rem;font-family:DM Mono,monospace;"
        f"letter-spacing:.08em;margin-bottom:1.2rem;'>{len(tracks_df)} tracks</div>",
        unsafe_allow_html=True)

    for idx, (_, row) in enumerate(tracks_df.iterrows()):
        tid   = int(row["track_id"])
        tname = row["title"]
        aname = row["artist_name"]

        with st.expander(f"🎵  {tname}  —  {aname}"):
            st.markdown("""
            <div style='font-family:Bebas Neue,sans-serif;font-size:1.1rem;letter-spacing:.04em;
                        margin-bottom:.8rem;color:var(--neon-purple);'>track info</div>
            """, unsafe_allow_html=True)

            ci1, ci2, ci3, ci4 = st.columns(4)
            with ci1:
                new_title_e = st.text_input("title", value=str(tname), key=f"ti_title_{tid}")
            with ci2:
                new_year_e  = st.text_input("year", value=str(int(row["year"])) if pd.notna(row["year"]) else "", key=f"ti_year_{tid}")
            with ci3:
                new_pop_e   = st.number_input("popularity (0–100)", min_value=0, max_value=100,
                                             value=int(row["popularity"]) if pd.notna(row["popularity"]) else 0,
                                             key=f"ti_pop_{tid}")
            with ci4:
                new_yt_e    = st.text_input("youtube link", value=str(row["Youtube_Link"]) if pd.notna(row["Youtube_Link"]) else "",
                                           key=f"ti_yt_{tid}")

            if st.button("💾 save track info", key=f"save_info_{tid}"):
                ok, msg = update_track_info(tid, new_title_e.strip(), new_year_e.strip() or None, int(new_pop_e), new_yt_e.strip() or None)
                if ok:
                    show_feedback("success", msg); st.rerun()
                else:
                    show_feedback("error", msg)

            st.markdown("<hr class='glow-divider' style='margin:.8rem 0;'>", unsafe_allow_html=True)
            st.markdown("""
            <div style='font-family:Bebas Neue,sans-serif;font-size:1.1rem;letter-spacing:.04em;
                        margin-bottom:.8rem;color:var(--neon-cyan);'>audio features</div>
            """, unsafe_allow_html=True)

            af1, af2, af3, af4 = st.columns(4)
            with af1:
                new_energy_e = st.number_input("energy (0–100)", min_value=0.0, max_value=100.0,
                    value=float(row["energy"]) if pd.notna(row["energy"]) else 50.0,
                    step=0.1, key=f"af_energy_{tid}")
            with af2:
                new_dance_e  = st.number_input("danceability (0–100)", min_value=0.0, max_value=100.0,
                    value=float(row["danceability"]) if pd.notna(row["danceability"]) else 50.0,
                    step=0.1, key=f"af_dance_{tid}")
            with af3:
                new_valence_e= st.number_input("valence (0–100)", min_value=0.0, max_value=100.0,
                    value=float(row["valence"]) if pd.notna(row["valence"]) else 50.0,
                    step=0.1, key=f"af_valence_{tid}")
            with af4:
                new_acoustic_e=st.number_input("acousticness (0–100)", min_value=0.0, max_value=100.0,
                    value=float(row["acousticness"]) if pd.notna(row["acousticness"]) else 50.0,
                    step=0.1, key=f"af_acoustic_{tid}")

            if st.button("🎛 save audio features", key=f"save_af_{tid}"):
                ok, msg = update_track_features(tid, new_energy_e, new_dance_e, new_valence_e, new_acoustic_e)
                if ok:
                    show_feedback("success", msg); st.rerun()
                else:
                    show_feedback("error", msg)

            st.markdown("<hr class='glow-divider' style='margin:.8rem 0;'>", unsafe_allow_html=True)
            st.markdown("""
            <div style='font-family:Bebas Neue,sans-serif;font-size:1.1rem;letter-spacing:.04em;
                        margin-bottom:.5rem;color:#fca5a5;'>danger zone</div>
            """, unsafe_allow_html=True)

            confirm_key = f"confirm_del_track_{tid}"
            st.markdown("<div class='delete-btn'>", unsafe_allow_html=True)
            if st.button(f"🗑 delete this song", key=f"del_track_btn_{tid}"):
                st.session_state[confirm_key] = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            if st.session_state.get(confirm_key, False):
                st.markdown(f"""
                <div style='background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.3);
                            border-radius:12px;padding:.8rem 1rem;margin:.4rem 0;
                            font-family:DM Mono,monospace;font-size:.82rem;color:#fca5a5;'>
                    ⚠ permanently delete <b style='color:#fff;'>"{tname}"</b>? no undo.
                </div>
                """, unsafe_allow_html=True)
                c_yes, c_no, _ = st.columns([1,1,4])
                with c_yes:
                    if st.button("yes, delete song", key=f"yes_del_track_{tid}"):
                        ok, msg = delete_track(tid)
                        if ok:
                            st.session_state[confirm_key] = False
                            show_feedback("success", f"'{tname}' deleted.")
                            st.rerun()
                        else:
                            show_feedback("error", msg)
                with c_no:
                    if st.button("cancel", key=f"no_del_track_{tid}"):
                        st.session_state[confirm_key] = False
                        st.rerun()


# =========================================================
# SQL QUERIES & INSIGHTS (ADMIN)
# =========================================================
def get_sql_query_items():
    return [
        {
            "category": "Basic",
            "question": "Display all playlists, count of tracks in each playlist, with the user who created them",
            "sql": """
                SELECT
                    p.playlist_name,
                    u.username,
                    COUNT(pt.track_id) AS track_count
                FROM playlist p
                JOIN user u ON p.user_id = u.user_id
                LEFT JOIN playlist_track pt ON p.playlist_id = pt.playlist_id
                GROUP BY p.playlist_id, p.playlist_name, u.username
                ORDER BY u.username, p.playlist_name
            """,
            "purpose": "Shows how users organize songs into playlists.",
            "insight": "Helps identify active users and playlist sizes."
        },
        {
            "category": "Basic",
            "question": "Display all genres and the total number of tracks associated with each genre",
            "sql": """
                SELECT
                    g.genre_name,
                    COUNT(tg.track_id) AS total_tracks
                FROM genre g
                LEFT JOIN track_genre tg ON g.genre_id = tg.genre_id
                GROUP BY g.genre_id, g.genre_name
                ORDER BY total_tracks DESC, g.genre_name
            """,
            "purpose": "Counts how many tracks belong to each genre.",
            "insight": "Shows the most populated genres in the catalog."
        },
        {
            "category": "Basic",
            "question": "Display all tracks released after the year 2000 along with their artist name",
            "sql": """
                SELECT
                    t.title,
                    a.artist_name,
                    t.year
                FROM track t
                JOIN artist a ON t.artist_id = a.artist_id
                WHERE t.year > 2000
                ORDER BY t.year DESC, t.title
            """,
            "purpose": "Filters tracks based on release year.",
            "insight": "Useful for analyzing newer catalog content."
        },
        {
            "category": "Basic",
            "question": "Show tracks with high energy but low acousticness",
            "sql": """
                SELECT
                    t.title,
                    a.artist_name,
                    af.energy,
                    af.acousticness
                FROM track t
                JOIN artist a ON t.artist_id = a.artist_id
                JOIN audio_features af ON t.track_id = af.track_id
                WHERE af.energy > 70 AND af.acousticness < 30
                ORDER BY af.energy DESC, af.acousticness ASC
            """,
            "purpose": "Finds intense, upbeat tracks with low acoustic feel.",
            "insight": "Useful for workout, party, or high-energy playlist analysis."
        },
        {
            "category": "Intermediate",
            "question": "Display average popularity of tracks for each genre",
            "sql": """
                SELECT
                    g.genre_name,
                    ROUND(AVG(t.popularity), 2) AS avg_popularity
                FROM genre g
                JOIN track_genre tg ON g.genre_id = tg.genre_id
                JOIN track t ON tg.track_id = t.track_id
                GROUP BY g.genre_id, g.genre_name
                ORDER BY avg_popularity DESC, g.genre_name
            """,
            "purpose": "Compares average popularity across genres.",
            "insight": "Helps identify genres that perform well overall."
        },
        {
            "category": "Intermediate",
            "question": "Show artists whose tracks have average popularity above 75",
            "sql": """
                SELECT
                    a.artist_name,
                    ROUND(AVG(t.popularity), 2) AS avg_popularity
                FROM artist a
                JOIN track t ON a.artist_id = t.artist_id
                GROUP BY a.artist_id, a.artist_name
                HAVING AVG(t.popularity) > 75
                ORDER BY avg_popularity DESC, a.artist_name
            """,
            "purpose": "Filters artists by strong average popularity.",
            "insight": "Highlights consistently popular artists."
        },
        {
            "category": "Intermediate",
            "question": "Display users who have both rated tracks and received recommendations",
            "sql": """
                SELECT DISTINCT
                    u.user_id,
                    u.username,
                    u.email
                FROM user u
                JOIN user_rating ur ON u.user_id = ur.user_id
                JOIN recommendation r ON u.user_id = r.user_id
                ORDER BY u.username
            """,
            "purpose": "Identifies highly engaged users.",
            "insight": "Shows users participating in both feedback and recommendation flows."
        },
        {
            "category": "Intermediate",
            "question": "Count tracks per artist, showing only artists with 2 or more tracks",
            "sql": """
                SELECT
                    a.artist_name,
                    COUNT(t.track_id) AS total_tracks
                FROM artist a
                JOIN track t ON a.artist_id = t.artist_id
                GROUP BY a.artist_id, a.artist_name
                HAVING COUNT(t.track_id) >= 2
                ORDER BY total_tracks DESC, a.artist_name
            """,
            "purpose": "Shows artists with meaningful catalog representation.",
            "insight": "Useful for artist-based recommendation strategies."
        },
        {
            "category": "Advanced",
            "question": "Display tracks recommended to users who have never actually listened to them",
            "sql": """
                SELECT
                    u.username,
                    t.title,
                    a.artist_name,
                    r.recommendation_score
                FROM recommendation r
                JOIN user u ON r.user_id = u.user_id
                JOIN track t ON r.track_id = t.track_id
                JOIN artist a ON t.artist_id = a.artist_id
                LEFT JOIN user_listening_history h
                    ON r.user_id = h.user_id AND r.track_id = h.track_id
                WHERE h.track_id IS NULL
                ORDER BY r.recommendation_score DESC, u.username
            """,
            "purpose": "Finds recommended tracks users have not explored yet.",
            "insight": "Helps evaluate recommendation effectiveness."
        },
        {
            "category": "Advanced",
            "question": "Show the highest recommendation score track for each user using ROW_NUMBER()",
            "sql": """
                SELECT username, title, artist_name, recommendation_score
                FROM (
                    SELECT
                        u.username,
                        t.title,
                        a.artist_name,
                        r.recommendation_score,
                        ROW_NUMBER() OVER (
                            PARTITION BY r.user_id
                            ORDER BY r.recommendation_score DESC, r.generated_at DESC
                        ) AS rn
                    FROM recommendation r
                    JOIN user u ON r.user_id = u.user_id
                    JOIN track t ON r.track_id = t.track_id
                    JOIN artist a ON t.artist_id = a.artist_id
                ) ranked
                WHERE rn = 1
                ORDER BY username
            """,
            "purpose": "Returns the single strongest recommendation per user.",
            "insight": "Useful for personalization and recommendation evaluation."
        },
        {
            "category": "Views",
            "question": "Show track details with artist, genre, and popularity from the track details view",
            "sql": """
                SELECT
                    track_id,
                    title,
                    artist_name,
                    genre_name,
                    year,
                    popularity
                FROM vw_track_full_details
                ORDER BY popularity DESC, title
                LIMIT 10
            """,
            "purpose": "Uses the reusable track metadata view.",
            "insight": "Makes it easy to analyze track characteristics from one place."
        },
        {
            "category": "Stored Procedures",
            "question": "Show available stored procedures in the current database",
            "sql": """
                SELECT
                    ROUTINE_NAME,
                    ROUTINE_TYPE,
                    CREATED,
                    LAST_ALTERED
                FROM information_schema.routines
                WHERE ROUTINE_SCHEMA = DATABASE()
                  AND ROUTINE_TYPE = 'PROCEDURE'
                ORDER BY ROUTINE_NAME
            """,
            "purpose": "Lists stored procedures available in the database.",
            "insight": "Helps document procedure-based analytical features."
        },
    ]


def page_sql_queries_insights():
    if not require_admin():
        return

    st.markdown("""
    <div style='padding-top:1.4rem;margin-bottom:1.2rem;'>
        <div class='section-tag'>// admin sql lab</div>
        <div class='section-title'>SQL Queries <span class='grad'>&amp; Insights</span></div>
        <div style='color:var(--muted);font-size:.82rem;font-family:DM Mono,monospace;'>
            run admin-ready analytical questions directly from the app · filters, joins, aggregates, views, and more
        </div>
    </div>
    """, unsafe_allow_html=True)

    category = st.selectbox(
        "select query category",
        ["All", "Basic", "Intermediate", "Advanced", "Views", "Stored Procedures"],
        index=0
    )

    items = get_sql_query_items()
    filtered_items = [item for item in items if category == "All" or item["category"] == category]

    if not filtered_items:
        st.info("no queries found for the selected category.")
        return

    st.markdown(
        f"<div style='color:var(--muted);font-size:.74rem;font-family:DM Mono,monospace;letter-spacing:.08em;margin-bottom:1rem;'>showing {len(filtered_items)} item(s)</div>",
        unsafe_allow_html=True
    )

    for idx, item in enumerate(filtered_items, start=1):
        with st.expander(f"❓ {idx}. {item['question']}"):
            st.markdown(f"**Category:** {item['category']}")
            st.markdown(f"**Purpose:** {item['purpose']}")
            st.markdown(f"**Insight:** {item['insight']}")
            render_sql_block(item["sql"])

            query_key = f"{category}_{idx}"

            if st.button("▶ run query", key=f"run_sql_query_{category}_{idx}", use_container_width=True):
                st.session_state.show_query_results[query_key] = True

            if st.session_state.show_query_results.get(query_key, False):
                close_col, spacer_col = st.columns([1, 8])
                with close_col:
                    st.markdown('<div class="close-query-btn">', unsafe_allow_html=True)
                    if st.button("✕ close", key=f"close_query_{category}_{idx}", use_container_width=True):
                        st.session_state.show_query_results[query_key] = False
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

                try:
                    df = fetch_df(item["sql"])
                    if df.empty:
                        st.info("query executed successfully, but no rows were returned.")
                    else:
                        st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Error running query: {e}")


# =========================================================
# ROUTER
# =========================================================
render_nav()

PAGES = {
    "Welcome":         page_welcome,
    "Dashboard":       page_dashboard,
    "Song Parlor":     page_browse_songs,
    "My Songbooks":    page_my_playlists,
    "Listening Diary": page_my_listening,
    "Little Reviews":  page_my_ratings,
    "For You":         page_recommendations,
    "House Ledger":    page_admin_dashboard,
    "Admin Analytics": page_admin_analytics,
    "Admin Playlists": page_admin_playlists,
    "Admin Songs":     page_admin_songs,
    "SQL Queries & Insights": page_sql_queries_insights,
}

PAGES.get(st.session_state.page, page_welcome)()
