# Professional Research Presentation Generation Prompt

This is the user's prompt, verbatim apart from Markdown formatting. It is the contract for every run of `paper-to-pptx`. `SKILL.md` adds run notes only. Where the two seem to conflict, this file wins, except where the user's request in the session says otherwise (for example a different slide count).

## Role and Objective

Act as a senior scientific presentation designer, research communication specialist, and PowerPoint production expert with extensive experience creating presentations for international academic conferences, research seminars, and technical presentations.

Your task is to thoroughly analyze my paper.tex file and create an exactly 15-slide, professionally designed, editable PowerPoint presentation (.pptx) that communicates the research clearly, accurately, and convincingly.

The presentation must look like it was carefully designed by an experienced academic researcher and professional presentation designer, not automatically assembled from a generic template.

## 1. Thoroughly Understand the Research Paper First

Before creating any slides, read and analyze the complete paper.tex source file, including its abstract, introduction, related work, methodology, mathematical formulations, proposed framework, experiments, results, discussion, limitations, and conclusion.

Also examine any available figures, tables, equations, algorithms, references, and supplementary source files that are relevant to the paper.

Identify the following:

- The research problem and motivation.
- The research gap and its significance.
- The primary research objectives and contributions.
- The proposed methodology, architecture, or theoretical framework.
- The experimental design, datasets, evaluation metrics, and baselines, where applicable.
- The most important results and their implications.
- The limitations, conclusions, and future research directions explicitly discussed in the paper.

Build a clear understanding of the research before deciding how to present it. Do not begin generating slides after reading only the abstract or selected sections.

## 2. Strict Scientific Accuracy and Source Fidelity

The paper is the sole authoritative source for the presentation's scientific content.

Follow these rules without exception:

- Do not invent facts, claims, statistics, experimental results, citations, methods, contributions, or conclusions.
- Do not introduce external research, unsupported examples, or additional arguments that are absent from the paper.
- Preserve the meaning of all technical terms, equations, methods, results, and conclusions.
- Do not exaggerate the novelty, performance, significance, or practical impact of the research.
- Preserve numerical values, units, dataset sizes, metric definitions, and reported comparisons exactly.
- Do not present a proposed method as experimentally validated unless the paper explicitly supports that claim.
- Use concise paraphrasing when necessary for presentation readability, but never change the scientific meaning.
- Use figures, tables, equations, and diagrams from the paper whenever appropriate. Redesign them for readability only when doing so preserves their full technical meaning.
- Use citations only when they are supported by the paper's references.
- Do not add a researcher's name, affiliation, funding statement, acknowledgment, or institutional logo unless the information is explicitly provided or authorized in the available source material.

You may reorganize the paper's information into a more effective presentation narrative. However, you must not introduce new scientific content merely to fill slides or make the presentation appear more impressive.

If important information is missing, ambiguous, or inconsistent, do not guess. Omit unsupported details or flag the issue for review.

## 3. Exactly 15 Slides

Create exactly 15 slides, including the opening and closing slides. Adapt the following structure to the paper's actual content rather than forcing irrelevant sections into the presentation.

1. **Title Slide:** Exact paper title, author information, affiliation, and relevant presentation details available in the source.
2. **Research Background:** Essential context needed to understand the problem.
3. **Problem Statement:** The specific problem addressed by the study.
4. **Research Gap and Motivation:** The gap identified in the paper and why it matters.
5. **Research Objectives and Contributions:** Clearly distinguish the objectives from the actual contributions.
6. **Related Work:** A focused synthesis of the relevant literature discussed in the paper.
7. **Research Overview:** A concise visual roadmap of the proposed approach.
8. **Methodology:** The main research process, methods, or theoretical approach.
9. **Proposed Framework or Architecture:** A clear, technically accurate visualization of the central model or system.
10. **Technical Details:** The most important equations, algorithms, design decisions, or implementation details.
11. **Experimental Setup or Evaluation Design:** Include the data, baselines, evaluation metrics, or analytical setup where applicable.
12. **Main Results:** Present the most important reported findings using accurate charts, tables, or visual comparisons.
13. **Analysis and Discussion:** Explain the findings and their significance strictly as supported by the paper.
14. **Conclusion and Limitations:** Summarize the main conclusions and explicitly reported limitations or future directions.
15. **Closing Slide:** A professional final slide with a concise concluding message grounded in the paper and a Q&A invitation.

This is a suggested structure, not permission to invent content. For theoretical or conceptual papers, adapt experimental slides to the paper's actual analytical or methodological content. If a suggested topic does not exist in the paper, use the slide for another relevant topic supported by the source.

## 4. Professional Research-Presentation Design

Study the design principles used in high-quality presentations at reputable academic conferences and research seminars. Select a coherent visual direction appropriate to the research topic, audience, and complexity of the paper.

The presentation should feature:

- A consistent visual identity, color palette, typography system, spacing system, and alignment grid.
- Strong visual hierarchy that makes the purpose of every slide immediately clear.
- Concise slide titles that communicate the main point of each slide.
- Readable body text and appropriately sized technical labels.
- Carefully composed layouts that balance text, diagrams, figures, and whitespace.
- Research-specific visualizations rather than generic decorative graphics.
- High-quality vector graphics wherever practical.
- Properly typeset mathematical equations and technical notation.
- Legible charts with accurate labels, units, legends, and scales.
- Consistent styles for diagrams, arrows, connectors, shapes, callouts, and annotations.
- Restrained use of color, with color carrying meaning rather than serving as decoration.
- Consistent treatment of references, footnotes, captions, and slide numbering where appropriate.

Use a professional 16:9 widescreen layout unless the presentation requirements specify otherwise.

