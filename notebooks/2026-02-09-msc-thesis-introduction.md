---
title: MSc thesis introduction
date: 2026-02-09
collection: Thesis
tags: thesis, msc
summary: Introduction from my MSc thesis.
---
# MSc thesis introduction

## Introduction

Consider a Jordan curve $\gamma:[0,1] \to \hat{\mathbb{C}}$ in the extended complex plane, tracing out a simple loop, i.e. starting and ending at the same point, $\gamma(0) = \gamma(1)$. One concrete visual example is the equator on the two-dimensional sphere. There are of course many other loops without self-crossing and in this thesis we study in detail some problems related to the Loewner energy of such curves, denoted $I^{L}(\gamma)$, a functional that measures roughly the deviation of such a loop from being a circle.  

Before we go into further detail regarding the specific tasks that lie ahead, it seems prudent to take a step back and examine what exactly we are measuring with Loewner energy and in what sense it is an energy. In 1923, Loewner examined families of conformal maps related to slit domains of the unit disk. \cite{Loewner1923} Translating to the conformally equivalent setting of the upper halfplane, we consider a curve $\gamma$ starting at zero and growing towards infinity. At any given point in time, it carves out a simply connected domain $H_{t} = \mathbb{H} \backslash \gamma[0, t]$ and then from the Riemann mapping theorem and a suitable normalization, we get a choice of conformal map $g_{t}:H_{t} \to \mathbb{H}$, with the expansion $g_{t}(z) = z + \frac{2t}{z} + O(|z|^{-2})$ at infinity. 

This yields a family of maps $(g_{t})_{t}$ and remarkably, these so-called mapping-out functions satisfy, for each $z$, an ODE of the form $\partial_{t} g_{t}(z) = \frac{2}{g_{t}(z) - \xi_{t}}$, a description of how the individual $z$ flow across time as the curve continues its growth towards infinity. What is more, the curve $\gamma$ is encoded by $\xi$ in the above ODE, called the Loewner driving function. In two papers from 2015 and 2016 Friz-Shekhar \cite{friz2015existencesletracefinite} and then independently Wang \cite{Wang_2019_deterministicloewnerchain} used this representation to define the chordal Loewner energy of $\gamma$ as the Dirichlet energy of the Loewner driving function, namely 


\begin{align}
I_{\mathbb{H}; 0, \infty}^{C}(\gamma) := \frac{1}{2}\int_{0}^{\infty} (\frac{d \xi_{t}}{dt})^{2} dt.
\end{align}


To get from this chordal setting to loops, one exploits that for a Jordan curve $\gamma$, the segment $\gamma[\epsilon, 1]$ is a chord in the simply connected domain $\hat{\mathbb{C}} \backslash \gamma[0, \epsilon]$ and then by using a limiting procedure it is possible to define the loop Loewner energy \cite{Rohde_2019}


\begin{align}
I^{L}(\gamma) := \lim_{\epsilon \to 0} I_{\hat{\mathbb{C}} \backslash \gamma[0, \epsilon]}^{C}(\gamma[\epsilon, 1]),
\end{align}


putting us firmly back in the setting of the opening paragraph. This can be taken one step further however. Any such Jordan curve $\gamma$ separates the extended complex plane $\hat{\mathbb{C}}$ into a bounded and unbounded component $\Omega$ and $\Omega^{*}$. Up to Möbius automorphisms, the Riemann mapping theorem gives conformal maps $f:\mathbb{H} \to \Omega$ and $g:\mathbb{H}^{*} \to \Omega^{*}$ from the upper and lower halfplanes onto these respective components. Defining the conformal welding $h = g^{-1} \circ f |_{\mathbb{R}}$ one obtains a different encoding of the geometric information of the curve. One defines the Loewner energy of a welding as that of a representative curve $\gamma_{h}$, which has $h$ as its conformal welding, namely $ I^{L}(h) := I^{L}(\gamma_{h})$. In conclusion, the Loewner energy is natural both for Jordan curves and for conformal weldings. 

