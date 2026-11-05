"""
Generate high-resolution visual assets for the VEERA presentation slides.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import numpy as np
import os

os.makedirs("presentation_assets", exist_ok=True)

# -------------------------------------------------------------
# 1. Results Accuracy & Compute Bar Chart
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)

# Accuracy subplot
splits = ['Validation Split\n(N = 954)', 'Test Benchmark\n(N = 958)']
baseline_acc = [93.61, 93.74]
finetuned_acc = [95.49, 95.82]

x = np.arange(len(splits))
w = 0.32

rects1 = ax1.bar(x - w/2, baseline_acc, w, label='Base Qwen2.5-VL-3B (Zero-Shot)', color='#94A3B8', edgecolor='#64748B', linewidth=1)
rects2 = ax1.bar(x + w/2, finetuned_acc, w, label='VEERA (LoRA Fine-Tuned)', color='#1E3A8A', edgecolor='#172554', linewidth=1)

ax1.set_ylabel('Binary QA Accuracy (%)', fontsize=11, fontweight='bold', color='#1E293B')
ax1.set_title('Answer Accuracy: Base vs. Fine-Tuned', fontsize=12, fontweight='bold', color='#0F172A', pad=12)
ax1.set_xticks(x)
ax1.set_xticklabels(splits, fontsize=10, fontweight='bold', color='#334155')
ax1.set_ylim(88, 100)
ax1.grid(axis='y', linestyle='--', alpha=0.5)
ax1.legend(loc='lower right', framealpha=0.9, fontsize=9)

for rect in rects1:
    h = rect.get_height()
    ax1.annotate(f'{h:.2f}%', xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                 fontsize=9, fontweight='bold', color='#475569')
for rect in rects2:
    h = rect.get_height()
    ax1.annotate(f'{h:.2f}%', xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                 fontsize=9, fontweight='bold', color='#1E3A8A')

# Compute / Latency subplot
methods = ['Uniform 4-Crop\n(Always Dense)', 'VEERA Dual-Stage\n(Adaptive Compute)']
compute_tokens = [5.0, 1.8]  # Relative forward passes
colors = ['#EF4444', '#0D9488']

bars = ax2.bar(methods, compute_tokens, width=0.45, color=colors, edgecolor='#334155', linewidth=1)
ax2.set_ylabel('Effective Forward Passes / Image', fontsize=11, fontweight='bold', color='#1E293B')
ax2.set_title('Compute Efficiency & Latency Reduction', fontsize=12, fontweight='bold', color='#0F172A', pad=12)
ax2.set_ylim(0, 6)
ax2.grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars:
    h = bar.get_height()
    ax2.annotate(f'{h:.1f}x\nPasses', xy=(bar.get_x() + bar.get_width()/2, h),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                 fontsize=10, fontweight='bold', color='#0F172A')

ax2.annotate('~64% Compute\nSavings', xy=(1, 1.8), xytext=(1.2, 3.5),
             arrowprops=dict(facecolor='#0D9488', shrink=0.08, width=1.5, headwidth=6),
             fontsize=10, fontweight='bold', color='#0D9488', ha='center')

plt.tight_layout()
plt.savefig('presentation_assets/results_accuracy_chart.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------
# 2. Adaptive Multi-Crop Spatial Layout Diagram
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)
ax.set_xlim(-10, 510)
ax.set_ylim(-10, 510)
ax.set_aspect('equal')
ax.axis('off')

# Full Image Canvas
full_img = Rectangle((0, 0), 500, 500, fill=True, facecolor='#F8FAFC', edgecolor='#334155', linewidth=2.5, linestyle='-')
ax.add_patch(full_img)
ax.text(250, 480, 'Full Input Image (x) [e.g. 500 x 500 px]', ha='center', va='center', fontsize=11, fontweight='bold', color='#1E293B')

# 4 Overlapping Crops
crops_def = [
    (0, 200, 300, 300, '#3B82F6', 'Crop 1: Top-Left (c1)\n[0, 0, 400, 400]'),
    (200, 200, 300, 300, '#10B981', 'Crop 2: Top-Right (c2)\n[0, 100, 400, 500]'),
    (100, 100, 300, 300, '#F59E0B', 'Crop 3: Centre ROI (c3)\n[50, 50, 450, 450]'),
    (200, 0, 300, 300, '#8B5CF6', 'Crop 4: Bottom-Right (c4)\n[100, 100, 500, 500]')
]

for x0, y0, w, h, col, lbl in crops_def:
    rect = Rectangle((x0, y0), w, h, fill=True, facecolor=col, alpha=0.18, edgecolor=col, linewidth=2, linestyle='--')
    ax.add_patch(rect)
    ax.text(x0 + w/2, y0 + h/2, lbl, ha='center', va='center', fontsize=8.5, fontweight='bold', color=col,
            bbox=dict(boxstyle="round,pad=0.3", fc="#FFFFFF", ec=col, lw=1, alpha=0.9))

# Stride annotation
ax.annotate('50% Stride Overlap across quadrants', xy=(250, 250), xytext=(250, 20),
            ha='center', fontsize=10, fontweight='bold', color='#BE123C',
            arrowprops=dict(arrowstyle="->", color='#BE123C', lw=1.5))

plt.tight_layout()
plt.savefig('presentation_assets/crop_layout_diagram.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------------------------------------------
# 3. Vision-Language Fusion & Spatial Merger Diagram
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 3.8), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 50)
ax.set_aspect('equal')
ax.axis('off')

# Stage boxes
def draw_card(x, y, w, h, title, subtitle, fc='#FFFFFF', ec='#CBD5E1', tc='#1E293B'):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.5",
                       facecolor=fc, edgecolor=ec, linewidth=1.5)
    ax.add_patch(p)
    ax.text(x + w/2, y + h*0.65, title, ha='center', va='center', fontsize=8.5, fontweight='bold', color=tc)
    ax.text(x + w/2, y + h*0.3, subtitle, ha='center', va='center', fontsize=7.5, color='#64748B')

draw_card(2, 10, 18, 30, 'Raw Patches', '14x14 px x 2 frames\nDim: [N, 1176]', fc='#EFF6FF', ec='#3B82F6', tc='#1E3A8A')
ax.annotate('', xy=(24, 25), xytext=(20.5, 25), arrowprops=dict(arrowstyle="-|>", color='#1E3A8A', lw=1.5))

draw_card(24, 10, 20, 30, 'ViT Vision Encoder', '32 Layers, 16 Heads\nDim: [N, 1280]', fc='#F0FDF4', ec='#10B981', tc='#065F46')
ax.annotate('', xy=(48, 25), xytext=(44.5, 25), arrowprops=dict(arrowstyle="-|>", color='#065F46', lw=1.5))

draw_card(48, 10, 22, 30, '2x2 Spatial Merger', '4x Token Reduction\nConcat: [N/4, 5120]\nProj -> [N/4, 2048]', fc='#FEF3C7', ec='#F59E0B', tc='#92400E')
ax.annotate('', xy=(74, 25), xytext=(70.5, 25), arrowprops=dict(arrowstyle="-|>", color='#92400E', lw=1.5))

draw_card(74, 10, 24, 30, 'Causal LLM Decoder', 'Unified Multimodal Seq\n36 Layers, GQA (16:2)\nLoRA (r=8, alpha=16)', fc='#EEF2FF', ec='#6366F1', tc='#312E81')

ax.text(50, 46, 'VEERA Vision-Language Tokenization & Spatial Merger Pipeline', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#0F172A')

plt.tight_layout()
plt.savefig('presentation_assets/fusion_mechanism_diagram.png', dpi=300, bbox_inches='tight')
plt.close()

print("All presentation visual assets successfully generated in presentation_assets/!")

