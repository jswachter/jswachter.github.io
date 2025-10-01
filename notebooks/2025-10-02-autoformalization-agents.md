---
title: Autoformalization agents   
date: 2025-10-02
tags: math, AI, autoformalization 
---

# Autoformalization agents 

Autoformalization in the context of mathematics is about taking more or less free flowing natural language and LaTeX renderings of statements or proofs and turning them into formal, ideally compilable statements, like Lean code. 

Some smart people are saying that no math paper will be published in 2030 without an appendix containing the formalized version. One could of course imagine a companion git repository, just as many ML papers have a code companion, but the presentation of this is not the main point of this post. 

Instead: How do we get there in a way that makes math research better? 

## Taking a step back 

Back in the fall of 2024 I undertook the daunting task of writing the full thirteen chapters of Beatrice Acciaios handwritten lecture notes for mathematical finance in LaTeX. It took a lot of painstaking interpretative work and many iterations, and I think I learnt a lot during the latter. It is especially useful to understand how different results build on oneathor, and trace the graph of dependency there. Of course this can be done without transcribing, but a good transcription can force you to do it. 

Thankfully a lot of great books and lecture notes are already transcribed. What if I could direct a system or an 'agent' at these artifacts and get the full dependecy between definitions, lemmas, theorems and the examples mentioned to illustrate. If one has access to the original LaTeX code and this one uses consistent labeling and referencing, one can use classical coding to create a pretty good graph. 

## Iteratively hashing out formalizations 

In the context of a mathematical paper or some lecture notes, one can consider a result and its proof. The assumptions, definitions and previous results all inform its presentation. The level of abstraction in the previous presentation influences what follows. 

Lean code can also be written at different levels of abstraction. One can import more or less sophisticated known results to construct proofs. 

What would be really interesting is if one could direct an agent to work through a math paper. It would make a first pass to understand the statements and whether they depend on oneaother. Then it would start to formalize this dependence, by using different parts of the paper to formalize other parts. This is probably not a fully linear, and certainly not a one-off process. Care would need to be taken to see what is left out, or taken for granted. Ideally some way of filling this in or claryfing what these blindspots are should be provided. Omission is absolutely crucial for thinking about math. It is not possible to create new and interesting results (or even solve a problem one doesn't know the answer to/strategy for) if every single step is fully grounded and bound by logic. But the logic, as in formal proof with stated assumptions, needs to enter the picture at some point, otherwise the whole enterprise of math is doomed. 

## Productizing the formalizer agent 

I'm not thinking so much about something to sell here, but rather about how this is something I would really like to use myself. 

It would be a plugin into ChatGPT or Claude that allows these bots to see a pdf that you direct it at. Then there is some server that stores screencaptures or some chunks of the pdf. These things are parsed into markdown and latex. Where there is uncertainty, the user is notified, and the exact transcription can be resolved with some human input. 

The markdown and latex document is then decorated with labels and interrelations of results. Some pdfs feature links between portions and this could also be used here. 

Then the formalization starts. Definitions and assumptions are recorded, the appropriate math libraries in Lean are imported, potential gaps are pointed out. The statements and their proofs are formalized with reference to other statements. Compilation of the Lean code is checked between each major change. Whenever there is a problem, a subagent is launched to find a remedy and the main agent determines whether the proposed change is admissible or not. Most likely the main agent is actually many parallel agents communicating, sharing their scratchwork. 

Implementation details: Some multi-agent orchestration, or perhaps multiple instances of Codex or Claude Code in appropriately crafted sandboxes. MCP server to create integration into your favorite chatbot of choice. Just like the latest iteration of terminal-based coding agents wiped out endless copy pasting and hopeless iterations back and forth for coding, this could make a big difference for the process of math research, especially the formalization step.  