For a chord in the upper halfplane to have zero Loewner energy, we must set the driving function to zero, and this gives a curve that traces out the segment $i \mathbb{R}_{+} \subset \mathbb{H}$. For loops, we end up with circles as the global minima and in the case of weldings, we get the identity welding pre- and post-composed by a Möbius map. These are the global minimizing objects for Loewner energy in their respective settings.

A very natural next step is to start putting some constraints on the set of curves or weldings being considered in the minimization. 

A problem in this vein was considered in detail by Wang and collaborators in \cite{marshall2025piecewisegeodesicjordancurves} \cite{bonk2025piecewisegeodesicjordancurves}. Let $z_{1}, \ldots, z_{n} \in \hat{\mathbb{C}}$ be $n$ distinct points and consider the set of Jordan curves passing through these points in that order. Insist furthermore that the curves are all homotopic relative to these $n$ points, denoting this class by $\mathcal{L}(z, \tau) = \mathcal{L}(z_{1}, \ldots, z_{n}, \tau)$, where $\tau$ is a representative curve within the homotopy class. As soon as $n \geq 4$, it is not assured that the points all lie on some circle, and thus we have in general that the Loewner energy of the minimizing curve, if it exists, is strictly positive. 

After establishing existence, uniqueness and some interesting geometric properties of the solution to the curve problem, Wang in 2025 \cite{wang2025optimizationproblemsloewnerenergy} considered a similar setup for weldings. Let $x_{1}, y_{1}, \ldots x_{n}, y_{n} \in \hat{\mathbb{R}}$ be $n$ pairs for which $x_{i} \neq x_{j}$, $y_{i} \neq y_{j}$ for $i \neq j$ and insist now that the welding map $h=g^{-1} \circ f |_{\mathbb{R}}$ satisfies $h(x_{k}) = y_{k}$, denoting this class by $\Phi_{x, y}$. In the same paper it is suggested that a solution should exist and be unique, but not proved. 

Some interesting comments regarding the geometry of the solution, particularly the representative curve $\gamma_{h}$ are made. There are also some hints regarding the structure of the Schwarzians $\mathcal{S}[f]$ and $\mathcal{S}[g]$ and how these should exhibit properties similar to $\mathcal{S}[f^{-1}]$ and $\mathcal{S}[g^{-1}]$ from the optimal solution to the curve problem. 

### Main results
This thesis studies the two optimization problems above, namely 


\begin{align}
\inf_{\gamma \in \mathcal{L}(z_{1}, \ldots, z_{n}, \tau)} I^{L}(\gamma), \qquad \inf_{h \in \Phi_{x, y}} I^{L}(h),
\end{align}


the existence and uniqueness of their solutions and the geometric properties thereof with particular emphasis on the Schwarzians of $f^{-1}$, $g^{-1}$ for the curve and $f$, $g$ for the welding. Recall the definition of the Schwarzian derivative of a holomorphic function $f$

 

