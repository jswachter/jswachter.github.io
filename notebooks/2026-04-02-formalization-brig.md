---
title: Formalization workshop, Brig 2026
date: 2026-04-02
collection: Math & Formal Methods
tags: formalization, workshop, brig
---

# Formalization workshop, Brig 2026


## Introduction

Between the 25th and 27th of March UniDistance in Brig hosted a workshop on proof assistants, bringing together mathematicians and AI practitioners working on formal mathematics. The use of formal methods for the verification of mathematical proofs is in and of itself not a new development, but the use of AI to speed up this process and remove much of the tedium, is rather new however, and also promises to make the overall formalization effort more prominent. Some notable recent successes include formalization of the sphere packing problem and very strong results on the IMO and Putnam competitions, with formally verified solutions. Both the leading 'frontier' model providers and more specialized startups are playing a role, something reflected in the list of speakers.

This report gives an account of the topics discussed during the workshop, summaries and takeaways from the most interesting talks and makes some recommendations as to how KOF of ETH Zurich can approach the use of AI-augmented formal methods in its research.

## Workshop Notes

### Day 1

#### The Formal Conjectures Project
*Speaker:* Moritz Firsching.
- Started in Zurich in late 2024, and open-sourced in 2025.
- The project formalizes statements of unsolved mathematical conjectures in Lean 4.
- The source base is broad: papers, MathOverflow, the Kourovka Notebook, Tao's Optimization Constants, and collections of Erdős and Green problems all feed into the repository.
- A conjecture may later be solved in exactly the posted formalization, in Lean 4 with only minor variation, or in another proof assistant
- Why care about this project? The first reason is that it offers an interface between problems humans care enough about to have written down and AI. The second reason is that this interface can help facilitate the resolution of open problems.
- Notable examples of this latter reason are MathOverflow 486481 and Erdős problem 1082b, which have both received formally verified solutions in this way.
- Misformalization is a central difficulty and quite common, so curation matters: the project uses lightweight checks, including a custom linter. The open-source, public GitHub also facilitates discussion on open PRs, and there are plans to extend the functionality of the website, to include a comment section and the possibility to vote on the likely truth value of a conjecture.
- In the context of AI, evaluations of capabilities is an important task and as a benchmark, formal-conjectures has advantages over static sets such as MiniF2F or PutnamBench: it is growing, tied to research mathematics, and close to live mathematical practice rather than only to archived competition problems.
- With regard to voting and comment functionality proposed by the creator, I was reminded of the paper on the SPRIG protocol. It's a blockchain hosted way to direct agents working on mathematical proofs and is both interesting from a technical and economic incentives point of view. [1]
- There is also an interesting question about whether conjecturing itself can be automated, similar to the ideas laid out by Jiang of Mistral. [2]

*Sources:* [3, 4, 5, 2, 1].

