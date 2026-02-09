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


$$
\begin{aligned}
I_{\mathbb{H}; 0, \infty}^{C}(\gamma) := \frac{1}{2}\int_{0}^{\infty} (\frac{d \xi_{t}}{dt})^{2} dt.
\end{aligned}
$$


To get from this chordal setting to loops, one exploits that for a Jordan curve $\gamma$, the segment $\gamma[\epsilon, 1]$ is a chord in the simply connected domain $\hat{\mathbb{C}} \backslash \gamma[0, \epsilon]$ and then by using a limiting procedure it is possible to define the loop Loewner energy \cite{Rohde_2019}


$$
\begin{aligned}
I^{L}(\gamma) := \lim_{\epsilon \to 0} I_{\hat{\mathbb{C}} \backslash \gamma[0, \epsilon]}^{C}(\gamma[\epsilon, 1]),
\end{aligned}
$$


putting us firmly back in the setting of the opening paragraph. This can be taken one step further however. Any such Jordan curve $\gamma$ separates the extended complex plane $\hat{\mathbb{C}}$ into a bounded and unbounded component $\Omega$ and $\Omega^{*}$. Up to Möbius automorphisms, the Riemann mapping theorem gives conformal maps $f:\mathbb{H} \to \Omega$ and $g:\mathbb{H}^{*} \to \Omega^{*}$ from the upper and lower halfplanes onto these respective components. Defining the conformal welding $h = g^{-1} \circ f |_{\mathbb{R}}$ one obtains a different encoding of the geometric information of the curve. One defines the Loewner energy of a welding as that of a representative curve $\gamma_{h}$, which has $h$ as its conformal welding, namely $ I^{L}(h) := I^{L}(\gamma_{h})$. In conclusion, the Loewner energy is natural both for Jordan curves and for conformal weldings. 

For a chord in the upper halfplane to have zero Loewner energy, we must set the driving function to zero, and this gives a curve that traces out the segment $i \mathbb{R}_{+} \subset \mathbb{H}$. For loops, we end up with circles as the global minima and in the case of weldings, we get the identity welding pre- and post-composed by a Möbius map. These are the global minimizing objects for Loewner energy in their respective settings.

A very natural next step is to start putting some constraints on the set of curves or weldings being considered in the minimization. 

A problem in this vein was considered in detail by Wang and collaborators in \cite{marshall2025piecewisegeodesicjordancurves} \cite{bonk2025piecewisegeodesicjordancurves}. Let $z_{1}, \ldots, z_{n} \in \hat{\mathbb{C}}$ be $n$ distinct points and consider the set of Jordan curves passing through these points in that order. Insist furthermore that the curves are all homotopic relative to these $n$ points, denoting this class by $\mathcal{L}(z, \tau) = \mathcal{L}(z_{1}, \ldots, z_{n}, \tau)$, where $\tau$ is a representative curve within the homotopy class. As soon as $n \geq 4$, it is not assured that the points all lie on some circle, and thus we have in general that the Loewner energy of the minimizing curve, if it exists, is strictly positive. 

After establishing existence, uniqueness and some interesting geometric properties of the solution to the curve problem, Wang in 2025 \cite{wang2025optimizationproblemsloewnerenergy} considered a similar setup for weldings. Let $x_{1}, y_{1}, \ldots x_{n}, y_{n} \in \hat{\mathbb{R}}$ be $n$ pairs for which $x_{i} \neq x_{j}$, $y_{i} \neq y_{j}$ for $i \neq j$ and insist now that the welding map $h=g^{-1} \circ f |_{\mathbb{R}}$ satisfies $h(x_{k}) = y_{k}$, denoting this class by $\Phi_{x, y}$. In the same paper it is suggested that a solution should exist and be unique, but not proved. 

Some interesting comments regarding the geometry of the solution, particularly the representative curve $\gamma_{h}$ are made. There are also some hints regarding the structure of the Schwarzians $\mathcal{S}[f]$ and $\mathcal{S}[g]$ and how these should exhibit properties similar to $\mathcal{S}[f^{-1}]$ and $\mathcal{S}[g^{-1}]$ from the optimal solution to the curve problem. 

### Main results
This thesis studies the two optimization problems above, namely 