\begin{align}
\mathcal{S}[f](z)
= \frac{f'''(z)}{f'(z)} - \frac32\left(\frac{f''(z)}{f'(z)}\right)^2.
\end{align}


Using the geometric properties of the solution curves (or the representative curve in the case of weldings), one obtains by setting $F=f^{-1}$ on $\Omega$ and $F=g^{-1}$ on $\Omega^{*}$ that $\mathcal{S}[F]$ can be extended to all of $\hat{\mathbb{C}}$ and that it has the following simple pole structure


\begin{align}
\mathcal{S}[F](z) = \sum_{k=1}^{n} \frac{\text{Res}(\mathcal{S}[F], z_{k})}{z-z_{k}}.
\end{align}


Similarly, for the welding, it will turn out that $\mathcal{S}[f]$ and $\mathcal{S}[g]$ can both be extended to all of $\hat{\mathbb{C}}$, albeit as different meromorphic functions, and that 


\begin{align}
\mathcal{S}[f](z) &= \sum_{k=1}^{n} \frac{\text{Res}(\mathcal{S}[f], x_{k})}{z-x_{k}} \\
\mathcal{S}[g](z) &= \sum_{k=1}^{n} \frac{\text{Res}(\mathcal{S}[g], y_{k})}{z-y_{k}}.
\end{align}


The main contribution of this thesis is to the understanding of the residues $\text{Res}(\mathcal{S}[F], z_{k})$, $\text{Res}(\mathcal{S}[f], x_{k})$ and $\text{Res}(\mathcal{S}[g], y_{k})$. We have the following results, the first of which was previously derived in \cite{bonk2025piecewisegeodesicjordancurves}. 

<a id="thm:intro_curve_schw"></a>

**Theorem 1.**

Consider the Loewner energy optimization problems for curves in $\mathcal{L}(z_{1}, ..., z_{n}; \tau)$ giving rise to optimal value and curve


\begin{align}
I^{L}(z_{1}, ..., z_{n}) := I^{L}(\gamma^{*}).
\end{align}


Let $F$ be the function associated to the optimal curve $\gamma^{*}$ as above. Assuming the derivative exists, we have the following formula for the residues of the Schwarzian. 


\begin{align}
\text{Res}(\mathcal{S}[F], z_{k}) = \frac{1}{2} \partial_{z_{k}} I^{L}(z_{1}, ..., z_{n})
\end{align}

For the welding optimization problem, we obtain: 

<a id="thm:intro_welding_schw"></a>

**Theorem 2.**

Consider the Loewner energy optimization problem for weldings in $\Phi_{x,y}$ with optimum 


\begin{align}
I^{L}(x,y) := I^{L}(h^{*})
\end{align}


Let $f$ and $g$ be the functions associated to the solution $h^{*}$. Assuming the derivatives exist, we have the following formula for the residues: 


\begin{align}
\text{Res}(\mathcal{S}[f], x_{k}) = \frac{1}{2} \partial_{x_{k}} I^{L}(x, y)  \\
\text{Res}(\mathcal{S}[g], y_{k}) = \frac{1}{2} \partial_{y_{k}} I^{L}(x, y).
\end{align}

To carry out the proofs we adapt a technique from Sung and Wang's work on quasiconformal deformations and how it relates to Loewner energy \cite{Sung2024}. There it is shown that the infinitesimal change of the Loewner energy of a Jordan curve exposed to application of a quasiconformal map $\omega^{t \mu}$ with Beltrami differential $\| t \mu \|_{\infty} < 1$ can be related to an integral of the Schwarzians in the following way 


\begin{align}
\label{eq:variational_formula}
\frac{d}{d t}|_{t = 0} I^{L}(\omega^{t \mu}(\gamma)) = - \frac{4}{\pi} \text{Re} \left [ \int_{\Omega} \mathcal{S}[f^{-1}](z) \mu(z)  d^{2}z + \int_{\Omega^{*}} \mathcal{S}[g^{-1}] \mu(z) d^{2}z \right ],
\end{align}


a result that concretizes work by Takhtajan-Teo on variations of the universal Lioville action $S_{1}$, set in the context of universal Teichmüller space. \cite{takhtajan2004weilpeterssonmetricuniversalteichmuller}

The main idea to get from the variational formula $\eqref{eq:variational_formula}$ to the results on residues [Theorem 1](#thm:intro_curve_schw) [Theorem 2](#thm:intro_welding_schw) is to pick a simplifying quasiconformal deformation that allows one to analyze one residue at a time. On a general level, this is facilitated by a map that moves only the point associated with that one particular residue.  


### Outline
We begin in Chapter 1 with the details on Loewner's equation, the Loewner transform and how this allows for the definition of Loewner energy of chords and loops as sketched in the above opening paragraphs.  

In Chapter 2 we recap some conformal geometry, the Schwarzian derivative and some important Riemann maps that are directly used in proving the simple pole structure and extendability results in [Theorem 1](#thm:intro_curve_schw) and [Theorem 2](#thm:intro_welding_schw). The class of conformal mappings are best understood as a subset of the quasiconformal maps and since quasiconformal deformation is the main ingredient in the new proof strategy for the main results, we devote them special attention. To unify the perspectives on curves and weldings, as well as use strong results on variation of Loewner energy, we also establish some Teichmüller theory. 

In Chapter 3 this bears fruit, as we get to use a theorem on first variation of the universal Liouville action, a functional with close ties to the Loewner energy, to understand how infinitesimal quasiconformal deformation of curves and weldings affects their Loewner energy. This is a key step to extend the proof strategy to cover the main welding result. 

Then in Chapter 4 we present the two optimization problems presented briefly above and discuss existence and uniqueness. 

Finally in Chapter 5 we put everything together and carry out the proofs of the results [Theorem 1](#thm:intro_curve_schw) and [Theorem 2](#thm:intro_welding_schw) using the quasiconformal deformation technique.

<!-- BEGIN AUTO-GENERATED REFERENCES -->

## References

1. Löwner, Karl (1923). *Untersuchungen {\"u}ber schlichte konforme Abbildungen des Einheitskreises. I*. Mathematische Annalen. DOI: `10.1007/BF01448091`. URL: `https://doi.org/10.1007/BF01448091`. Key: `Loewner1923`.
2. Peter K. Friz and Atul Shekhar (2015). *On the existence of SLE trace: finite energy drivers and non-constant $\kappa$*. URL: `https://arxiv.org/abs/1511.02670`. Key: `friz2015existencesletracefinite`.
3. Wang, Yilin (2019). *The energy of a deterministic Loewner chain: Reversibility and interpretation via SLE$_{0+}$*. Journal of the European Mathematical Society. DOI: `10.4171/jems/876`. URL: `http://dx.doi.org/10.4171/JEMS/876`. Key: `Wang_2019_deterministicloewnerchain`.
4. Rohde, Steffen and Wang, Yilin (2019). *The Loewner Energy of Loops and Regularity of Driving Functions*. International Mathematics Research Notices. DOI: `10.1093/imrn/rnz071`. URL: `http://dx.doi.org/10.1093/imrn/rnz071`. Key: `Rohde_2019`.
5. Donald Marshall and Steffen Rohde and Yilin Wang (2025). *Piecewise geodesic Jordan curves I: weldings, explicit computations, and Schwarzian derivatives*. URL: `https://arxiv.org/abs/2202.01967`. Key: `marshall2025piecewisegeodesicjordancurves`.
6. Mario Bonk and Janne Junnila and Steffen Rohde and Yilin Wang (2025). *Piecewise geodesic Jordan curves II: Loewner energy, projective structures, and accessory parameters*. URL: `https://arxiv.org/abs/2410.22275`. Key: `bonk2025piecewisegeodesicjordancurves`.
7. Yilin Wang (2025). *Two optimization problems for the Loewner energy*. URL: `https://arxiv.org/abs/2402.10054`. Key: `wang2025optimizationproblemsloewnerenergy`.
8. Jinwoo Sung and Yilin Wang (2024). *Quasiconformal deformation of the chordal Loewner driving function and first variation of the Loewner energy*. Mathematische Annalen. DOI: `10.1007/s00208-024-02866-0`. URL: `https://doi.org/10.1007/s00208-024-02866-0`. Key: `Sung2024`.
9. Leon A. Takhtajan and Lee-Peng Teo (2004). *Weil-Petersson metric on the universal Teichmuller space I: Curvature properties and Chern forms*. URL: `https://arxiv.org/abs/math/0312172`. Key: `takhtajan2004weilpeterssonmetricuniversalteichmuller`.

<!-- END AUTO-GENERATED REFERENCES -->