#### AlphaProof: RL for Math, Gold Medals for Gemini, and Beyond
*Speaker:* Goran Zuzic.
- The first part situated AlphaProof inside a broader acceleration in AI for mathematics: AlphaTensor, AlphaGeometry, newer reasoning models such as o1, Gemini 2.0 and DeepSeek R1.
- AlphaProof itself was presented as reinforcement learning and self-play inside a strong verifier. The proving process becomes a game with tactic states as states, Lean tactics as actions, Lean events as transitions, and binary reward based on compilation of the Lean program.
- The architecture combines a transformer over pretty-printed tactic states with policy and value heads, and uses MCTS together with AND-OR search to guide proof exploration.
- Data is a bottleneck, since formal mathematics is way more scarce than its natural language counterpart. A large part of the story is synthetic curriculum building: natural-language mathematics is autoformalized, filtered by syntax and consistency checks, and expanded at scale. The gain is large, going from 1 million natural language statements to 80 million formal variants.
- Autoformalization itself is an ill-posed problem and the process itself is rather heuristic driven. No human ever checks the 80 million statements, and surely some of them are nonsense, but the interesting thing is that as training data, the recipe works incredibly well.
- The team used test tie reinforcement learning (TTRL) to make the underlying model better able to tackle the most complex formal statements. It's an interesting open question how this can be scaled to near real time.
- Via variant generation, local loops (for a specific problem) and TTRL adaptation, the system was able to solve problem 6 of the IMO (2025), previously thought to be an almost impossible level of difficulty.
- There are two main scaling laws at play: Search scaling and TTRL scaling. On the margin, the latter seems to be a more efficient allocation of compute.
- RL tends to give very non-human Lean code. Future directions include greater mathematical taste and increased capacity for theory building.
- An interesting point that featured in the question session afterwards is that of partial progress and how it interacts with binary rewards. If a human tries to learn mathematics, the overall strategy used to reach a solution is often very important and in some cases emphasized above actually getting the correct solution, so the reward is certainly not binary. The scale of training data and lack of human oversight makes it impossible to reliably administer the same partial rewards for the AI-system. Interestingly, variant generation can itself be a form of partial rewards: On average there were 80 formal statements for every natural language one, and if these 80 are generated with more or less access to the full natural language solution, that turns out to be a good proxy for rewarding partial progress, by moving this signal into the data itself.

*Sources:* [3, 6, 7, 8].

#### lean-lsp-mcp: A toolbox for agents to interact with Lean
*Speaker:* Oliver Dressler.
- If Lean users work with goals, diagnostics, syntax highlighting, documentation, and local exploration, agents should get comparable interfaces rather than only raw text prompts.
- The toolbox exposes Lean through MCP and the Language Server Protocol (same system used in VSCode), allowing agents like Codex or Claude Code access to fine-grained feedback.
- Search is a major part of that loop. Loogle, Lean State Search, and Lean Finder were highlighted as effective retrieval tools, with search functioning as a kind of outsourcing for local reasoning and recall.
- The talk also pointed to an evolution towards the use of agent skills, which is a paradigm of markdown-based instructions progressively disclosed to an agent as it tries to solve a problem.
- Having worked a great deal with MCP and Skills myself, I think there are some interesting question here around context management, disabling tools and whether the raw model will eventually do best with its built-in tools only.

*Sources:* [3, 9, 10].

### Day 3

#### First steps in formalization III: using AI
*Speaker:* David Loeffler.
- The session compared three current entry points into AI-assisted formalization: a general model used one-shot (ChatGPT), a dedicated proving agent (Aristotle by Harmonic), and a repository-level Lean coding agent (Leanstral by Mistral). Model capability and harness quality seem to be very important.
- ChatGPT looked useful as a fast baseline, but still prone to hallucinations, overengineered proofs, and weaker performance on conceptual problems.
- Harmonic's Aristotle was slower, but substantially more reliable. It could work from English or directly inside a Lean repository, and the examples discussed suggested notably shorter proofs and genuine end-to-end successes on nontrivial tasks.
- Even strong generated proofs still create editing work: nested `have` statements, awkward nonterminal steps, and several new helper lemmas can leave the human with a cleanup and restructuring problem rather than a finished Mathlib library contribution.
- It is of course very much in doubt whether a Mathlib library contribution is or will be the goal of most formalization work. It certainly is of most interest to the speaker and other mathematicians with a history of such library contributions, but from a verification point of view, the need for a canonical formalization is probably much lower.
- Leanstral was presented as a smaller but more repository-native Lean agent: weaker at raw proving, but able to read and edit files directly and sometimes producing cleaner code when it worked. I have a friend who worked closely on reinforcement learning for this model and look forward to trying it out myself.

*Sources:* [3, 11, 12, 13].

