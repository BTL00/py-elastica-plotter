import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import special
import gradio as gr


# --- Mathematical functions (Euler-Bernoulli elastic line theory) ---

def JacobiAmplitude(u_, m_):
    return special.ellipj(u_, m_)[3]

def EllipticK(k_):
    return special.ellipk(k_)

def EllipticE(phi_, m_):
    return special.ellipeinc(phi_, m_)

def JacobiCN(u_, m_):
    return special.ellipj(u_, m_)[1]

def x1(s_, k, lmb):
    return (
        -s_
        + (2 / lmb) * EllipticE(JacobiAmplitude((s_ * lmb) + EllipticK(k), k), k)
        - (2 / lmb) * EllipticE(JacobiAmplitude(EllipticK(k), k), k)
    )

def x2(s_, k, lmb):
    return -2 * k / lmb * JacobiCN(EllipticK(k) + s_ * lmb, k)

def x1derr(s, k, lmb):
    return (x1(s + 0.001, k, lmb) - x1(s, k, lmb)) / 0.001

def x2derr(s, k, lmb):
    return (x2(s + 0.001, k, lmb) - x2(s, k, lmb)) / 0.001


# --- Plotting function called by Gradio ---

def plot_elastica(l, alpha_deg, m):
    k = np.sin(alpha_deg * np.pi / 360)
    lmb = 2 * m * EllipticK(k)
    s = np.arange(0, l, 1e-4)

    x1s = x1(s, k, lmb)
    x2s = x2(s, k, lmb)

    # Smooth numerical discontinuities
    for n in range(1, len(x1s) - 2):
        if np.absolute(x1s[n + 1] - x1s[n]) > np.absolute(x1s[n + 2] - x1s[n]) * 2:
            x1s[n + 1] = x1s[n]

    x2derrs = x2derr(s, k, lmb)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.set_title("Elastica curve")
    ax1.set_xlabel("x1")
    ax1.set_ylabel("x2")
    ax1.plot(x1s, x2s)
    ax1.set_aspect('equal', adjustable='datalim')
    ax1.grid(True)

    ax2.set_title("x2 derivative")
    ax2.set_xlabel("s")
    ax2.set_ylabel("dx2/ds")
    ax2.plot(s, x2derrs)
    ax2.grid(True)

    fig.tight_layout()
    return fig


# --- Gradio UI ---

with gr.Blocks(title="Elastica Plotter") as demo:
    gr.Markdown(
        "# Elastica Plotter\n"
        "Open-source deflection curve plotter based on Leonhard Euler and Jakob Bernoulli theory for elastic lines."
    )

    with gr.Row():
        l_slider = gr.Slider(minimum=0.1, maximum=1.0, step=0.1, value=1.0, label="l  [0.1 : 1.0]")
        alpha_slider = gr.Slider(minimum=0, maximum=180, step=1, value=135, label="alpha  [0 : 180]  (degrees)")
        m_slider = gr.Slider(minimum=1, maximum=4, step=1, value=2, label="m  [1 : 4]")

    plot_output = gr.Plot()

    inputs = [l_slider, alpha_slider, m_slider]

    for slider in inputs:
        slider.change(fn=plot_elastica, inputs=inputs, outputs=plot_output)

    demo.load(fn=plot_elastica, inputs=inputs, outputs=plot_output)


if __name__ == "__main__":
    demo.launch()