Choose a restrained, sophisticated design suitable for a serious academic presentation. Avoid unnecessary visual effects, excessive gradients, decorative icons, gratuitous illustrations, and other elements that distract from the science.

## 5. Avoid Generic or Formulaic AI-Generated Design

Before developing the presentation, evaluate at least 20 design-quality considerations commonly associated with generic, automatically generated, or poorly designed presentations.

Include considerations such as:

- Repetitive slide layouts.
- Predictable card-based compositions on every slide.
- Excessive use of rounded rectangles and decorative containers.
- Generic stock-style illustrations unrelated to the research.
- Arbitrary icons that add no scientific information.
- Excessive gradients, shadows, glows, and visual effects.
- Inconsistent spacing, alignment, and typography.
- Unbalanced compositions and awkward whitespace.
- Overcrowded slides and excessively small text.
- Vague, repetitive, or generic slide titles.
- Long paragraphs copied directly from the manuscript.
- Repeated text that adds no new information.
- Decorative charts or diagrams with little analytical value.
- Inconsistent color use or meaningless color coding.
- Overly symmetrical layouts that ignore the content's needs.
- Inconsistent diagram styles and connector conventions.
- Poorly rendered equations, symbols, or special characters.
- Misleading visual emphasis or unsupported numerical claims.
- Low-quality, stretched, or pixelated figures.
- Generic opening and closing slides that do not fit the research.

Treat this as a design-quality audit, not as a way to evade AI-detection systems. No visual checklist can reliably establish whether a presentation was generated by AI. The objective is to produce a deliberate, research-specific, polished presentation with the care and judgment expected from a skilled human designer.

Do not mechanically force every slide into a different layout just to create variation. Use a layout only when it serves the information being presented. Maintain consistency while allowing appropriate variation in composition.

## 6. Data Visualization and Technical Figures

Prioritize the scientific figures, framework diagrams, experimental plots, tables, and equations that are most important to understanding the paper.

For every visual:

- Verify that the information matches the source.
- Do not change data values, axis scales, units, labels, or comparative relationships.
- Simplify complex figures only when the underlying meaning remains intact.
- Ensure diagrams accurately represent the proposed system, research workflow, or relationships described in the paper.
- Make technical visuals understandable from presentation distance.
- Avoid redrawing a figure in a way that introduces unsupported relationships or implications.

When a figure in the manuscript is already effective, reuse it at high resolution. When a figure is too dense for a slide, create a faithful, simplified presentation version rather than shrinking it until it becomes unreadable.

## 7. Slide Content and Presentation Narrative

Create a coherent narrative from the research problem to the proposed approach, evidence, findings, and conclusion.

Each slide should have one principal purpose and a clear takeaway. Use concise bullet points, short explanatory statements, equations, diagrams, and data visualizations instead of dense paragraphs.

Ensure that:

- The audience can understand the main argument without reading the manuscript.
- Technical depth is appropriate for an academic audience familiar with the research field.
- Important definitions are introduced before they are used extensively.
- The methodology logically connects to the results.
- The results directly support the conclusions presented.
- Transitions between slides feel natural.
- The most important scientific contributions receive appropriate visual emphasis.

Do not sacrifice essential technical detail simply to make the slides minimalistic. Prioritize clarity, accuracy, and meaningful detail over both excessive text and excessive simplification.

## 8. PowerPoint File Requirements

Generate a real, editable .pptx file rather than a PDF, a collection of slide images, or a visual mockup.

Where practical:

- Use native PowerPoint text boxes, shapes, connectors, tables, and charts.
- Keep text editable and ensure objects are properly aligned.
- Use vector-based diagrams when suitable.
- Avoid using full-slide images as a substitute for editable slide content.
- Preserve equations and special characters correctly.
- Use fonts that are widely available or properly embedded where supported.
- Ensure that the deck opens correctly in Microsoft PowerPoint.

A complex original research figure may remain an image when recreating it would reduce fidelity, but the rest of the slide should remain editable.

## 9. Quality Assurance Before Delivery

After generating the PowerPoint, perform a complete slide-by-slide review.

Check the following:

- **Content integrity:** Verify titles, technical terms, numerical values, formulas, references, figure captions, and scientific claims against paper.tex.
- **Visual integrity:** Detect overflow, clipped content, overlapping elements, distorted figures, inconsistent spacing, poor contrast, and unreadable text.
- **Presentation consistency:** Confirm consistent typography, colors, margins, alignment, slide numbering, and diagram styling.
- **Narrative quality:** Verify that the 15 slides form a coherent presentation and that no slide repeats information unnecessarily.
- **Technical integrity:** Confirm that the .pptx file opens successfully, contains exactly 15 slides, and retains editability wherever intended.

Render every slide to an image or PDF for inspection if the available tools support it. Inspect the rendered slides individually, make corrections, and render them again when needed. Do not consider the presentation complete merely because the file was generated successfully.

## 10. Final Deliverables

Provide the following:

1. **Final PowerPoint:** A polished, editable file named `Research_Presentation.pptx`.
2. **Slide Preview:** A PDF version or slide montage for quick review, if supported.
3. **Source or Generation Files:** The script, project files, or other editable source materials used to generate the presentation, if practical.
4. **Verification Summary:** A brief report confirming the slide count, scientific-content verification, visual inspection, and any limitations or unresolved issues.

## Final Instruction

First understand the complete research paper. Then plan the presentation narrative, select a suitable visual direction, develop the slides, generate the actual PowerPoint file, and inspect the finished slides before delivery.

Scientific accuracy is mandatory. Visual professionalism is essential. Every design decision must serve the research.

The final result should look polished enough for an international academic conference, research symposium, or formal university presentation. It must communicate the paper's actual contributions without inventing content, exaggerating results, or relying on generic presentation-design patterns.
