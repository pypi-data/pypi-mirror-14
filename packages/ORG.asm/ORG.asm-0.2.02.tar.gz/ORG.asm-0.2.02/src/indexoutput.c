/*
 * indexoutput.c
 *
 *  Created on: 18 sept. 2012
 *      Author: coissac
 */

#include "orgasm.h"

void writeOrdoredSequences(buffer_t *buffer,FILE* output)
{

	uint32_t i;
	uint32_t nextprint=DISPLAYSTEP;
	char* record;

	fprintf(stderr,"\nWriting sorted sequence reads...\n\n");

	for (i=0; i < buffer->readCount; i++)
	{
		if (i > nextprint)
		{
			fprintf(stderr,"%9d sequences read\r",nextprint);
			nextprint+=DISPLAYSTEP;
		}

		record = buffer->records + buffer->order1[i] * buffer->recordSize;
		fwrite(record,buffer->recordSize,1,output);
	}

	fprintf(stderr,"%9d sequences read\n",i);

}

void writeOrder1(buffer_t *buffer,FILE* output)
{
	fwrite(buffer->order1,buffer->readCount,sizeof(uint32_t),output);
}

void writeOrder2(buffer_t *buffer,FILE* output)
{
	fwrite(buffer->order2,buffer->readCount,sizeof(uint32_t),output);
}

void writePairData(buffer_t *buffer,FILE* output)
{
	fprintf(stderr,"\nWriting sequence pairing data...\n\n");

	writeOrder2(buffer,output);

	fprintf(stderr,"Done.\n");
}

void writeOrderData(buffer_t *buffer,FILE* output)
{
	fprintf(stderr,"\nWriting sequence suffix index...\n\n");

	writeOrder1(buffer,output);

	fprintf(stderr,"Done.\n");
}

void writeGeneralData(buffer_t *buffer,FILE* output)
{
	fprintf(stderr,"\nWriting global data...\n\n");

	fwrite(buffer,1,sizeof(buffer_t),output);

	fprintf(stderr,"Done.\n");
}