$$
\begin{aligned}
\inf_{\gamma \in \mathcal{L}(z_{1}, \ldots, z_{n}, \tau)} I^{L}(\gamma), \qquad \inf_{h \in \Phi_{x, y}} I^{L}(h),
\end{aligned}
$$


the existence and uniqueness of their solutions and the geometric properties thereof with particular emphasis on the Schwarzians of $f^{-1}$, $g^{-1}$ for the curve and $f$, $g$ for the welding. Recall the definition of the Schwarzian derivative of a holomorphic function $f$

 
$$
\begin{aligned}
\mathcal{S}[f](z)
= \frac{f'''(z)}{f'(z)} - \frac32\left(\frac{f''(z)}{f'(z)}\right)^2.
\end{aligned}
$$


Using the geometric properties of the solution curves (or the representative curve in the case of weldings), one obtains by setting $F=f^{-1}$ on $\Omega$ and $F=g^{-1}$ on $\Omega^{*}$ that $\mathcal{S}[F]$ can be extended to all of $\hat{\mathbb{C}}$ and that it has the following simple pole structure


$$
\begin{aligned}
\mathcal{S}[F](z) = \sum_{k=1}^{n} \frac{\text{Res}(\mathcal{S}[F], z_{k})}{z-z_{k}}.
\end{aligned}
$$


Similarly, for the welding, it will turn out that $\mathcal{S}[f]$ and $\mathcal{S}[g]$ can both be extended to all of $\hat{\mathbb{C}}$, albeit as different meromorphic functions, and that 


$$
\begin{aligned}
\mathcal{S}[f](z) &= \sum_{k=1}^{n} \frac{\text{Res}(\mathcal{S}[f], x_{k})}{z-x_{k}} \\
\mathcal{S}[g](z) &= \sum_{k=1}^{n} \frac{\text{Res}(\mathcal{S}[g], y_{k})}{z-y_{k}}.
\end{aligned}
$$


The main contribution of this thesis is to the understanding of the residues $\text{Res}(\mathcal{S}[F], z_{k})$, $\text{Res}(\mathcal{S}[f], x_{k})$ and $\text{Res}(\mathcal{S}[g], y_{k})$. We have the following results, the first of which was previously derived in \cite{bonk2025piecewisegeodesicjordancurves}. 

**Theorem.**

Consider the Loewner energy optimization problems for curves in $\mathcal{L}(z_{1}, ..., z_{n}; \tau)$ giving rise to optimal value and curve


$$
\begin{aligned}
I^{L}(z_{1}, ..., z_{n}) := I^{L}(\gamma^{*}).
\end{aligned}
$$


Let $F$ be the function associated to the optimal curve $\gamma^{*}$ as above. Assuming the derivative exists, we have the following formula for the residues of the Schwarzian. 


$$
\begin{aligned}
\text{Res}(\mathcal{S}[F], z_{k}) = \frac{1}{2} \partial_{z_{k}} I^{L}(z_{1}, ..., z_{n})
\end{aligned}
$$

For the welding optimization problem, we obtain: 

**Theorem.**

Consider the Loewner energy optimization problem for weldings in $\Phi_{x,y}$ with optimum 


$$
\begin{aligned}
I^{L}(x,y) := I^{L}(h^{*})
\end{aligned}
$$


Let $f$ and $g$ be the functions associated to the solution $h^{*}$. Assuming the derivatives exist, we have the following formula for the residues: 


$$
\begin{aligned}
\text{Res}(\mathcal{S}[f], x_{k}) = \frac{1}{2} \partial_{x_{k}} I^{L}(x, y)  \\
\text{Res}(\mathcal{S}[g], y_{k}) = \frac{1}{2} \partial_{y_{k}} I^{L}(x, y).
\end{aligned}
$$

To carry out the proofs we adapt a technique from Sung and Wang's work on quasiconformal deformations and how it relates to Loewner energy \cite{Sung2024}. There it is shown that the infinitesimal change of the Loewner energy of a Jordan curve exposed to application of a quasiconformal map $\omega^{t \mu}$ with Beltrami differential $\| t \mu \|_{\infty} < 1$ can be related to an integral of the Schwarzians in the following way 


$$
\begin{aligned}
\frac{d}{d t}|_{t = 0} I^{L}(\omega^{t \mu}(\gamma)) = - \frac{4}{\pi} \text{Re} \left [ \int_{\Omega} \mathcal{S}[f^{-1}](z) \mu(z)  d^{2}z + \int_{\Omega^{*}} \mathcal{S}[g^{-1}] \mu(z) d^{2}z \right ],
\end{aligned}
$$


a result that concretizes work by Takhtajan-Teo on variations of the universal Lioville action $S_{1}$, set in the context of universal Teichmüller space. \cite{takhtajan2004weilpeterssonmetricuniversalteichmuller}

The main idea to get from the variational formula \eqref{eq:variational_formula} to the results on residues \cref{thm:intro_curve_schw} \cref{thm:intro_welding_schw} is to pick a simplifying quasiconformal deformation that allows one to analyze one residue at a time. On a general level, this is facilitated by a map that moves only the point associated with that one particular residue.  


### Outline
We begin in \cref{ch:preliminaries} with the details on Loewner's equation, the Loewner transform and how this allows for the definition of Loewner energy of chords and loops as sketched in the above opening paragraphs.  

In \cref{ch:useful_background} we recap some conformal geometry, the Schwarzian derivative and some important Riemann maps that are directly used in proving the simple pole structure and extendability results in \cref{thm:intro_curve_schw} and \cref{thm:intro_welding_schw}. The class of conformal mappings are best understood as a subset of the quasiconformal maps and since quasiconformal deformation is the main ingredient in the new proof strategy for the main results, we devote them special attention. To unify the perspectives on curves and weldings, as well as use strong results on variation of Loewner energy, we also establish some Teichmüller theory. 

In \cref{ch:quasiconformal_deformation} this bears fruit, as we get to use a theorem on first variation of the universal Liouville action, a functional with close ties to the Loewner energy, to understand how infinitesimal quasiconformal deformation of curves and weldings affects their Loewner energy. This is a key step to extend the proof strategy to cover the main welding result. 

Then in \cref{ch:two_optimization_problems_of_the_loewner_energy} we present the two optimization problems presented briefly above and discuss existence and uniqueness. 

Finally in \cref{ch:residue_formulas} we put everything together and carry out the proofs of the results \cref{thm:intro_curve_schw} and \cref{thm:intro_welding_schw} using the quasiconformal deformation technique. 


\begin{comment}
  \newpage 

Consider a simple curve $\gamma$ growing in the upper half plane, starting at zero and extending towards infinity, carving out a path $\gamma[0, t]$. At any given point in time, the unoccupied space $\mathbb{H} \backslash \gamma[0, t]$ is simply connected and there is a conformal map $g_{t}:\mathbb{H}\backslash \gamma[0,t] \to \mathbb{H}$. Charles Loewner showed in [year...] [paper...] that under certain technical conditions on the growth of this curve, the map $g_{t}$ satisifes, for each fixed $z$ the following differential equation

\todo[inline]{Add Loewner reference}


$$
\begin{aligned}
\partial_{t} g_{t}(z) = \frac{2}{g_{t}(z) - \xi_{t}}.
\end{aligned}
$$


soluble in some interval $[0, \zeta(z))$, where the function in the denominator $\xi(\cdot)$ is referred to as the Loewner transform. More remarkably, it was furthermore shown that one could essentially move freely back and forth from one representation to the other, i.e. that there is a bijective correspondence between such simple curves and Loewner transform functions.

The representation in terms of the Loewner transform suddenly unlocks the possibility to define unambiguously a measure of the energy of such a curve, by considering the Dirichlet energy of the Loewner transform 


$$
\begin{aligned}
I_{\mathbb{H}; 0, \infty}^{C}(\gamma) := \frac{1}{2}\int_{0}^{\infty} (\frac{d \xi_{t}}{dt})^{2} dt.
\end{aligned}
$$


By using invariance properties of the transform that transfer over nicely to the above integral, it is possible to define the Loewner energy for curves in a simply connected domain, growing from one boundary point to another. And via a limiting procedure, it is possible to generalize the definition to the energy of a Jordan curve, i.e. a simple loop, in the extended complex plane $I^{L}(\gamma)$, a quantity that can be seen roughly as a measure of the deviation of the curve from a perfect circle. 

This can be taken one step further however. Any such Jordan curve $\gamma$ separates the extended complex plane $\hat{\mathbb{C}}$ into a bounded and unbounded component $\Omega$ and $\Omega^{*}$. Up to Möbius automorphisms, the Riemann mapping theorem gives conformal maps $f:\mathbb{H} \to \Omega$ and $g:\mathbb{H}^{*} \to \Omega^{*}$ from the upper and lower half planes onto these respective components. Defining the conformal welding $h = g^{-1} \circ f |_{\mathbb{R}}$ one obtains a different encoding of the geometric information of the curve. One defines the Loewner energy of a welding as that of a representative curve $\gamma_{h}$, which has $h$ as its conformal welding, namely $ I^{L}(h) := I^{L}(\gamma_{h})$. In conclusion, the Loewner energy is natural both for Jordan curves and for conformal weldings. 


### Goal of the thesis
This thesis studies two constrained optimization problems for the Loewner energy of curves and weldings respectively. The first of these, examined in detail by Wang and collaborators \cite{marshall2025piecewisegeodesicjordancurves} \cite{bonk2025piecewisegeodesicjordancurves} concerns Jordan curves in the extended complex plane passing through $n$ points in order and within the same relative homotopy class, denoted by $\mathcal{L}(z_{1}. \ldots, z_{n}, \tau)$. 

The second problem, introduced by Wang in \cite{wang2025optimizationproblemsloewnerenergy}, considers conformal weldings, with $n$ prescibed point assignments $x_{k} \mapsto y_{k}$, denoted by $\Phi_{x, y}$. The corresponding objectives are then 

 
$$
\begin{aligned}
\inf_{\gamma \in \mathcal{L}(z_{1}, \ldots, z_{n}, \tau)} I^{L}(\gamma), \qquad \inf_{h \in \Phi_{x, y}} I^{L}(h).
\end{aligned}
$$


The goal of this thesis is twofold. First, we want to understand existence and uniqueness properties of the solutions and secondly, study the functions $f$ and $g$ at the optimal points $\gamma^{*}$ and $h^{*}$

While the existence and uniqueness is well understood for the curve case, it was so far only suggested for the welding, see \cite{wang2025optimizationproblemsloewnerenergy}. We recap the known results and are able to derive existence of a solution to the welding problem. We are unsuccessful in our attempt at the uniqueness, but describe some approaches and lines of attack we tried. 

To make the second goal more precise, we recall the definition of the Schwarzian derivative of a holmorphic function $f$, namely 


$$
\begin{aligned}
\mathcal{S}[f](z) = \frac{f'''(z)}{f'(z)} - \frac32\left(\frac{f''(z)}{f'(z)}\right)^2.
\end{aligned}
$$


