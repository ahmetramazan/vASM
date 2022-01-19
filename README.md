# vASM
An Accountable Subgroup Multi-signature Scheme with Verifiable Group Setup

An accountable multi-signature (ASM) is a multi-signature scheme in which any subgroup S of a group G jointly sign a message m, ensuring that each member of S is accountable for the resulting signature. This notion was firstly defined by Micali et al. by proposing the first ASM scheme in 2001. In a more recent paper Boneh, Drijvers and Neven proposed another ASM scheme which is based on BLS signature and solves the open problem of constructing an ASM scheme in which the subgroup S is not determined before the signature generation. We propose The first one is vASM (verifiable ASM) scheme which is indeed a modified BLS signature. We give a method of generating a membership key via VSS protocol, which transforms BLS signature scheme into an ASM scheme. The proposed vASM scheme, which also solves the above mentioned open problem, requires fewer group operations and bilinear pairings than the ASM schemes proposed by Boneh et al. You can find details in https://eprint.iacr.org/2022/018

I provide here a naive implementation with SageMath and Python. Any feedbacks and contributions are welcome.


