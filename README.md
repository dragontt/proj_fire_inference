# proj_fire_inference

Inferring highly informative TF motifs is the essential intermediate step to build the regulatory edges of all TFs to their target genes. The approach presented in this document, modifies existing motif inference program FIRE by constraining the seeding procedure. The constraint allows the input seeds to possess only specific sequence pattern, according to the DNA binding domain (DBD) family that each TF belongs to. To our knowledge, FIRE among the prevalent motif inference programs, is the most feasible software utilizing the direct and functional binding data generated in NetProphet.

DBD family sequence prior is used to modify FIRE k-mer seeds. More specifically, SGD TF database that contains DNA binding domain family is compiled to give information of individual TF; and TF DBD prior is manually curated from literature and online resource; then combination of both datasets yields the prioritized seeds for each protein family. Accordingly, those seeds of k-mer sizes from 5 to 8 are applied to FIRE inference respectively. Meanwhile, FIRE utilizes ChIP positive-negative data and discretized NetProphet data independently for mutual information computation and optimization. NetProphet then constructs a new regulatory network, by using motifs discovered in FIRE using the discrete NetProphet scores, in addition to coexpression from discrete cluster of gene expression data, and difference expression from gene perturbation. And the new network is fed back to FIRE. This process is repeated between motif inference and network mapping algorithms. Ultimately, we expect this pipeline to demonstrate its ability to output the best network and motif.

Both collections of inferred motifs independently using ChIP and NetProphet data are aligned to and evaluated against the ground truth PWMs, which are primarily curated in ScerTF database and complementarily in YeTFaSCo database. The motif evaluation calculates 2 scores; each is a combination of 3 FIRE scores and 3 TOMTOM alignment scores respectively. Each evaluation score of using DBD family prior is compared with the one without using constraint. Then a compound score of the 2 comparison scores determines whether applying protein family prior information improves the motif inference for each TF.

Check write-up for details.