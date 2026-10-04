---
title: Optimizing Learning in University: Three Evidence-Based Study Strategies
author: Johannes Wolf
affiliation: Department of Psychology, University of Groningen
course: Academic Skills (PSBE1-25)
instructor: Maria Eșanu
date: 4 October 2026
paper: student
papersize: a4
font: Times New Roman
repo: https://github.com/johannesnorbertwolf/academic-skills-essay-a
word_target: 800
word_min: 700
word_max: 1000
---

<!--
MASTER TEXT — this file holds every word written in this project.

How to use it (Johannes):
  * Type your own words normally. Anything not tagged counts as written by you.
  * When a passage comes from the AI, wrap it in a tag naming the prompt:
        [[AI:1]] the AI text goes here [[/AI]]
    The number must match an entry in PROMPTS.md.
  * Keep the tags tight so the coloring stays word-accurate.
  * In-text citations: [@key] renders parenthetically, @key narratively,
    both matching an entry in refs.bib.

Headings become APA headings in the PDF:
  #   -> Level 1 (centered, bold)
  ##  -> Level 2 (flush left, bold)
  ### -> Level 3 (flush left, bold italic)

The title-page details (title, author, course, instructor, date, ...) live in
the block at the very top of this file, between the two --- lines.

Word count: the required 700-1000 words count the essay body only. Headings are
not counted, and neither is anything from the appendix onward. Put the appendix
material (reflection, statement on AI use) under a heading that contains the
word "Appendix", "Reflection", or "Disclosure", and everything from there down
is left out of the count. `build.py` writes the running total to WORDCOUNT.md.
-->

A university student spends many hours studying. Yet, many students are surprised and disappointed by their results. [[AI:20]]A common reason is that they rely on strategies that feel effective but are not: rereading a textbook chapter, for example, creates a sense of familiarity that is easily mistaken for real knowledge. Cognitive research has identified study techniques that produce more durable learning, yet students tend to underuse them. Self-report studies show that students favor rereading and highlighting over the methods that research supports [@miyatsu2018].[[/AI]] [[AI:53]]The most popular study techniques are therefore not the most effective ones.[[/AI]] [[AI:20]]Some reviews have responded by suggesting how students might improve the strategies they already prefer [@miyatsu2018]. A more [[/AI]]direct route, [[AI:20]]however, is to adopt the strategies with the strongest evidence. This essay therefore asks how university students can optimize their learning, and answers by discussing three evidence-based strategies: pretesting, retrieval practice, and spaced practice. Effective studying is not simply a matter of effort, but [[/AI]]of method.

## [[AI:22]]Pretesting[[/AI]]

[[AI:20]]The first strategy is [[/AI]]pretesting: answering questions about the study material before any studying happens, even if the answers to the questions must [[AI:20]]be [[/AI]]guessed. This might seem counterintuitive, but research indicates that this strategy improves later recall [@putnam2016]. This activates any prior knowledge about the topic and prepares the student to [[AI:20]]connect new information with what is already known. Even incorrect guesses [[/AI]]are useful as they make the student notice [[AI:20]]and remember the correct [[/AI]]information once it appears. 

Prequizzing is becoming easier to put into practice. Before a study session, such as a reading session or a lecture, a student can write down questions about the topic and attempt to answer them and return to them afterwards to check and correct the answers [@putnam2016]. Many textbooks also contain post-reading quizzes that can be easily repurposed for pretesting. The emergence of AI-chatbots gives us another option: create a quiz from lecture slides or textbook chapter and it can even be prompted to meet precisely specified requirements such as difficulty level or quiz size. The main obstacle to this strategy is psychological rather than practical: it feels wrong to guess at material without any prior studying. Intuitively, students prefer to read first. Recognizing that pretesting takes little time and prepares the memory helps to overcome this hesitation.

## [[AI:22]]Retrieval Practice[[/AI]]

The second strategy is retrieval practice: the reproduction or summarization of the study material after consuming it without looking at it. One implementation is the RRR method, Read, Recite, Review, described by @putnam2016: the student visits the lecture or reads the material, writes a summary from memory, and lastly reviews it against the study material. The second step is the retrieval itself, and the important part is that the student reproduces the material from memory rather than copying it. This both reactivates what was learned and reveals what was missed.

The student will not use the material for summarization but merely write down what they remember. This shows what they did not fully understand or remember. In its classical implementation, of the common study strategies discussed by @miyatsu2018, only flash cards make use of retrieval practice.

As discussed by @miyatsu2018, at least summarization and outlining can be altered in a way that makes use of retrieval by practicing these after studying the material from memory.


## [[AI:22]]Spaced Practice[[/AI]]

The third strategy is spaced practice: this is not about how to study but when. If a student uses spaced practice, they study for short periods of time, mix studying of different subjects and take considerable breaks between study sessions. [[AI:33]]In practice, this means studying each subject a little on most days and revisiting earlier topics in later sessions.[[/AI]] The opposite of spaced practice is massed, crammed studying. According to @putnam2016, for the same time spent studying, spaced practice gives much better results.

The typical example of cramming is a long study session the day or even the night before an exam. The difference in retention becomes even greater in the long term. While this might give acceptable results on the day of the exam, for long-term learning, spaced practice is the much better study strategy. Assuming university students are not merely studying to pass exams but are eager to learn and remember, spaced practice is the more effective strategy. 

  

 
# [[AI:22]]Conclusion[[/AI]]

[[AI:42]]This paper examined[[/AI]] three study strategies discussed by @putnam2016: pretesting, retrieval practice and spaced practice. The former two focus on retrieving prior and just acquired information; the latter is a strategy for allocating study time most efficiently. 