It turns out that the optimal points, i.e. the curve $\gamma^{*} \in \mathcal{L}(z_{1}, \ldots, z_{n}, \tau)$ and $h^{*} \in \Phi_{x,y}$, the Schwarzians $\mathcal{S}[f^{-1}]$, $\mathcal{S}[g^{-1}]$ (for the curve) and $\mathcal{S}[f]$, $\mathcal{S}[g]$ (for the welding) can all be extended meromorphically to all of $\hat{\mathbb{C}}$ and that all poles are simple. It is furthermore possible to derive a precise formula relating the residues at the simple poles to a first variation of the optimal Loewner energy. 

For the curve, this previously established result, which we obtain here with a new proof, takes the following compact form. 

**Theorem.**

Consider the Loewner energy optimization problems for curves in $\mathcal{L}(z_{1}, ..., z_{n}; \tau)$ giving rise to optimal value and curve


$$
\begin{aligned}
I^{L}(z_{1}, ..., z_{n}) := I^{L}(\gamma^{*}).
\end{aligned}
$$


Set $F=f^{-1}$ on $\Omega$ and $F=g^{-1}$ on $\Omega^{*}$. Then the Schwarzian $\mathcal{S}[F]$ extends to a meromorphic function on all of $\hat{\mathbb{C}}$ 


