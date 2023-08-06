/*
 * load.c
 *
 *  Created on: 3 oct. 2012
 *      Author: coissac
 */

#include "orgasm.h"

void indexReverseComplement(buffer_t *reads)
{
	int32_t i;

	if (reads->complement)
		FREE(reads->complement);

	reads->complement=(uint32_t*) MALLOC(sizeof(uint32_t) * reads->readCount);

	for (i=0;i < reads->readCount; i++)
		reads->complement[reads->order1[i]]=i;
}
buffer_t *loadIndexedReads(const char *indexname)
{
	buffer_t tmp;
	buffer_t *reads;
	char *indexFileName;
	FILE *index;
	size_t maxsize;

	//
	// Read the general data about the sequence index
	//

	asprintf(&indexFileName,"%s.ogx",indexname);
	if (indexFileName == NULL)
		FATALERROR("Cannot allocate memory for file name %s",indexname);

	index = fopen(indexFileName,"r");
	if (index == NULL)
		FATALERROR("Cannot open file %s",indexFileName);

	loadGeneralData(&tmp,index);

	free(indexFileName);
	fclose(index);

	maxsize = (tmp.recordSize  + \
			   2 * sizeof(uint32_t)) * tmp.readCount + 48;

	reads = newBuffer(maxsize,tmp.readSize,0);

	reads->readCount = tmp.readCount;

	//
	// Read the forward sequence data
	//

	asprintf(&indexFileName,"%s.ofx",indexname);
	if (indexFileName == NULL)
		FATALERROR("Cannot allocate memory for file name %s",indexname);

	index = fopen(indexFileName,"r");
	if (index == NULL)
		FATALERROR("Cannot open file %s",indexFileName);

	loadSequences(reads,index);

	fclose(index);
	free(indexFileName);

	//
	// Read the pair-end data --> into order2
	//

	asprintf(&indexFileName,"%s.opx",indexname);
	if (indexFileName == NULL)
		FATALERROR("Cannot allocate memory for file name %s",indexname);

	index = fopen(indexFileName,"r");
	if (index == NULL)
		FATALERROR("Cannot open file %s",indexFileName);

	loadPairData(reads,index);

	fclose(index);
	free(indexFileName);

	//
	// Read index for the reverse complemented sequences --> into order1
	//

	asprintf(&indexFileName,"%s.orx",indexname);
	if (indexFileName == NULL)
		FATALERROR("Cannot allocate memory for file name %s",indexname);

	index = fopen(indexFileName,"r");
	if (index == NULL)
		FATALERROR("Cannot open file %s",indexFileName);

	fprintf(stderr,"\nLoading reverse index...\n\n");
	loadOrder1(reads,index);
	fprintf(stderr,"Done.\n");

	fclose(index);
	free(indexFileName);

	reads->complement=NULL; // Provisoire...

	fprintf(stderr,"\nIndexing reverse complement sequences ...\n\n");
	indexReverseComplement(reads);

	fprintf(stderr,"\nFast indexing forward reads...\n\n");
	indexForward(reads);
	fprintf(stderr,"\nFast indexing reverse reads...\n\n");
    indexReverse(reads);
	fprintf(stderr,"Done.\n");

	return reads;
}