#### Formalizing the sphere packing problem in dimension 8
*Speaker:* Maryna Viazovska.
- The talk placed the project against the longer history of sphere packing: the sphere packing constant $\Delta_d$, the Cohn--Elkies linear-programming bounds, and the fact that exact optimality is known only in dimensions 1, 2, 8, and 24.
- The dimension-8 and dimension-24 cases stand out because the Cohn-Elkies upper bounds and the best known packings nearly coincide, marking them as strong candidates. The $E_8$ and Leech lattices were then proved to be optimal.
- Viazovska's breakthrough rests on the construction of a special auxiliary function, together with its Fourier transform, built from deep modular and quasimodular structure and now often described as the "magic function".
- The path to formalization was presented as a serious mathematical project in its own right: Kevin Buzzard encouraged the effort, work began with Sidharth Hariharan, and further collaborators were recruited.
- The blueprint for the project created a big dependency graph of results and supporting theory needed.
- One recurring question in the background was what formalization should optimize for once AI systems can generate large parts of the code: mere completion, deeper understanding, or some combination of the two. Maryna highlighted the (partial) need to better understand what the autoformalization agent by Math, Inc actually did in generating the proofs.

*Sources:* [3, 14, 15, 16].

#### Formalising Sphere Packing
*Speaker:* Sidharth Hariharan.
- The project was organized around a blueprint that kept changing as the mathematics and the codebase grew: Maryna's original proof, Seewoo Lee's modular-form inequalities, the broader sphere-packing narrative, and Hariharan's undergraduate formalization work on the magic function all had to be integrated into one formal development.
- The mathematical output goes well beyond the final theorem statement. The formalization built infrastructure for sphere packings as sets of centers, modular and quasimodular forms, inequalities, contour integration, and the analytic machinery around the magic function.
- There were also metaprogramming gains, including new automation for complex-number calculations and tools for atomic-limit `Tendsto` statements; formalization here was not mainly about deleting `sorry`'s, but about finding the right abstractions and understanding the proof better.
- Gauss pushed the project to a `sorry`-free proof, but that was not the end of the work in the speakers view. Review, refactoring, file reorganization, cleanup of custom definitions, and integration with human-written code remained substantial tasks. The AI-written code currently lives in its own branch and is merged in batches.
- A main lesson for human-AI collaboration was that objectives can diverge: one side may want a model demo, the other a maintainable and illuminating proof, and ideally a structure that can later be reused across other projects. The only stable arrangement is one in which human leads set the direction and the AI output is treated as material to be reviewed, reorganized, and absorbed.

*Sources:* [3, 15, 17, 16, 18].

#### Autoformalization --- A year of progress
*Speaker:* Auguste Poiroux.
- The strong Prime Number Theorem appeared as one milestone inside a much broader chronology of recent autoformalization: de Bruijn's abc theorem, the strong Prime Number Theorem, Erdős conjectures, sphere packing, and more recent Frontier Math / Ramsey hypergraph results.
- Autoformalization was framed as translation from natural-language mathematics into proof-assistant code, but not as a fully hands-off process. Human mathematicians still matter through problem selection, scaffolding, review, and the surrounding formal foundations.
- The sphere-packing case illustrated the current scale jump: dimension 8 in five days (80k lines of code), dimension 24 in two weeks (500k lines of code), followed by a large compression phase that removed dead code, merged duplicate declarations, improved project structure, and 'golfed' proofs toward something more reusable.
- Quality rules, linters, declaration-level cleanup, and modernization of Lean itself are part of turning machine-generated proof code into a workable tool.
- OpenGauss was presented as the open-source side of this story: parallel runs, interactive and inspectable. Much closer to general coding-agent workflows than to the sealed long-running system that autoformalized sphere packing with no user intervention. Having a human in the loop seems like a promising approach to make sure the review phase after a formal proof has been generated can be reduced.

*Sources:* [19, 20, 21, 17, 10].

