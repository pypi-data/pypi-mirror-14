/*
 * orgasmi.c
 *
 *  Created on: 11 juil. 2012
 *      Author: coissac
 */

#include <stdio.h>
#include <string.h>
#include "orgasm.h"

#include "debug.h"

//#define LARGE_TEST
#define LOAD_ONLY

int main(int argc, char *argv[])
{
	FILE* forward;
	FILE* reverse;
	FILE* index;
	buffer_t* reads;
	uint32_t i;
	const char* indexfiles;
	char query[500];
	char key[500];
	char *akey;
	char *aquery;
	int32_t eol;
	int32_t pos;
	int32_t pnext;
	char *toto;


#define CMPLENGTH 100

#ifdef LARGE_TEST
//	char* forwardFileName="/Users/coissac/travail/GuillaumeBesnard/lecontella/120824_SN365_A_L005_GWM-9_R1.fastq";
//	char* reverseFileName="/Users/coissac/travail/GuillaumeBesnard/lecontella/120824_SN365_A_L005_GWM-9_R2.fastq";
	char* forwardFileName="/Users/coissac/travail/GuillaumeBesnard/Sartidia/Spe_CAGATC_L001_R1.fastq";
	char* reverseFileName="/Users/coissac/travail/GuillaumeBesnard/Sartidia/Spe_CAGATC_L001_R2.fastq";
	indexfiles = "/Users/coissac/encours/orgasm/samples/sartidia";
	indexfiles = "/Users/coissac/encours/orgasm/samples/locontella";
#define MAXREAD 2000000000

#else
	char* forwardFileName="/Users/coissac/encours/orgasm/samples/5_1.fastq";
	char* reverseFileName="/Users/coissac/encours/orgasm/samples/5_2.fastq";

	indexfiles = "/Users/coissac/encours/orgasm/samples/5";

#define MAXREAD 1000000000
#endif

#ifndef LOAD_ONLY

	reads = buildIndex(forwardFileName,reverseFileName,indexfiles,95,MAXREAD);

	freeBuffer(reads);

#endif

//	reads = loadIndexedReads(indexfiles);
//	akey = "CCTGAGTGAAAAAGATACCGCGAGAACGATCTTTTTCAATAAAATCATCGCGCAATAAATCAACAAAACCTAAAGTAATTTCGCGTTCCCCTTCTAACTT";
//	//      TTTGTAAAgt
//	//      acTTTACAAA
//
//	printf("%9d, %s\n",0,akey);
//
//	pnext = lookForString(reads, akey, CMPLENGTH, &eol);
//	i=0;

//	printf ("pos = %d -> endoflist = %d\n",pnext,eol);
//	printf ("--> %s\n 0 :%s\n",akey,decode(reads, pnext-1, 0, CMPLENGTH, 0));
//	printf ("-1 :%s\n",decode(reads, pnext-2, 0, CMPLENGTH, 0));
//	printf ("+1 :%s\n",decode(reads, pnext, 0, CMPLENGTH, 0));
//
//	while (pnext > 0 && eol==0)
//	{
//		i++;
//		pos = pnext;
//		pnext = nextRead(reads, pos, CMPLENGTH, &eol);
//	}
//
//	printf ("pos = %d -> endoflist = %d\n",pos,eol);
//	printf ("--> %s\n 0 :%s\n",akey,decode(reads, pos-1, 0, CMPLENGTH, 0));
//	printf ("-1 :%s\n",decode(reads, pos-2, 0, CMPLENGTH, 0));
//	printf ("+1 :%s\n",decode(reads, pos, 0, CMPLENGTH, 0));
//	printf ("read count : %d\n",i);
//
//	while (eol==0)
//	{
//		i++;
//		pos = pnext;
//		printf("%9d, %s\n",pos,getRead(reads, pos, 0, CMPLENGTH, 0));
//		pnext = nextRead(reads, pos, CMPLENGTH, &eol);
//	}
//
//	printf("%9d, %s\n",pos-1,getRead(reads, pos-1, 0, CMPLENGTH, 0));
//	printf("%9d, %s\n",pos+1,getRead(reads, pos+1, 0, CMPLENGTH, 0));
//
//	printf ("\nread count : %d\n",i);
//
//	freeBuffer(reads);

	akey = PTR16(key);
	aquery = PTR16(query);

	bzero(key,500);
	bzero(query,500);

	akey = encodeSequence(akey, "gcgagctgagctagtcgatgctagcatggcgagctgagctagtcgatgctagcatggcgagctgagctagtcgatgctagcatg", 84);

	i = 21;

	aquery = shiftKey(aquery, akey,4, i);
	toto = decodeSequence(aquery, 0, 88, NULL);

	printf ("   %s\n%s\n","gcgagctgagctagtcgatgctagcatggcgagctgagctagtcgatgctagcatggcgagctgagctagtcgatgctagcatg",toto);

	return 0;
}
