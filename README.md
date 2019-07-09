# Gender Analysis Toolkit
A toolkit for analyzing of gender and gender relations across documents

##  History

This toolkit is an extension of work we began in Fall 2018 analyzing gender in English language novels.

The results of that research is available at [The Gender Novels Project](http://gendernovels.digitalhumanitesmit.org) website, and our research code is available at https://github.com/dhmit/gender_novels/

*This MIT Digital Humanities Lab project is part of the [MIT/SHASS Programs in Digital Humanities](https://digitalhumanities.mit.edu/) funded by the [Mellon Foundation](https://www.mellon.org/).*

## Usage
To use our tools or contribute to the project, please view our guide to contributing, `CONTRIBUTING.md`. It includes information on how to install the tools we used as well as style guidelines for adding code. We are open to contributions and would love to see other people’s ideas, thoughts, and additions to this project, so feel free to leave comments or make a pull request!

## Navigating Gender Analysis

For anybody who wants to use our code, here’s a little outline of where everything is.

In the [`gender_analysis/gender_analysis`](https://github.com/dhmit/gender_analysis/tree/master/gender_analysis) folder, there are three folders: 

1. [`analysis`](https://github.com/dhmit/gender_analysis/tree/master/gender_analysis/analysis) — programming files focused on textual analysis and research write-ups, including data visualizations and conclusions
2. [`pickle_data`](https://github.com/dhmit/gender_analysis/tree/master/gender_analysis/pickle_data) — pickled data for various analyses to avoid running time-consuming computation
3. [`testing`](https://github.com/dhmit/gender_analysis/tree/master/gender_analysis/testing) — files for code tests

In the [`gender_analysis/gender_analysis/analysis`](https://github.com/dhmit/gender_analysis/tree/master/gender_analysis/analysis) folder, there are the following 
modules: 

1. [`metadata_visualizations`](https://github.com/dhmit/gender_analysis/tree/master/gender_novels/analysis/metadata_visualizations.py) — 
code for graphing information about corpus metadata.
1. [`dunning`](https://github.com/dhmit/gender_novels/tree/master/gender_analysis/analysis/dunning.py) — 
code for comparing the significance of certain words between two corpora.
1. [`gender_pronoun_frequency`](https://github.com/dhmit/gender_analysis/tree/master/gender_novels/analysis/gender_pronoun_frequency.py) — 
code for analyzing frequency of gendered pronouns.
1. [`instance_distance`](https://github.com/dhmit/gender_analysis/tree/master/gender_novels/analysis/instance_distance.py) — 
code for analyzing distances between occurrences of certain words.
1. [`pronoun_adjective`](https://github.com/dhmit/gender_analysis/tree/master/gender_novels/analysis/pronoun_adjective.py) — 
code for analyzing adjectives associated with gendered pronouns.
1. [`statistical`](https://github.com/dhmit/gender_analysis/tree/master/gender_novels/analysis/statistical.py) — 
code for analyzing results for statistical significance.


[`corpus.py`](https://github.com/dhmit/gender_analysis/blob/master/gender_novels/corpus.py) and 
[`document.py`](https://github.com/dhmit/gender_analysis/blob/master/gender_novels/novel.py) 
include code for loading texts and metadata such that they can be analyzed.   


*This document was prepared by the MIT Digital Humanities Lab.*

Copyright © 2018-2019, [MIT Programs in Digital Humanities](https://digitalhumanities.mit.edu/). Released under the [BSD license](https://github.com/dhmit/gender_novels/blob/master/LICENSE).
Some included texts might not be out of copyright in all jurisdictions of the world.