Unlike the study strategies reviewed by @miyatsu2018, the study strategies discussed in this paper are not chosen by popularity among students but by effectiveness. They do, however, have the disadvantage of needing more time in preplanning, a more conscious decision and commitment to stick to them as they may not be obvious or intuitive to students. 

The technological advancements in AI can benefit these study methods. For example, a student may feed their study material to a chatbot and have it create a pretesting quiz for them. In the RRR method, they might ask an AI chatbot for feedback after the final review step of the method to make sure they did not miss or misunderstand anything.

The strategies discussed in this paper do not mean that a student has to spend more time studying. With these more efficient strategies they should get better results with the same amount of time studying. Alternatively, if a student is already happy with their results, these study strategies should enable them to spend less time studying for a similar result. Any time saved can be leisurely spent with what student life has to offer beyond lectures, studying and exams.

# [[AI:20]]AI disclosure statement[[/AI]]

[[AI:54]]This assignment was written with extensive help from an AI assistant. My intention was to make the assignment an honest experiment: to produce a real piece of academic writing while keeping a complete, public record of exactly how it was made. Transparency about how work is produced is a central academic value, and this project tries to live up to it. Every prompt I sent and every reply the assistant gave are recorded in the project's public repository (https://github.com/johannesnorbertwolf/academic-skills-essay-a), and the final text carries a word-level attribution showing which passages I wrote and which the assistant produced. The project's public web page shows the same attribution in color.[[/AI]]

The tool used (the so-called harness) was opencode running a Chinese open-weights language model DeepSeek V4.1 Flash. I [[AI:54]]supplied the two assigned articles and the assignment brief, and I chose the topic and the three strategies. The assistant produced an initial full draft, which I then worked through carefully: I read it against the original articles, rewrote passages in my own words, corrected mistakes, cut material that was inaccurate or unnecessary, and decided what the argument should say. About four-fifths of the current wording is [[/AI]]my own.

[[AI:54]]Both assigned articles [@miyatsu2018; @putnam2016] [[/AI]]were thoroughly read by me. I read Putnam first, and interrupted my reading at the very beginning when the pretesting strategy was introduced. This sounded so counterintuitive, I wanted to immediately try it out — of course with the help of AI. So I threw it into Gemini Notebook (formerly NotebookLM), an AI tool that specializes in working with documents without (or with fewer hallucinations). One of its headlining features is that it creates multiple-choice quizzes on the documents you feed it. So this is what I did almost before starting the reading. I put the pretesting strategy into practice and quizzed myself on the two articles I was about to read.

[[AI:54]]How this happened, section by section:[[/AI]]
- First, I had the AI draft the essay as a whole
- For the section on pretesting, I took this first draft and changed it to my liking. My intention was to do it like that with the whole text. However, I realized that this was not a good strategy. I didn't enjoy this process, I felt like I was only changing things to have it not all written by the AI and worst of all, I felt I was making the text worse with my changes. The first draft of the AI was totally solid and if it hadn't been written by AI, it would have surely been good enough to pass the assignment. 
- So for the second and third study strategy, I changed my approach. I deleted what the AI had written and drafted the text myself. I felt this was much better for my learning process, I asked myself, why I chose this study strategy, what I liked about it, in what way, I thought it was better than the other strategies. A few times, I went back to the original articles to check how exactly the strategies worked. When I was done, I asked the AI for feedback related to spelling, style, format and also what it thought about the content. I reviewed the suggestions one by one using most of them. The more complicated feedback I worked into the text myself, the simpler things like typos, style and format suggestions I let the AI fix. 
- For the conclusion, I again tried a new approach. I asked the AI for some ideas on what to stress and used its suggestions to then write the text myself. Again, I used the feedback from the AI to streamline the text I had produced. 
- Lastly, for the introduction, I left this mostly to the AI. I let it write a first draft, just made some changes by hand. In the end I felt like it would probably have been better to write this last. However I did feel like writing an introduction is something that should absolutely be outsourced to AI. In the end I proposed to the AI to rewrite it now that we know exactly what the rest of the text will be but it just suggested some smaller edits which I allowed it to do. To me the introduction reads completely fine, does what an introduction is supposed to do. 
- Reflection: written entirely by me. Just some minor editing by the AI.
- My plan for the AI disclosure statement was to allow myself the joke of having this completely written by the AI (with heavy steering, feedback and editing from me). However, what the AI drafted completely misrepresented the workflow and my values behind this process, so that I decided to mostly write this myself.

[[AI:65]]Both assigned articles were read in full, and every citation was checked against its source, so no reference is invented or misattributed. I take full responsibility for the finished text and can discuss and defend every part of it.[[/AI]] 

I want to emphasize that even if this work does not meet the standards of academic writing or the rules for AI usage, the use of AI is completely transparent. I thusly hope and expect it won't be considered fraud. 

# [[AI:20]]Reflection[[/AI]]
I felt like just writing the essay would have been a little too boring. I am excited about what AI can do for us so I decided to use this essay to explore what is possible, what is fun, what helps and hinders my learning process and what is allowed. I definitely tried to test the waters of this last point. It is obvious that this new world of AI is unfamiliar to us all, students and faculty, and nobody really knows yet how it should be used. I suppose this is why the rules for AI usage are still rather blurry. I am very curious to find out whether I will pass this assignment with the amount of AI used. I had tremendous fun writing it, but also, it was a lot of work. There is no doubt just writing it myself the traditional way would have been much easier. I really hope the readers don't take my approach as a provocation but as an invitation to also think about how AI should be used in academic writing without a pre-existing answer but with curiosity.   