$$
\begin{aligned}
\mathcal{S}[F](z) = \sum_{k=1}^{n} \frac{\text{Res}(\mathcal{S}[F], z_{k})}{z-z_{k}}
\end{aligned}
$$


and, assuming the derivative exists, we have the following formula for the residues: 


$$
\begin{aligned}
\text{Res}(\mathcal{S}[F], z_{k}) = \frac{1}{2} \partial_{z_{k}} I^{L}(z_{1}, ..., z_{n})
\end{aligned}
$$

For the welding, we use the same proof strategy, to derive a first proof of the following.  

**Theorem.**

Consider the Loewner energy optimization problem for weldings in $\Phi_{x,y}$ with optimum 


$$
\begin{aligned}
I^{L}(x,y) := I^{L}(h^{*})
\end{aligned}
$$


and representative curve $\gamma = \gamma_{h^{*}}$.Then these Schwarzians can be extended to (two different) functions $\hat{\mathbb{C}} \to \hat{\mathbb{C}}$ 


$$
\begin{aligned}
\mathcal{S}[f](z) &= \sum_{k=1}^{n} \frac{\text{Res}(\mathcal{S}[f], x_{k})}{z-x_{k}} \\
\mathcal{S}[g](z) &= \sum_{k=1}^{n} \frac{\text{Res}(\mathcal{S}[g], y_{k})}{z-y_{k}}
\end{aligned}
$$


