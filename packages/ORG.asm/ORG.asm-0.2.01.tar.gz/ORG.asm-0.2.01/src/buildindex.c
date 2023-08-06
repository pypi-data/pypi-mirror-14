/** buildindex.c
 *
 *  Created on: 26 sept. 2012
 *      Author: coissac
 */

#include "orgasm.h"

buffer_t *buildIndex(const char *forwardFileName, const char* reverseFileName,
					    const char *indexname,
		 	 	 	 	uint32_t minword,
		 	 	 	 	size_t maxread,
					    size_t maxbuffersize,
					    uint32_t readLength
					   )
{
	FILE* forward;
	FILE* reverse;
	FILE* index;

	char* indexFileName;

//	uint32_t indexcount;
//	uint32_t i;
	buffer_t *reads;

	forward = fopen(forwardFileName,"r");

	if (forward == NULL)
	FATALERROR("Cannot open file %s",forwardFileName)

	reverse = fopen(reverseFileName,"r");

	if (reverse == NULL)
	FATALERROR("Cannot open file %s",reverseFileName)

	reads = loadPairedFastq(forward,reverse,maxread,maxbuffersize,readLength);

	fclose(forward);
	fclose(reverse);

	sortBuffer(reads);

	asprintf(&indexFileName,"%s.ofx",indexname);
	if (indexFileName == NULL)
		FATALERROR("Cannot allocate memory for file name %s",indexname);

	index = fopen(indexFileName,"w");
	if (index == NULL)
		FATALERROR("Cannot open file %s",indexFileName);

	writeOrdoredSequences(reads,index);

	fclose(index);
	free(indexFileName);

	asprintf(&indexFileName,"%s.opx",indexname);
	if (indexFileName == NULL)
		FATALERROR("Cannot allocate memory for file name %s",indexname);

	index = fopen(indexFileName,"w");
	if (index == NULL)
		FATALERROR("Cannot open file %s",indexFileName);

	writePairData(reads,index);

	fclose(index);
	free(indexFileName);

	asprintf(&indexFileName,"%s.ofx",indexname);
	if (indexFileName == NULL)
		FATALERROR("Cannot allocate memory for file name %s",indexname);

	index = fopen(indexFileName,"r");
	if (index == NULL)
		FATALERROR("Cannot open file %s",indexFileName);

	loadSequences(reads,index);

	fclose(index);
	free(indexFileName);

	compSortBuffer(reads);

	asprintf(&indexFileName,"%s.orx",indexname);
	if (indexFileName == NULL)
		FATALERROR("Cannot allocate memory for file name %s",indexname);

	index = fopen(indexFileName,"w");
	if (index == NULL)
		FATALERROR("Cannot open file %s",indexFileName);

	writeOrderData(reads,index);

	fclose(index);
	free(indexFileName);

//	indexcount = reads->readSize - minword;
//	reads->minword  =minword;
//	reads->suffixidx=indexcount;

	asprintf(&indexFileName,"%s.ogx",indexname);
	if (indexFileName == NULL)
		FATALERROR("Cannot allocate memory for file name %s",indexname);

	index = fopen(indexFileName,"w");
	if (index == NULL)
		FATALERROR("Cannot open file %s",indexFileName);

	writeGeneralData(reads,index);

	free(indexFileName);
	fclose(index);

	indexForward(reads);
    indexReverse(reads);

	return reads;
}

