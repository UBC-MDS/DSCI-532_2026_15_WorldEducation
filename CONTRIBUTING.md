# Contributing to the World Education Dashboard project

This outlines how to propose a change to the World Education Dashboard project.

## Coding style
Consistency in coding style is important throughout the project. We recommend following the official Python style guide (PEP 8).
Key points include:
- Indentation: Use consistent tabs or spaces to maintain readability.
- Line Length: Keep lines reasonably short; avoid exceeding half the width of notebook cells if applicable.
- Comments: Use # for comments and write them clearly to explain the code.
- Whitespace: Include proper spacing around operators, function arguments, and within control structures.
- Imports: Organize import statements in logical groups and in the recommended order (standard library, third-party packages, local modules).

## Prerequisites
Before you make a substantial pull request, you should always file an issue and
make sure someone from the team agrees that it's a problem. If you've found a
bug, create an associated issue and illustrate the bug with a minimal reproducible example.

## Pull Request Process
- It is recommended to create a Git branch for each pull request in order to maintain consistency.
- Code should follow the official python style guide
- We will be using Docstring for documentation.

## Code of Conduct
Each contributor shall adhere to the examples set below:
- Use welcoming and inclusive language
- Be respectful of differing opinions and viewpoints
- Be cognizant of intention when proivding constructive criticism
- Recognize the best in others
- Show empathy towards community members

Each contributor should avoid behaviours such as:
- Sexualized language and unwanted sexual attention/advances
- Trolling, insults, derogatory comments, and political attacks
- Public or private harassment
- Ignoring privacy concerns of the community
- And other conduct which could reasonably be considered inappropriate in a professional setting

## Development tools, GitHub infrastructure, and practices used

Throughout this project, our team was able to apply various tools used in software engineering and practices in a real-life data science and machine learning workflow. We were able to leverage Git and GitHub for version control, and had a collaborative process throughout the projects - through pull requests, code reviews, and issue tracking. With these tools, we were able to manage changes systematically and document any design changes, and keep a traceable project history.

## Code of Conduct

This project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md) and by contributing to or otherwise participating in this project you agree to abide by its terms.


## Collaboration Retrospective and Norms
### M3 Retrospective
What worked
- We continued to divide work into major and minor tasks, allowing each team member to take ownership of a core feature while contributing to smaller improvements
- All team members contributed across both code and documentation, and most tasks were completed on time.
- All PRs received at least one reviewer before merging.
- We successfully integrated multiple components (map, bar charts, scatterplot, AI tab) into a dashboard.

What didn't work
- Some team members did much more coding than others and some did much more writing than others
- Design documentation was not consistently updated alongside implementation, especially for major features like charts and filtering logic.
- Communication gaps remained around task ownership and responsibilities (e.g., releases, submissions)
- PR sizes remained large (e.g., 500–800+ LoC), making reviews difficult and reducing their effectiveness.

### M4 Collaboration Norms
For M4, we are committing to the following:
- Smaller, more managable PRs
- Stronger review practices. Every PR must have at least one meaningful review comment before merging. Wherever possible, the reviewer should be someone who did not implement the feature
- Documentation-first approach. Update spec before writing code.
- Include clear PR descriptions explaining what changed and why
- Improved communication and coordination.  More frequent check=ins


## Attribution

These contributing guidelines were adapted from the [dplyr contributing guidelines](https://github.com/tidyverse/dplyr/blob/master/.github/CONTRIBUTING.md).
