'''
A naive implmentation of vASM which is a pairing-based accountable subgroup multi-signature scheme.
--------------------------------------------------------------------------------------------------------
Thanks to:
https://hackmd.io/@benjaminion/bls12-381#Swapping-G1-and-G2
https://tools.ietf.org/id/draft-yonezawa-pairing-friendly-curves-00.html#rfc.section.2.1
https://github.com/Chia-Network/bls-signatures/tree/master/python-impl
---------------------------------------------------------------------------------------------------------
'''

from random import randint
from fields import Fq, Fq2, Fq12
from bls12381 import q,a,b,gx,gy,g2x,g2y,n,h,h_eff, k, parameters
from ec import default_ec, default_ec_twist, bytes_to_point, G2Infinity, G1Generator, G2Generator,scalar_mult_jacobian,G1FromBytes, G2FromBytes, point_to_bytes, add_points_jacobian,y_for_x, JacobianPoint
from pairing import ate_pairing
from util import hash256, hash512

#generators
g1 = G1Generator(default_ec)
g2 = G2Generator(default_ec_twist) 

""" 
Suppose that there is a group G of users, and a subgroup S of G wants to sign a common message. 
All users compute their public and private key pairs independently. Then they set up a 1-round 
communication in order to compute their membership keys jointly. 
"""

#Key Generation
def KeyGeneration(n,skList = [],pkList = []):
	for i in range(n):
		skList.append(randint(1,q-1))

	for i in range(n):
		pkList.append(skList[i]*g2)
	print ('Key Generation is completed.')

#Group Setup 
def GroupSetup(skLis, pkLis, mKe = [], ComLis=[]):
	#Assume that each user in G chooses coefficients for his secret polynomial.
	coeff=[]
	for i in range(len(skLis)):
		coeff.append(skLis[i])
		for j in range(len(skLis)-1):
			coeff.append(randint(1,q-1))

	#evaluations of the secret polynomials
	lisEval = []
	for i in range(len(skLis)):
		for j in range(len(skLis)):
			evl = 0
			for k in range(len(skLis)):
				evl = evl + coeff[i*len(skLis)+k]*(j+1)**k
			lisEval.append(evl)

	#computing membership keys
	for i in range (len(skLis)):
		aaa = 0
		for j in range(0,len(lisEval),len(skLis)):
			aaa = aaa + lisEval[i+j]
		mKe.append(aaa)

	#Individual commitments of the users' secret polynomials
	lisCom = []
	for i in range (len(coeff)):
		lisCom.append(coeff[i]*g2)

	#aggregating individual commitments
	for i in range (len(mKe)):
		aaa = 0
		for j in range(0,len(lisCom),len(mKe)):
			aaa = aaa + lisCom[i+j]
		ComLis.append(aaa)

	#consitency check
	chck1= []
	for i in range (len(mKe)):
		tre = mKe[i]*g2
		chck1.append(tre)

	df = G2Infinity()
	chck2=[]
	for i in range (len(mKe)):
		for j in range(len(mKe)):
			df = df + ((i+1)**j)*ComLis[j]
		chck2.append(df)

	if ComLis[0] == sum(pkLis):
		for i in range(len(mKe)):
			if chck1[i]==chck2[i]:
				print('Membership keys are consistent. Group Setup is completed.')
				return mKe
	else:
		print ('Shared secrets have to be the secret keys of the users. Restart the group setup.')


def SignatureGeneration(SubGr,message,mklist):
	#message as point in G1
	msgp = scalar_mult_jacobian(int.from_bytes((hash256(message) + hash256(message)[16:]), byteorder="big"), g1, default_ec, Fq)

	#individual signatures of each user in subgroup S
	signInd=[]
	for i in SubGr:
		signInd.append(mklist[i-1]*msgp)

	#return aggrerated signature as a point in G1
	return sum(signInd)

#Verification
def Verify(mesgs,AggS,Sub,ComL):
	#mapping message on the group G1
	message = scalar_mult_jacobian(int.from_bytes((hash256(mesgs) + hash256(mesgs)[16:]), byteorder="big"), g1, default_ec, Fq)

	summed = G2Infinity()
	for i in Sub:
		for j in range(len(ComL)):
			summed = summed + ((i)**j)*ComL[j]

	#ate pairing: e(p2,p1,EC) as elements in Fq12 
	v1 = ate_pairing(message, summed, default_ec)
	v2 = ate_pairing(AggS, g2, default_ec)

	#verification
	if v1 == v2:
		print ('Signature is valid.')	
	else:
		print ('Signature is NOT valid.')


#WLOG assume that group G has 5 users.
skList = []
pkList = []
KeyGeneration(5,skList,pkList)

mkList = []
ComList = []
GroupSetup(skList, pkList, mkList, ComList)

#message to be signed
msg = b'Hello world.'

#Assume that S={1,2,3} is the subgroup of indices of signers
SubG=[1,2,3]
AggSign = SignatureGeneration(SubG,msg,mkList)

Verify(msg,AggSign,SubG,ComList)