#### Public discussion on human-AI collaboration
- The discussion was framed by a recent public debate, including exchanges on Zulip, about AI companies creating a wasteland in the formal mathematics ecosystem, disincentivizing humans to make contributions and disregarding "honor codes" of mathematical practice and other collaboration norms.
- One issue with the sphere packing formalization was the surprise element to it, the lack of communication between the AI company Math, Inc and the human contributors.
- The Lean code was and is quite messy and some participants wondered whether the shift towards reducing the number of lines of code and increasing quality was always part of the plan or a response to backlash. Auguste answered that code quality had always been a priority, behind the top priority of compiling code generation.
- A recurring theme was that autoformalization changes where the bottlenecks sit rather than making human expertise irrelevant. For technically demanding areas such as complex analysis, one view was that the work is tedious enough that without autoformalization some projects are barely feasible.
- Several participants treated AI-assisted review as a promising near-term use case, i.e. a setup where the AI can itself help make code quality better.
- "Autonomous research" was discussed as a gradual shift rather than a clear threshold one can point to.
- The institutional questions were harder. Should Math, Inc. or similar companies help fund shared infrastructure such as Mathlib? Should one prioritize code quality over immediate upstreaming into Mathlib? No definitive answer emerged, but code quality was treated as the more urgent constraint.
- The discussion also surfaced distributional concerns: whether students are already dropping BSc or MSc projects because frontier systems move too quickly (as seems to have been the case in at least one instance related to sphere packing), whether Mathlib can absorb outside contributions at the needed rate, and how to handle a landscape in which cutting-edge work increasingly sits inside private labs.
- Does Math, Inc have a responsibility to fund Mathlib and its maintainers? Should there be libraries beside Mathlib with lower barriers of entry, similar to a system of different journals, and sites like arxiv?
- Another open question is whether pure mathematics will even be the main beneficiary. Other domains may want lighter-weight formal libraries of their own, with lower barriers to entry and different tradeoffs from Mathlib.

*Sources:* [21, 17, 10, 22].

#### Lean: Collaboration Using Formalization
*Speaker:* Floris van Doorn.
- Floris presented Lean as infrastructure for digitizing mathematics: a proof assistant with a large shared library, broad enough to support current research formalization and collaborative work at scale.
- The case for formalization was framed in institutional rather than only technical terms: verification of proofs, including AI-generated ones, a durable digital math library, lower peer-review burden, and new forms of large-scale collaboration.
- The talk used recent flagship projects (including sphere packing, covered above) to show that this is no longer a niche activity. The cases covered in more detail in this talk were: Tao's equational-theories collaboration, and a Lean formalization of a generalized Carleson theorem in harmonic analysis.
- A recurring organizational theme was blueprint infrastructure. Dependency graphs and explicit prerequisite tracking make it easier to coordinate large teams and to see which assumptions can be weakened or dropped without losing the overall shape of the project.

*Sources:* [3, 23, 24, 22].

## Formalization for the Swiss Economic Institute

Having set the context and sketched the rapid pace of current developments in formal mathematics, especially in its AI-augmented incarnations, we are now in a position to think about second order consequences for fields that are in some sense partially downstream of math, i.e. where one input into the process of doing research involves creating and studying mathematical models, proving properties about them and so on.

On a surface level, investing early in know-how and infrastructure to do formalization for economics could lead to greater trust in research outputs. It would not answer the question whether a model makes sense or whether it has been correctly formalized from natural language math into Lean 4, but it might create more trust that the results proved in the appendix of a typical KOF research paper are correct. Just as many papers in machine learning or empirical economics come with a code companion, e.g. in the form of a GitHub repository, one could imagine a repository also for the proofs in the appendix, containing formal statements of all main results and compiling Lean 4 code that matches the proofs provided in natural language mathematics in the paper.

