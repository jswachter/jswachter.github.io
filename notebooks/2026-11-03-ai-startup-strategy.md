---
title: AI startup strategy, nine months later
date: 2026-11-03
collection: AI
tags: AI, agents, startups, accounting
---

# AI startup strategy, nine months later

It’s always a somewhat silly exercise to report predictions after many of them have turned out to be right. Of course any such report is prone to have a bias in favor of well-turned out ones, leaving the reader in the dark about the host of other predictions that did not come to pass.

I was involved in startup work for quite some months last year up until February of this year and I here extract some of my thoughts towards the end of this work. We were in a position where a pivot was needed and thought hard about what the basis for it ought to be, what viewpoint and outlook should guide it. In the end, the most consequential determinant of not pursuing these ideas came from logistical and personal constraints, some of which, along with broader reflections of our general position, I explained in the paragraphs surrounding the following excerpt, translated by AI from Swedish into English for a more cohesive reading experience.

I think it’s quite interesting to reflect on some of these dynamics and revisit them now, 9 months later. Excerpt:

> […]
>
> Another problem, I would say, is that using AI is a skill that takes time to learn. We can probably be a little blind to how much further ahead we are in using these models than the average person. I have no data on this, but I would not be surprised if we consume 100x the number of tokens over a given period compared with [REDACTED]’s employees...[^token-gap] both privately and at work. [REDACTED] is probably not unique in this respect; things surely look at least as bad at many workplaces.
>
> […]
>
> Another thing that is different is that the models are so incredibly much better. I have no doubt that almost all tasks carried out at [REDACTED] could be handled by an agent given the right prompt, context and previous examples. What would remain is verification and checking. To get there, someone obviously needs to create prompts, collect examples, build workflows and break things down into tasks. There also needs to be a system that provides an overview of the agent’s work. It must be possible to follow which decisions have been made and why. When a new model is released and an old one is phased out, it must be possible to track how this affects reliability, meaning some kind of internal evals.
>
> It is hard to communicate the above. Very few people (relatively speaking) understand how good the models actually are at many difficult tasks. People are also incredibly bad at prompting, understanding what needs to be given to the model, and so on. Evals are an unfamiliar concept.
>
> […]
>
> We have somewhat different views on how big a problem/opportunity Claude Cowork represents and what the likely development of that product is when it comes to features and adoption. To me, it is clear that
>
> 1. Anthropic’s goal is for knowledge workers to use either Claude Code (if they are technical) or Claude Cowork (if they are not technical). They will aim for most of one’s working day to be spent in Cowork and for it to be the main "operating system" for knowledge work.
> 2. Traditional software that cannot be integrated/connected to Cowork will stop being used by customers who use Cowork. The whole point is to have a workspace with all the integrations and a very strong underlying orchestrator in the Claude Agent SDK. An interesting example that actually goes a step further is that Harvey (non-traditional software by my definition, rather AI-native) has released a connector for Claude Cowork. Instead of becoming an operating system for legal work, they are positioning themselves more as an agent that can be called on by Cowork.
> 3. Cowork will face competition. OpenAI will release a wrapper for Codex that is user-friendly for non-technical people. Mistral will build some kind of wrapper for Mistral Vibe. Solutions like Openwork will be expanded and come very close to the closed-source alternatives in features.
> 4. Claude Cowork and similar systems will expand more and more. They have already released scheduled tasks and simple customization solutions. Everything that is general to knowledge work will be built.
> 5. The model makers will release models that are only available in their own "wrappers". An early example of this was Codex-5.3, which was available only in the app for a week. I can imagine a scenario where it is not a matter of a week but applies to a model’s entire lifecycle.
> 6. Anthropic and OpenAI will increasingly strive for tokens to be consumed directly through their application layer, rather than through third parties like Cursor, Harvey, etc. They want to own the margins and lock-in that the application layer provides, and are worried about commoditization of the model layer.
>
> Based on these guesses about what the future will look like, I think the following principles are important for a startup in the AI application layer:
>
> 1. The product must be able to integrate into a general-purpose workspace like Claude Cowork, probably via MCP.
> 2. The product must solve a specific problem for a particular vertical that cannot be captured by a skill + base model invocation. It must be a task that requires a lot of private data, or very specific private data, packaged in the right way, and possibly several steps. Perhaps several agents collaborating on different parts.
> 3. The product should emphasize verification rather than consuming tokens. What do I mean by this? Previous generations of the application layer have generally been token resellers; see the comment on Legora earlier. This is a paradigm that is becoming increasingly unsustainable as Anthropic and OpenAI clearly move into the application layer. What still remains, however, and is a problem that keeps growing with token consumption, is the need to create an overview and verify outputs. This requires people who know the subject ([REDACTED]) and systems that make verification at that scale economical (perhaps Hilma).
>
> I think the intuition around Beancount was good in that it focused on verification and on writing the accounting in a format where you could run tests like bean check. Now, for various reasons, Beancount is not mature enough for accounting at the level [REDACTED] does it, but I see a layer that helps with verification, running tests, etc., and is specifically geared toward accounting as remaining valuable for quite some time.
>
> I think we should take certain "structural forces" into account:
>
> 1. The accounting profession will start using agentic AI on a large scale during 2026/2027.
> 2. Anthropic and OpenAI will compete directly with their own API customers with the aim of owning the majority of token consumption. If your product is one or a few API calls per task, it will be eaten up by the larger companies.
> 3. As AI outputs become increasingly common, the demands for observability and verification increase.
> 4. Just as there are lots of successful companies and startups in dev tooling, there will be multibillion companies in tooling for knowledge workers, tools that are specifically adapted to be used with agents.
>
> I think GitHub for accounting is significantly more defensible than Claude Code for accounting for that reason.
>
> At the same time, as I said, I think the consulting track is incredibly important. Our outreach on LinkedIn and by email shows that the market is absolutely not there yet when it comes to AI use... it is incredibly difficult to build GitHub for accounting if no one is using agents yet.
>
> […]

[^token-gap]: Currently, early November 2026, with tens to sometimes hundreds of millions of tokens spent per day this gap has probably increased.
