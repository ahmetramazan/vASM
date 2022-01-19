# vASM
An Accountable Subgroup Multi-signature Scheme with Verifiable Group Setup

An accountable subgroup multi-signature (ASM) is a kind of multi-signature scheme in which any subgroup S of a group G jointly sign a message m, ensuring that each member of S is accountable for the resulting signature. This notion was firstly defined by Micali et al. by proposing the first ASM scheme (https://www.cs.bu.edu/~reyzin/papers/multisig.pdf) in 2001. In 2018, Boneh, Drijvers and Neven proposed another ASM scheme (https://eprint.iacr.org/2018/483.pdf) which is based on BLS signature and solves the open problem of constructing an ASM scheme in which the subgroup S is not determined before the signature generation. More recently, we propose a novel pairing-based ASM scheme, i.e. vASM (verifiable ASM) scheme, which is indeed a modified BLS signature. We give a method of generating a membership key via VSS protocol, which transforms BLS signature scheme into an ASM scheme. The proposed vASM scheme, which also solves the above mentioned open problem, requires fewer group operations and bilinear pairings than the ASM schemes proposed by Boneh et al. You can find details in https://eprint.iacr.org/2022/018.pdf

I provide here a naive implementation with SageMath and Python. Any feedbacks and contributions are welcome.

Note:
For background information about pairings visit https://www.craigcostello.com.au/tutorials

