Step 1.1:

Bash command used:

Rscript runChicago.R raw/PCHIC_Data/GM_rep1.chinput,raw/PCHIC_Data/GM_rep2.chinput,raw/PCHIC_Data/GM_rep3.chinput chicago  --design-dir raw/Design --en-feat-list raw/Features/featuresGM.txt --export-format washU_text



Step 1.2:

My significant interactions from this PCHiC data seem to overlap with histones containing activating modifications, such as H3K27ac, H3K4me1, and H3K4me3, about twice as often as histones with repressive modification and chromatin boundary proteins, such as H3K9me3 and CTCF.  This pattern is expected, as genomic regions bound by histones with repressive modifications have compacted chromatin that is less conducive to significant interactions between promoters and promoter-binding regions, such as enhancers, and boundary proteins like CTCF inhibit interactions on either side of that bound genomic region.



Step 2.2:

Top 6 Promoter-Promoter Interactions:
1. Interacting fragments: 'chr20,44562442,44565593 chr20,44438565,44442365'; Interaction Score: 34.77
2. Interacting fragments: 'chr20,44596299,44607204 chr20,44438565,44442365', Interaction Score: 34.29
3. Interacting fragments: 'chr21,26837918,26842640 chr21,26926437,26939577', Interaction Score: 34.02
4. Interacting fragments: 'chr20,44562442,44565593 chr20,44452862,44471524', Interaction Score: 33.89
5. Interacting fragments: 'chr20,17946510,17951709 chr20,17660712,17672229', Interaction Score: 33.85
6. Interacting fragments: 'chr20,24972345,24985047 chr20,25036380,25043735', Interaction Score: 33.84

Top 6 Promoter-Enhancer Interactions:
1. Interacting fragments: 'chr21,26926437,26939577 chr21,26797667,26799364'; Interaction Score: 33.13; Associated Gene(s): MIR155HG
2. Interacting fragments: 'chr20,55957140,55973022 chr20,56067414,56074932'; Interaction Score: 32.29; Associated Gene(s): RBM38, RP4-800J21.3
3. Interacting fragments: 'chr21,26926437,26939577 chr21,26790966,26793953'; Interaction Score: 29.17; Associated Gene(s): MIR155HG
4. Interacting fragments: 'chr20,5585992,5601172 chr20,5625693,5628028'; Interaction Score: 28.88; Associated Gene(s): GPCPD1
5. Interacting fragments: 'chr21,26926437,26939577 chr21,26793954,26795680'; Interaction Score: 26.23; Associated Gene(s): MIR155HG
6. Interacting fragments: 'chr20,5929472,5933156 chr20,5515866,5523933'; Interaction Score: 26.08; Associated Gene(s): MCM8, TRMT6



Step 2.3:

2 Promoter-Enhancer Interactions of Interest:

1. Interacting fragments: 'chr20,55957140,55973022 chr20,56067414,56074932'; Interaction Score: 32.29; Associated Gene(s): RBM38;RP4-800J21.3

This promoter-enhancer interaction seems to be regulating transcription of RBM38, with the promoter sequence of RBM38 serving as bait in this interaction.  RBM38 is highly expressed in the bone marrow, which is consistent with strong promoter-enhancer interactions in our B-cell derived GM12878 cell line.  RBM38 is thought to be involved in the DNA damage response and negative regulation of proliferation.  Given it's expression pattern and functions consistent with B-cell origins and characteristics, it makes sense that RBM38 is interacting with enhancers and likely producing transcripts in the GM12878 line. 


2. Interacting fragments: 'chr20,5585992,5601172 chr20,5625693,5628028'; Interaction Score: 28.88; Associated Gene(s): GPCPD1

This promoter-enhancer interaction is likely regulating transcription of GPCPD1, a gene that is primarily thought to be involved in glycerophosphocholine phosphodiesterase activity, glycerophospholipid catabolism, and skeletal muscle development.  Expression of GPCPD1 is ubiquitous in the bone marrow, which suggests expression in B-cells and can explain GPCPD1's strong interactions with enhancers and likely transcriptoin in the B-cell derived GM12878 line.