The process of finding the right abstractions for a formalization is highly nontrivial. The author of the present report had an abstract algebra professor in undergrad who used to remark that mathematics is far more about the definitions than the proofs (there are many variants of this quip). The same goes for setting up the appropriate mathematical machinery for economics. One goal of formalizing mathematical economics would be to make use of AI at scale, where a researcher can essentially provide the formal statements of interest and mathematical tools to an AI model and allow it to explore or ensure the quality of research directions much more quickly than a human researcher. Just as coding agents like Claude Code or Codex make choices about how to implement a graphical user interface for a web app based on the frameworks overrepresented in training data, it seems very likely that AI models trained on economics Lean 4 code would default to certain approaches or abstractions. Getting these right from the start can have a huge positive impact on research output, from a volume and especially a quality perspective.

The technology is now mature enough to start experimenting with seriously in the context of economics research assistance at KOF of ETH. Going beyond the immediate implications for the author's role at KOF however, one can also think about this technology in a long-term perspective. A large repository of policy relevant research formalized in Lean 4 could allow policy makers to quickly adjust assumptions of their models or prescribe new ones on the fly. Some of the work that today happens between conferences and meetings could happen live, there and then, in the rooms where decisions get made, so to speak. The author of this report has at best a very rudimentary understanding of what this would look like at this stage, but consider the following scenario: A plenum where a board of directors are tasked with setting policy in response to a shock. Modelling this shock is important to plan for it. One policy maker might disagree about certain assumptions of the model being proposed and wishes that one part of the model be made richer to accommodate this nuance. Do the theoretical implications used to justify a proposed policy move still hold under these assumptions? Traditionally, answering such a question would be the role of an expert endowed with knowledge of the available literature, but what if the expert knowledge currently does not cover this specific edge case? With a rich enough formal specification, the model can be updated and the same "theorem" can be asked about it. With the rate of progress in formal solvers like those of Math, Inc and Harmonic AI, some questions of this type might plausibly be answerable before the imaginary plenary meeting ends.

Formal verification is also an interesting field to study from an economist's perspective in its own right. Where do bottlenecks move when technological capital can automate a large part of the generative tasks previously performed by human labor? Where does value accrue and what are the long run implications for human capital formation? Based on the authors reading of recent work such as "Some Simple Economics of AGI" [25], it seems clear that verification (whether aided by formal methods or humans in the loop) is an extremely important piece of the puzzle here, and something that fits well with some of the research directions already pursued at the KOF, e.g. "AI as self-learning capital" [26]. As remarked in the workshop notes on the formal-conjectures project, the SPRIG protocol [1] could also be very interesting to revisit and build upon, as it gives a treatment of the economics behind proof claims and their contestation.

## References

