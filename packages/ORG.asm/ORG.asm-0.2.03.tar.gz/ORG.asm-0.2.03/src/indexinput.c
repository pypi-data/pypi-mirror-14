/*
 * indexinput.c
 *
 *  Created on: 21 sept. 2012
 *      Author: coissac
 */


#include "orgasm.h"

void loadSequences(buffer_t *buffer,FILE* input)
{
	char*    records = buffer->records;
	uint32_t nreads;

	fprintf(stderr,"\nReading indexed sequence reads...\n\n");

	nreads = (uint32_t)fread(records,buffer->recordSize,buffer->readCount,input);
	ASSERT(nreads==buffer->readCount,"Error in the indexed sequence read file %s","");

	fprintf(stderr,"%9zd sequences read\n",buffer->readCount);

	fillOrdored(buffer);

}


uint32_t loadOrder1(buffer_t *buffer,FILE* input)
{
	return fread((void*)buffer->order1,sizeof(uint32_t),buffer->readCount,input);
}

uint32_t loadOrder2(buffer_t *buffer,FILE* input)
{
	return fread((void*)buffer->order2,sizeof(uint32_t),buffer->readCount,input);
}

void loadPairData(buffer_t *buffer,FILE* input)
{
	uint32_t nreads;

	fprintf(stderr,"\nReading indexed pair data...\n\n");

	nreads = loadOrder2(buffer,input);
	ASSERT(nreads==buffer->readCount,"Error in the indexed pair data file %s","");

	fprintf(stderr,"Done.\n");
}

void loadGeneralData(buffer_t *buffer,FILE* input)
{
	fprintf(stderr,"\nLoading global data...\n\n");

	fread(buffer,1,sizeof(buffer_t),input);

	fprintf(stderr,"Done.\n");
}
