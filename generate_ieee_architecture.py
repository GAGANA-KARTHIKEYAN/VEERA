"""
VEERA IEEE Architecture Diagram — Matplotlib-based renderer.
Produces publication-quality SVG, PDF, and 300-DPI PNG with full color support.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# ─── colour palette ───────────────────────────────────────────────
C_BG       = "#FFFFFF"
C_NAVY     = "#1E3A8A"   # global / VLM accent
C_TEAL     = "#0D7377"   # adaptive stage accent
C_AMBER    = "#92400E"   # decision gate border
C_AMBER_BG = "#FEF3C7"   # decision gate fill
C_GREEN    = "#047857"   # pass / consensus
C_GREEN_BG = "#D1FAE5"
C_RED      = "#BE123C"   # abstention
C_RED_BG   = "#FFE4E6"
C_DARK     = "#1E293B"   # text / arrows
C_GRAY     = "#64748B"   # muted text
C_LGRAY    = "#F1F5F9"   # box header fills
C_BORDER   = "#94A3B8"   # neutral border
C_WHITE    = "#FFFFFF"
C_VLM_BG   = "#EFF6FF"   # light blue VLM background
C_TEAL_BG  = "#F0FDFA"   # light teal for adaptive boxes
C_TEAL_LT  = "#CCFBF1"   # teal header bar
C_OUT_BG   = "#F8FAFC"

# ─── figure setup ─────────────────────────────────────────────────
# IEEE single column: 3.5 in wide.  We use a tall aspect for the flow.
FIG_W = 3.5
FIG_H = 7.6
DPI   = 300

fig, ax = plt.subplots(1, 1, figsize=(FIG_W, FIG_H), dpi=DPI)
ax.set_xlim(0, 100)
ax.set_ylim(0, 210)
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor(C_BG)
ax.set_facecolor(C_BG)

# ─── helper functions ─────────────────────────────────────────────
def box(x, y, w, h, fc=C_WHITE, ec=C_BORDER, lw=0.8, zorder=2, rounding=0.4):
    """Draw a rounded rectangle. (x, y) is bottom-left in data coords."""
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rounding}",
                       facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder,
                       transform=ax.transData, clip_on=False)
    ax.add_patch(p)
    return p

def txt(x, y, s, size=5.5, color=C_DARK, weight="normal", ha="left", va="center",
        family="sans-serif", style="normal", zorder=5):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, fontfamily=family, fontstyle=style,
            zorder=zorder, clip_on=False)

def arrow(x1, y1, x2, y2, color=C_DARK, lw=0.7, style="-|>", head_w=3, head_l=2.5,
          zorder=3, linestyle="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=f"{style},head_width={head_w/20},head_length={head_l/20}",
                                color=color, lw=lw, linestyle=linestyle),
                zorder=zorder)

def hline(x1, y1, x2, y2, color=C_DARK, lw=0.7, ls="-", zorder=3):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, ls=ls, zorder=zorder, clip_on=False)

# ─── coordinate system (top=210, bottom=0) ────────────────────────
# We work top-down, so higher y = higher on figure.

# ═══════════════════════════════════════════════════════════════════
# A. INPUT BOXES
# ═══════════════════════════════════════════════════════════════════
Y_IN = 198
box(3, Y_IN, 44, 10, fc=C_LGRAY, ec=C_BORDER, lw=0.7)
txt(5, Y_IN+7.5, "INPUT IMAGE (x)", size=5, weight="bold", color=C_NAVY)
txt(5, Y_IN+4.5, "RGB image, arbitrary size", size=4, color=C_GRAY)
txt(5, Y_IN+2, "SmartResize preprocessing", size=3.5, color=C_GRAY)

box(53, Y_IN, 44, 10, fc=C_LGRAY, ec=C_BORDER, lw=0.7)
txt(55, Y_IN+7.5, "BINARY QUESTION (q)", size=5, weight="bold", color=C_NAVY)
txt(55, Y_IN+4.5, '"Is there a [target]?"', size=4, color=C_GRAY, style="italic")
txt(55, Y_IN+2, "Natural language binary query", size=3.5, color=C_GRAY)

# Merge arrows into VLM
arrow(25, Y_IN, 25, Y_IN-3, color=C_DARK, lw=0.6)
arrow(75, Y_IN, 75, Y_IN-3, color=C_DARK, lw=0.6)
hline(25, Y_IN-3, 75, Y_IN-3, color=C_DARK, lw=0.6)
arrow(50, Y_IN-3, 50, Y_IN-5, color=C_DARK, lw=0.6)

# ═══════════════════════════════════════════════════════════════════
# B. SHARED VLM CORE
# ═══════════════════════════════════════════════════════════════════
Y_VLM = 176
box(3, Y_VLM, 94, 15, fc=C_VLM_BG, ec=C_NAVY, lw=1.0)
# header bar
box(3, Y_VLM+12.5, 94, 2.5, fc=C_NAVY, ec=C_NAVY, lw=0.5, rounding=0.2)
txt(50, Y_VLM+13.7, "SHARED VISION-LANGUAGE MODEL CORE", size=4.5, weight="bold",
    color=C_WHITE, ha="center")

# inner sub-boxes
box(5, Y_VLM+1.5, 43, 9.5, fc=C_WHITE, ec=C_BORDER, lw=0.5, rounding=0.3)
txt(7, Y_VLM+9, "Qwen2.5-VL-3B-Instruct", size=4.2, weight="bold", color=C_DARK)
txt(7, Y_VLM+6.5, "Pre-trained vision encoder", size=3.5, color=C_GRAY)
txt(7, Y_VLM+4.5, "+ 36-layer LLM decoder", size=3.5, color=C_GRAY)
txt(7, Y_VLM+2.5, "Autoregressive generation", size=3.5, color=C_GRAY)

box(52, Y_VLM+1.5, 43, 9.5, fc=C_WHITE, ec=C_BORDER, lw=0.5, rounding=0.3)
txt(54, Y_VLM+9, "LoRA Adapter (Fine-Tuned)", size=4.2, weight="bold", color=C_DARK)
txt(54, Y_VLM+6.5, "Rank r = 8,  Scaling \u03b1 = 16", size=3.5, color=C_GRAY)
txt(54, Y_VLM+4.5, "Dropout = 0.05", size=3.5, color=C_GRAY)
txt(54, Y_VLM+2.5, "q_proj, k_proj, v_proj, o_proj", size=3.5, color=C_GRAY)

# ─── arrow down to Stage 1 ─────
arrow(50, Y_VLM, 50, Y_VLM-3.5, color=C_DARK, lw=0.6)
txt(52, Y_VLM-1.5, "[1] Global Pass", size=3.2, color=C_GRAY)

# ═══════════════════════════════════════════════════════════════════
# C. STAGE 1: GLOBAL INFERENCE & RELIABILITY
# ═══════════════════════════════════════════════════════════════════
Y_S1 = 150
box(3, Y_S1, 94, 21, fc=C_WHITE, ec=C_BORDER, lw=0.8)
# header
box(3, Y_S1+18.5, 94, 2.5, fc=C_LGRAY, ec=C_BORDER, lw=0.5, rounding=0.2)
txt(5, Y_S1+19.7, "STAGE 1: GLOBAL INFERENCE & RELIABILITY ESTIMATION",
    size=4.2, weight="bold", color=C_NAVY)

txt(5, Y_S1+16.5, "\u2022 Full-image forward pass (chat template formatted)", size=3.8, color=C_DARK)
txt(5, Y_S1+14,   "\u2022 Extract logits at prompt boundary [0, \u22121]", size=3.8, color=C_DARK)
txt(5, Y_S1+11.5, "\u2022 Softmax over Token 9454 (\u2018Yes\u2019) & 2753 (\u2018No\u2019)", size=3.8, color=C_DARK)

# formula box
box(5, Y_S1+1.5, 90, 7.5, fc="#FAFBFF", ec="#CBD5E1", lw=0.6, rounding=0.2)
txt(8, Y_S1+7, "Empirical Reliability Gap:", size=4, weight="bold", color=C_DARK)
txt(8, Y_S1+4, "G(x, q) = |P(Yes) \u2212 P(No)|", size=5, weight="bold",
    color=C_DARK, family="serif", style="italic")
txt(55, Y_S1+4, "\u2208  [0.0, 1.0]", size=4, color=C_GRAY, family="serif")

# arrow down
arrow(50, Y_S1, 50, Y_S1-3.5, color=C_DARK, lw=0.6)

# ═══════════════════════════════════════════════════════════════════
# D. SUFFICIENCY GATE (DIAMOND)
# ═══════════════════════════════════════════════════════════════════
Y_GATE = 138.5
# Diamond using polygon
diamond_x = [50, 10, 50, 90, 50]
diamond_y = [Y_GATE+6, Y_GATE, Y_GATE-6, Y_GATE, Y_GATE+6]
ax.fill(diamond_x, diamond_y, fc=C_AMBER_BG, ec=C_AMBER, lw=1.0, zorder=2)
txt(50, Y_GATE+2, "SUFFICIENCY GATE", size=4.2, weight="bold", color=C_AMBER, ha="center")
txt(50, Y_GATE-0.5, "G(x, q) \u2265 \u03c4 ?", size=4.5, weight="bold",
    color=C_AMBER, ha="center", family="serif", style="italic")
txt(50, Y_GATE-2.8, "\u03c4 = 0.7853", size=3.5, color=C_AMBER, ha="center",
    family="serif", style="italic")

# ═══ YES branch (left — fast direct path) ═══
hline(10, Y_GATE, 2, Y_GATE, color=C_NAVY, lw=0.8)
# YES label
box(1.5, Y_GATE+1.5, 12, 3, fc="#EFF6FF", ec=C_NAVY, lw=0.5, rounding=0.2)
txt(3.5, Y_GATE+3, "YES", size=3.8, weight="bold", color=C_NAVY)
txt(3.5, Y_GATE+1.8, "G \u2265 \u03c4", size=3, color=C_NAVY, family="serif")

# vertical line down left side
hline(2, Y_GATE, 2, 20, color=C_NAVY, lw=0.8, ls=(0,(4,2)))
# arrow into final output
arrow(2, 20, 3, 20, color=C_NAVY, lw=0.8)

# ─── Direct Path annotation ─────
box(0, Y_GATE-30, 8, 10, fc="#EFF6FF", ec=C_NAVY, lw=0.5, rounding=0.3)
txt(4, Y_GATE-23, "DIRECT", size=3.2, weight="bold", color=C_NAVY, ha="center")
txt(4, Y_GATE-25.5, "FAST", size=3.2, weight="bold", color=C_NAVY, ha="center")
txt(4, Y_GATE-28, "PATH", size=3.2, weight="bold", color=C_NAVY, ha="center")

# ═══ NO branch (downward — adaptive path) ═══
arrow(50, Y_GATE-6, 50, Y_GATE-12, color=C_DARK, lw=0.6)
# NO label
box(52, Y_GATE-10, 24, 3, fc=C_RED_BG, ec=C_RED, lw=0.5, rounding=0.2)
txt(54, Y_GATE-8.5, "NO (G < \u03c4)", size=3.5, weight="bold", color=C_RED)

# ═══════════════════════════════════════════════════════════════════
# E. STAGE 2: ADAPTIVE SPATIAL EVIDENCE ACQUISITION
# ═══════════════════════════════════════════════════════════════════
Y_S2 = 98
box(10, Y_S2, 87, 27, fc=C_TEAL_BG, ec=C_TEAL, lw=0.9)
# header
box(10, Y_S2+24.5, 87, 2.5, fc=C_TEAL, ec=C_TEAL, lw=0.5, rounding=0.2)
txt(12, Y_S2+25.7, "STAGE 2: ADAPTIVE SPATIAL EVIDENCE ACQUISITION",
    size=4.2, weight="bold", color=C_WHITE)

txt(12, Y_S2+22, "\u2022 Generate 4 overlapping crops (400\u00d7400 px, 50% stride):",
    size=3.8, color=C_DARK)

# 4 crop sub-boxes
cw, ch = 19, 7
cx = [13, 35, 57, 79]
cy = Y_S2 + 12
labels_top = ["c\u2081: Top-Left", "c\u2082: Top-Right", "c\u2083: Centre", "c\u2084: Bottom-Rt"]
labels_bot = ["400\u00d7400 px", "400\u00d7400 px", "400\u00d7400 px", "400\u00d7400 px"]
for i in range(4):
    box(cx[i], cy, cw, ch, fc=C_WHITE, ec=C_TEAL, lw=0.6, rounding=0.25)
    txt(cx[i]+1, cy+5, labels_top[i], size=3.3, weight="bold", color=C_TEAL)
    txt(cx[i]+1, cy+2.5, labels_bot[i], size=2.8, color=C_GRAY)

txt(12, Y_S2+9.5, "\u2022 Adaptive scaling for images \u2264 400 px (65% sub-quadrants)",
    size=3.6, color=C_DARK)
txt(12, Y_S2+7, "\u2022 Each crop c\u1d62 paired with original query q", size=3.6, color=C_DARK)
txt(12, Y_S2+4, "\u2022 All crops processed through shared VLM core above",
    size=3.8, weight="bold", color=C_TEAL)

# Feedback re-use arrow (right side, going up to VLM core)
hline(97, Y_S2+13, 99, Y_S2+13, color=C_TEAL, lw=0.7, ls=(0,(3,2)))
hline(99, Y_S2+13, 99, Y_VLM+8, color=C_TEAL, lw=0.7, ls=(0,(3,2)))
arrow(99, Y_VLM+8, 97, Y_VLM+8, color=C_TEAL, lw=0.7)
# label
txt(99.5, Y_VLM-7, "Re-uses", size=2.8, weight="bold", color=C_TEAL, ha="center", va="center")
txt(99.5, Y_VLM-9, "Shared", size=2.8, weight="bold", color=C_TEAL, ha="center", va="center")
txt(99.5, Y_VLM-11, "Core", size=2.8, weight="bold", color=C_TEAL, ha="center", va="center")

# arrow down
arrow(50, Y_S2, 50, Y_S2-4, color=C_DARK, lw=0.6)

# ═══════════════════════════════════════════════════════════════════
# F. REGIONAL EVIDENCE AGGREGATION
# ═══════════════════════════════════════════════════════════════════
Y_AGG = 68
box(10, Y_AGG, 87, 24, fc=C_TEAL_BG, ec=C_TEAL, lw=0.9)
# header
box(10, Y_AGG+21.5, 87, 2.5, fc=C_TEAL, ec=C_TEAL, lw=0.5, rounding=0.2)
txt(12, Y_AGG+22.7, "REGIONAL EVIDENCE AGGREGATION & GATING",
    size=4.2, weight="bold", color=C_WHITE)

txt(12, Y_AGG+19, "Three mandatory failure-aware criteria:", size=3.8, weight="bold", color=C_DARK)

# criterion boxes
for i, (lbl, desc) in enumerate([
    ("1. Consensus Quorum:", "Agreement ratio Q \u2265 75%  (\u2265 3 of 4 crops)"),
    ("2. Crop Reliability:",  "Every agreeing crop satisfies G(c\u1d62, q) \u2265 \u03c4"),
    ("3. Global Alignment:",  "Crop consensus matches global prediction direction"),
]):
    cy = Y_AGG + 13 - i*5
    box(12, cy, 83, 4.2, fc=C_WHITE, ec="#CBD5E1", lw=0.5, rounding=0.15)
    txt(14, cy+2.3, lbl, size=3.5, weight="bold", color=C_TEAL)
    txt(37, cy+2.3, desc, size=3.3, color=C_DARK)

txt(12, Y_AGG+1.5, "\u26a0 Failure on ANY criterion prevents definitive prediction",
    size=3.3, color=C_RED, weight="bold")

# Two branches from aggregation
# Left: All Met → Consensus
arrow(30, Y_AGG, 30, Y_AGG-5, color=C_GREEN, lw=0.7)
box(18, Y_AGG-3.5, 22, 2.5, fc=C_GREEN_BG, ec=C_GREEN, lw=0.5, rounding=0.2)
txt(19, Y_AGG-2.2, "ALL 3 MET", size=3, weight="bold", color=C_GREEN)

# Right: Unmet → Abstention
arrow(70, Y_AGG, 70, Y_AGG-5, color=C_RED, lw=0.7)
box(56, Y_AGG-3.5, 26, 2.5, fc=C_RED_BG, ec=C_RED, lw=0.5, rounding=0.2)
txt(57, Y_AGG-2.2, "UNMET / CONFLICT", size=3, weight="bold", color=C_RED)

# ═══════════════════════════════════════════════════════════════════
# G. OUTCOME CARDS
# ═══════════════════════════════════════════════════════════════════
Y_OUT = 44
# Consensus Verdict (Left)
box(10, Y_OUT, 37, 16, fc=C_GREEN_BG, ec=C_GREEN, lw=0.8)
box(10, Y_OUT+13.5, 37, 2.5, fc="#A7F3D0", ec=C_GREEN, lw=0.5, rounding=0.2)
txt(12, Y_OUT+14.7, "CONSENSUS VERDICT", size=3.8, weight="bold", color="#065F46")
txt(12, Y_OUT+11, "Status: 'answered'", size=3.5, weight="bold", color=C_DARK)
txt(12, Y_OUT+8.5, "Answer: { yes | no }", size=3.5, color=C_DARK)
txt(12, Y_OUT+6, "Mean G\u0304 (agree) \u2265 \u03c4", size=3.3, color=C_GRAY, family="serif")
txt(12, Y_OUT+3.5, "Verified by \u226575% crop", size=3.3, color=C_GRAY)
txt(12, Y_OUT+1.5, "quorum consensus", size=3.3, color=C_GRAY)

# Failure-Aware Abstention (Right)
box(53, Y_OUT, 37, 16, fc=C_RED_BG, ec=C_RED, lw=0.8)
box(53, Y_OUT+13.5, 37, 2.5, fc="#FECDD3", ec=C_RED, lw=0.5, rounding=0.2)
txt(55, Y_OUT+14.7, "FAILURE-AWARE ABSTENTION", size=3.5, weight="bold", color="#9F1239")
txt(55, Y_OUT+11, "Status: 'review'", size=3.5, weight="bold", color=C_DARK)
txt(55, Y_OUT+8.5, "Assessment: 'inconclusive'", size=3.5, color=C_DARK)
txt(55, Y_OUT+6, "Tied vote (2:2), weak crop,", size=3.3, color=C_GRAY)
txt(55, Y_OUT+3.5, "or global\u2013local contradiction", size=3.3, color=C_GRAY)
txt(55, Y_OUT+1.5, "\u2192 Escalated to human review", size=3.3, weight="bold", color=C_RED)

# arrows down to final output
arrow(28, Y_OUT, 28, Y_OUT-6, color=C_DARK, lw=0.6)
arrow(72, Y_OUT, 72, Y_OUT-6, color=C_DARK, lw=0.6)

# ═══════════════════════════════════════════════════════════════════
# H. FINAL OUTPUT BOX
# ═══════════════════════════════════════════════════════════════════
Y_FIN = 14
box(3, Y_FIN, 94, 22, fc=C_OUT_BG, ec=C_DARK, lw=1.0)
# header bar
box(3, Y_FIN+19.5, 94, 2.5, fc=C_DARK, ec=C_DARK, lw=0.5, rounding=0.2)
txt(50, Y_FIN+20.7, "FINAL SYSTEM OUTPUT & DIAGNOSTIC TELEMETRY",
    size=4.2, weight="bold", color=C_WHITE, ha="center")

# left block
box(5, Y_FIN+1, 44, 16.5, fc=C_WHITE, ec="#CBD5E1", lw=0.5, rounding=0.3)
txt(7, Y_FIN+15.5, "System Disposition:", size=3.8, weight="bold", color=C_DARK)
txt(7, Y_FIN+13, "\u2022 Direct confident: {Yes / No}", size=3.3, color=C_DARK)
txt(7, Y_FIN+10.5, "\u2022 Multi-crop consensus: {Yes / No}", size=3.3, color=C_DARK)
txt(7, Y_FIN+8, "\u2022 Selective abstention: {Review}", size=3.3, weight="bold", color=C_RED)
txt(7, Y_FIN+5.5, "Safe escalation to human", size=3, color=C_GRAY)
txt(7, Y_FIN+3.5, "domain expert when evidence", size=3, color=C_GRAY)
txt(7, Y_FIN+1.5, "is inconclusive", size=3, color=C_GRAY)

# right block
box(52, Y_FIN+1, 43, 16.5, fc=C_WHITE, ec="#CBD5E1", lw=0.5, rounding=0.3)
txt(54, Y_FIN+15.5, "Telemetry Payload:", size=3.8, weight="bold", color=C_DARK)
txt(54, Y_FIN+13, "\u2022 reliability_score: G \u2208 [0, 1]", size=3.1, color=C_GRAY)
txt(54, Y_FIN+11, "\u2022 crops_inspected: [0 | 4]", size=3.1, color=C_GRAY)
txt(54, Y_FIN+9, "\u2022 consensus_ratio: [0.50\u20131.00]", size=3.1, color=C_GRAY)
txt(54, Y_FIN+7, "\u2022 crop_bboxes: coordinates", size=3.1, color=C_GRAY)
txt(54, Y_FIN+5, "\u2022 latency_breakdown: (s)", size=3.1, color=C_GRAY)
txt(54, Y_FIN+3, "\u2022 evidence_history: rounds", size=3.1, color=C_GRAY)

# ═══════════════════════════════════════════════════════════════════
# Save all formats
# ═══════════════════════════════════════════════════════════════════
os.makedirs("figures", exist_ok=True)

for base_dir in [".", "figures"]:
    base = os.path.join(base_dir, "veera_ieee_architecture")

    fig.savefig(f"{base}.svg", format="svg", dpi=DPI, bbox_inches="tight",
                pad_inches=0.05, facecolor=C_BG)
    fig.savefig(f"{base}.pdf", format="pdf", dpi=DPI, bbox_inches="tight",
                pad_inches=0.05, facecolor=C_BG)
    fig.savefig(f"{base}.png", format="png", dpi=DPI, bbox_inches="tight",
                pad_inches=0.05, facecolor=C_BG)

plt.close(fig)

# Report sizes
for ext in ["svg", "pdf", "png"]:
    p = f"veera_ieee_architecture.{ext}"
    sz = os.path.getsize(p)
    print(f"{ext.upper()}: {p} — {sz:,} bytes")

from PIL import Image
im = Image.open("veera_ieee_architecture.png")
print(f"PNG dimensions: {im.width} x {im.height} px at {DPI} DPI")
print("\nDONE — All exports successful!")