1. Sylvain Carré, Franck Gabriel, Clément Hongler, Gustavo Lacerda, and Gloria Capano. "Smart Proofs via Recursive Information Gathering: Decentralized Refereeing by Smart Contracts." *Distributed Ledger Technologies: Research and Practice* (2024). DOI: 10.1145/3595298. URL: https://infoscience.epfl.ch/entities/publication/09e071db-4362-4b42-9017-aa2861d536a9.
2. Albert Q. Jiang, Wenda Li, and Mateja Jamnik. "Learning Plausible and Useful Conjectures." In *Proceedings of the 11th Conference on Artificial Intelligence and Theorem Proving* (2022). URL: https://aitp-conference.org/2022/abstract/AITP_2022_paper_19.pdf.
3. UniDistance Suisse. "SMS Spring Meeting: Formalization and Proof Assistants." 2026-03-25. URL: https://unidistance.ch/mathematiques-et-informatique/evenement/sms-spring-meeting-formalization-and-proof-assistants.
4. Formal Conjectures Authors. "Formal Conjectures." URL: https://google-deepmind.github.io/formal-conjectures/.
5. The Formal Conjectures Authors. "Formal Conjectures GitHub Repository." 2025. URL: https://github.com/google-deepmind/formal-conjectures.
6. AlphaProof and AlphaGeometry teams. "AI Achieves Silver-Medal Standard Solving International Mathematical Olympiad Problems." Google DeepMind 2024-07-25. URL: https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/.
7. Google DeepMind. "Advanced Version of Gemini with Deep Think Officially Achieves Gold-Medal Standard at the International Mathematical Olympiad." 2025-07-21. URL: https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/.
8. Thomas Hubert, Rishi Mehta, Laurent Sartran, and others. "Olympiad-Level Formal Mathematical Reasoning with Reinforcement Learning." *Nature* (2025). DOI: 10.1038/s41586-025-09833-y. URL: https://www.nature.com/articles/s41586-025-09833-y.
9. Oliver Dressler. "Lean LSP MCP: Tools for Agentic Interaction with the Lean Theorem Prover." 2025. URL: https://github.com/oOo0oOo/lean-lsp-mcp.
10. Auguste Poiroux, Antoine Bosselut, and Viktor Kunčak. "RLMEval: Evaluating Research-Level Neural Theorem Proving." In *Findings of the Association for Computational Linguistics: EMNLP 2025* (2025) pp. 10946--10957. DOI: 10.18653/v1/2025.findings-emnlp.581. URL: https://aclanthology.org/2025.findings-emnlp.581/.
11. Harmonic. "Aristotle." URL: https://aristotle.harmonic.fun/.
12. Mistral AI. "Leanstral: Open-Source Foundation for Trustworthy Vibe-Coding." 2026-03-16. URL: https://mistral.ai/fr/news/leanstral.
13. Harmonic. "One Month In - A New SOTA on MiniF2F and More." 2024-07-09. URL: https://harmonic.fun/news.
14. Maryna S. Viazovska. "The Sphere Packing Problem in Dimension 8." *Annals of Mathematics* 185(3) (2017): 991--1015. DOI: 10.4007/annals.2017.185.3.7. URL: https://annals.math.princeton.edu/2017/185-3/p07.
15. Sphere Packing in Lean authors. "Formalising Sphere Packing in Lean." URL: https://thefundamentaltheor3m.github.io/Sphere-Packing-Lean/.
16. EPFL. "Prof. Viazovska's proofs of sphere packing formalized with AI." 2026-03-11. URL: https://actu.epfl.ch/news/prof-viazovska-s-proofs-of-sphere-packing-formaliz/.
17. Math, Inc. "Completing the Formal Proof of Higher-Dimensional Sphere Packing." URL: https://www.math.inc/sphere-packing.
18. Jeremy Avigad. "Reliability of Mathematical Inference." 2019. URL: https://philsci-archive.pitt.edu/16283/.
19. Math, Inc. "Gauss on GitHub." URL: https://www.math.inc/gauss-on-github.
20. Math, Inc. "Introducing Gauss, an Agent for Autoformalization." URL: https://www.math.inc/gauss.
21. Math, Inc. "OpenGauss: an Open Source, State of the Art Autoformalization Harness." URL: https://www.math.inc/opengauss.
22. Patrick Massot. "leanblueprint: plasTeX Plugin to Build Formalization Blueprints." URL: https://github.com/PatrickMassot/leanblueprint.
23. Floris van Doorn. "Lean: Collaboration Using Formalization." 2026-03-30. URL: https://ista.ac.at/en/news-events/event/?eid=5761.
24. van Doorn, Floris and collaborators. "carleson: A Formalized Proof of Carleson's Theorem in Lean." URL: https://github.com/fpvandoorn/carleson.
25. Christian Catalini, Xiang Hui, and Jane Wu. "Some Simple Economics of AGI." *arXiv preprint arXiv:2602.20946* (2026). DOI: 10.48550/arXiv.2602.20946. URL: https://arxiv.org/abs/2602.20946.
26. Hans Gersbach, Evgenij Komarov, and Richard von Maydell. "Artificial Intelligence as Self-Learning Capital." *Economic Modelling* 153 (2025): 107221. DOI: 10.1016/j.econmod.2025.107221. URL: https://doi.org/10.1016/j.econmod.2025.107221.
