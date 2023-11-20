Step 1.1:

How many 100bp reads are needed to sequence a 1Mbp genome to 3x coverage?

Read number = coverage * ((genome length) / (read length))
Read number = 30,000



Step 1.3:

1. In my simulation of 3x coverage, 50550 bases have 0 coverage.  This is 5.055% of the genome.
2. Based on the graph, this simulation is consistent with Poisson expectations, as the simulated coverage and Poisson distribution are slightly right-skewed.  The normal distribution does not fit the simulated data as well as the Poisson, as it predicts a distribution that is slightly less right-skewed than the simulated data and Poisson distribution.



Step 1.4:

1. In my simulation of 10x coverage, 19 bases have 0 coverage.  This is 0.0019% of the genome.
2. This simulation is, again, consistent with Poisson expectations, as the simulation and Poisson distribution both have overlapping normal distributions.  The normal distribution also fits the data well, but not as well as the Poisson distribution.  It predicts a curve that is slightly more left-skewed than the simulation.



Step 1.5:

1. In my simulation of 30x coverage, 1 base has 0 coverage.  This is 0.0001% of the genome.
2. This simulation is, once again, consistent with Poisson expectations. The simulation and Poisson distribution both have highly overlapping normal distributions, this time centered on a coverage of 30, rather than 10 as seen in the previous simulation.  The normal distribution also fits the data well.  However, if I were to choose between the Poisson and normal distribution to represent the simulation data, I would choose the Poisson distribution.  The Poisson distribution more closely matches the data, while the normal distribution is, again, very slightly skewed to the left.



Step 2.4:

Used the following command in my terminal to produce my directed graph:
dot -Tpng debruijn.dot -o ex2_digraph.png



Step 2.5: 

Possible genome sequence with a maximum 3-mer occurance of five:

Order of k-mers used:
TTC TCT CTT TTA TAT ATT TTC TCA CAT ATT TTG TGA GAT ATT TTG TGA GAT ATT TTC TCT CTT TTA TAT ATT TTT TT

Assembled sequence:
TTCTTATTCATTGATTGATTCTTATTT

This sequence contains each of the following reads:
reads = ['ATTCA', 'ATTGA', 'CATTG', 'CTTAT', 'GATTG', 'TATTT', 'TCATT', 'TCTTA', 'TGATT', 'TTATT', 'TTCAT', 'TTCTT', 'TTGAT']



Step 2.6:

There are multiple approaches for accurately reconstructing a genome sequence.  First, coverage can be increased to ensure that each base pair in the genome is sequenced.  Ideally, each base pair should have a coverage larger than 1, as this will reduce the risk of sequencing errors being integrated into the final, assembled sequence.  More advanced sequencing approaches can also be utilized to overcome common genome assembly obstacles, such as repetitive regions.  These include paired end sequencing, which generates reads on both ends of a fragment to get a better understanding of the entire fragment's genomic location, and long read sequencing, which generates longer reads.  These approaches can overcome the difficulty of assembling reads within repetitive regions, as longer reads are less likely to map to multiple sites in the genome.  Lastly, advanced assembly algorithms, such as de Bruijn graph-based assemblers, are essential for identifying overlaps between these regions and assembling the genome.



Step 3.1:


Prompt for ChatGPT:

Hey Chat, please write an essay on why I'm interested in genomics.  Include the references you use as a works cited section at the end of the essay.


Output from ChatGPT:

Title: Exploring the Genomic Frontier: A Personal Journey into Genomics

Introduction:

Genomics, the study of an organism's complete set of genes and their functions, has captivated my interest for its transformative potential in understanding life at its most fundamental level. As we delve into the intricacies of DNA, genes, and their complex interplay, the promise of genomics to revolutionize medicine, agriculture, and our understanding of life's diversity becomes increasingly evident.

Body:

Unlocking the Blueprint of Life:
The allure of genomics lies in its ability to decipher the genetic code, the blueprint that orchestrates the development, function, and evolution of living organisms. The Human Genome Project, a monumental collaborative effort, marked a watershed moment in genomics, providing the first comprehensive map of the human genome. This accomplishment has paved the way for a deeper comprehension of genetic variations, disease susceptibility, and the intricate mechanisms governing health and disease.
Precision Medicine:
Genomics serves as the cornerstone for precision medicine, a paradigm shift from the one-size-fits-all approach to healthcare. By analyzing an individual's genomic makeup, clinicians can tailor treatment plans to match the specific genetic characteristics of patients. This promises more effective interventions with fewer side effects, heralding a new era in medical care.
Unraveling the Secrets of Evolution:
The study of genomics unravels the evolutionary tapestry that connects all living organisms. Comparative genomics enables scientists to trace commonalities and differences in the genetic codes of diverse species, shedding light on evolutionary relationships. This knowledge has profound implications for biodiversity conservation, agriculture, and our understanding of the interconnectedness of life on Earth.
Genomic Agriculture:
Agriculture stands to benefit significantly from genomics, with the potential to engineer crops for enhanced yield, resistance to diseases, and adaptability to changing climates. By unraveling the genetic makeup of plants and animals, we gain the insights needed to develop resilient and sustainable agricultural practices, crucial for addressing global food security challenges.
Conclusion:

In conclusion, my fascination with genomics stems from its capacity to unravel the mysteries of life, empower precision medicine, illuminate evolutionary history, and revolutionize agriculture. As we stand on the cusp of unprecedented breakthroughs in genomic research, my enthusiasm for exploring the genomic frontier continues to grow.

Works Cited:

International Human Genome Sequencing Consortium. (2001). Initial sequencing and analysis of the human genome. Nature, 409(6822), 860–921.
Collins, F. S., Morgan, M., & Patrinos, A. (2003). The Human Genome Project: Lessons from Large-Scale Biology. Science, 300(5617), 286–290.
Ginsburg, G. S., & Phillips, K. A. (2018). Precision Medicine: From Science to Value. Health Affairs, 37(5), 694–701.
Venter, J. C., Adams, M. D., Myers, E. W., et al. (2001). The Sequence of the Human Genome. Science, 291(5507), 1304–1351.
Varshney, R. K., Ribaut, J.-M., Buckler, E. S., Tuberosa, R., Rafalski, J. A., & Langridge, P. (2012). Can genomics boost productivity of orphan crops? Nature Biotechnology, 30(12), 1172–1176.



Step 3.2:

ChatGPT's response for this prompt is mostly logical, but I would have written an essay with this prompt differently.  Chat uses sensational phrases throughout the paper, which does not reflect the mindset of someone who is informed on both the prospects and limitations of genomics.  Furthermore, Chat brushes over a few of the major applications of genomics without mentioning the diverse ways that genomics approaches have been integrated into biology research.  While the cited papers are real, they mostly discuss the Human Genome Project.  This effort significantly improved our understanding of the human genome, but more recent efforts have used new technologies to provide a more complete representation of our genome.  In an essay where someone is explaining why they are interested in genomics, these recent endeavors should be discussed more.