and, assuming the derivatives exist, we have the following formula for the residues: 


$$
\begin{aligned}
\text{Res}(\mathcal{S}[f], x_{k}) = \frac{1}{2} \partial_{x_{k}} I^{L}(x, y)  \\
\text{Res}(\mathcal{S}[g], y_{k}) = \frac{1}{2} \partial_{y_{k}} I^{L}(x, y)
\end{aligned}
$$

\end{comment}


\begin{comment}
By considering the extended complex plane as the Riemann sphere, the most immediately available example is perhaps a circle, like the equator. There are of course many circles and even larger assortment of possible simple loops, and this thesis is in large part about measuring how far off   


By considering the extended complex plane as the Riemann sphere, we can picture a very immlike the equator in an idealization of the earth. Of course there are many such circles on the surface of the sphere, and an even greater number of simple loops.  


The Loewner energy of a Jordan curve $\gamma$ in the extended complex plane $\hat{\mathbb{C}}$, denoted by $I^{L}(\gamma)$, measures roughly how far away the curve is from being a circle. Among all Jordan curves, the circles are precisely those for which the Loewner energy attains its minimum value $I^{L}(\gamma) = 0$
\end{comment} 


\begin{comment}
The next set of main results and the highlight of the thesis concern the Schwarzian derivative, defined for a holomorphic functions as 


$$
\begin{aligned}
\mathcal{S}[f](z) = \frac{f'''(z)}{f'(z)} - \frac32\left(\frac{f''(z)}{f'(z)}\right)^2.
\end{aligned}
$$


The solutions $\gamma^{*}$ and $h^{*}$ give rise to corresponding maps $f$ and $g$ and the goal is to say something about the structure of the Schwarzians $\mathcal{S}[f^{-1}], \mathcal{S}[g^{-1}]$ (for the curve) and $\mathcal{S}[f], \mathcal{S}[g]$ (for the welding). In  \cref{ch:residues} we present the two main results of this thesis, namely that all of these Schwarzians can be meromorphically extended meromorphically to all of $\hat{\mathbb{C}}$
\end{comment}


\begin{comment}
Existence and uniqueness of solutions has been established for \eqref{eq:intro_curve_min} and for \eqref{eq:intro_welding_min} it was suggested in  \cite{wang2025optimizationproblemsloewnerenergy}. We are able to derive the existence for the latter problem, and this forms the first main result of this thesis. For the uniqueness several attempts were made, and we briefly discuss the gap. 
\end{comment}


\begin{comment}
In \cref{ch:two_optimization_problems_of_the_loewner_energy} we consider two related constrained optimization problems for these energies following the work of Wang  \cite{wang2025optimizationproblemsloewnerenergy}. In the first case, treated thoroughly in work by Wang and collaborators  \cite{marshall2025piecewisegeodesicjordancurves}  \cite{bonk2025piecewisegeodesicjordancurves}, we fix $n$ points $z_{1}, \ldots, z_{n} \in \hat{\mathbb{C}}$ and insist that the Jordan curves $\gamma$ pass through these points in that order, and are all in some fixed homotopy class $[\tau]$ relative to this so called $z$-marking. We denote this class of curves $\mathcal{L}(z_{1}. \ldots, z_{n}, \tau)$ and consider  


$$
\begin{aligned}
\inf_{\gamma \in \mathcal{L}(z_{1}, \ldots, z_{n}, \tau)} I^{L}(\gamma).
\end{aligned}
$$


The second problem fixes instead $n$ pairs of real points $(x_{1}, y_{1}), \ldots (x_{n}, y_{n})$ and insists that the weldings in the class denoted by $\Phi_{x, y}$ satisfy $h(x_{k}) = y_{k} \quad k \in \{ 1, \ldots, n\}$. We then consider


$$
\begin{aligned}
\inf_{h \in \Phi_{x, y}} I^{L}(h).
\end{aligned}
$$

\end{comment}


\begin{comment}
   twofold. First we want to study two different constrained optimization problems for the Loewner energy, one within a class of curves and the other one within a class of weldings. In \cref{ch:two_optimization_problems_of_the_loewner_energy} we present these two problems, as well as existence and uniqueness of their solutions. And then, finally in \cref{ch:residue_formulas} we explain how the functions $f$ and $g$ associated with the optimal solutions have a very particular structure to their Schwarzians, and relate the residues to a first variation of the optimal Loewner energy. 
\end{comment}


\begin{comment}
There is no obvious correspondence between points $z_{1}, \ldots, z_{n}$ defining a $z$-marking and point prescriptions for the welding $(x_{1}, y_{1}), \ldots, (x_{n}, y_{n})$, meaning that running over curves in $\mathcal{L}(z_{1}, \ldots, z_{n}, \tau)$ one will encounter corresponding weldings that don't conform to point prescription, and correspondingly, running over weldings in $\Phi_{x, y}$, there is no fixed $z$-markings that all the corresponding representative curves adhere to. 
\end{comment}

\begin{comment}
The two central objects of study in this thesis are the Loewner energies on Jordan curves in the extended complex plane, and the related Loewner energy on conformal weldings respectively. Up until this point, we have emphasized the equivalence of different descriptions of the same underlying objects. It is recurring throughout the exposition above, starting with a translation from curve to Loewner transform, and from curve to welding. And while equivalent descriptions and unifying perspectives on seemingly different objects will be a recurring theme and powerful tool in what is to follow, it is important to briefly set the stage for the setting in which these two objects start to behave differently. 
\end{comment}

\begin{comment}
Thanks invariance properties of the transform that transfer over nicely to the above integral, this can then be extended to a definition of the Loewner energy for a chord growing from a boundary point $a$ to another boundary point $b$ of a simply connected domain $D$. 


One obtains the generalization to the Loewner energy of a Jordan curve in the extended complex plane by a limiting procedure, choosing a root $\gamma(0)$ and considering the chord $\gamma[\epsilon, 1]$ in the domain $\hat{\mathbb{C}} \backslash \gamma[0, \epsilon]$

   
I^{L}(\gamma) := \lim_{\epsilon \to 0} I_{\hat{\mathbb{C}} \backslash \gamma[0, \epsilon]}^{C}(\gamma[\epsilon, 1])


This quantity, the Loewner energy on Jordan curves in the extended complex plane can be seen roughly as a measure of the deviation of the curve from a perfect circle.

Any such Jordan curve $\gamma$ separates the extended complex plane $\hat{\mathbb{C}}$ into a bounded and unbounded component $\Omega$ and $\Omega^{*}$. Up to Möbius automorphisms, the Riemann mapping theorem gives conformal maps $f:\mathbb{H} \to \Omega$ and $g:\mathbb{H}^{*} \to \Omega^{*}$ from the upper and lower half planes onto these respective components. Defining the conformal welding $h = g^{-1} \circ f |_{\mathbb{R}}$ one obtains a different encoding of the geometric information of the curve. It turns out that it is possible to define the Loewner energy of a welding as that of a representative curve $\gamma_{h}$, which has $h$ as its conformal welding, namely 


I^{L}(h) := I^{L}(\gamma_{h}).
\end{comment}
