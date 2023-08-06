/*
 * fastq.c
 *
 *  Created on: 11 juil. 2012
 *      Author: coissac
 */

#include <stdio.h>
#include <inttypes.h>
#include <string.h>

#include "orgasm.h"

#include "debug.h"

/**
 *
 *  This simple fastq reader assume that sequence and quality are stored
 *  on a single line and only read the sequence from the file not the quality
 *
 *	dest    : a pointer to a memory zone where the read sequence
 *	          will be stored
 *
 *	in      : the input file from which sequences are read
 *
 *	maxsize : the maximal size of the read sequence
 *
 *  The function return the length of the sequence or 0 on error
 */

uint32_t readFastq(char* dest, FILE* in, int32_t maxsize)
{

	char* buffer;
	size_t lseq;

	// Look for the first fastq sequence header starting
	// with a @

	buffer = fgetln(in,&lseq);

	while(buffer!=NULL && buffer[0]!='@')
		buffer = fgetln(in,&lseq);

	// We check if we are on error

	if (buffer==NULL)
		return 0;

	// Then we read the sequence on one line

	buffer = fgets(dest,maxsize,in);
	lseq=strlen(buffer);

	// Then two lines are skipped for the quality

	buffer = fgetln(in,&lseq);
	buffer = fgetln(in,&lseq);

	if (lseq > 0)
		{
			lseq--;
			dest[lseq]=0;
		}

	return lseq;

}

/**
 *
 *  This function read paired fastq file using the readFastq function
 *  encoded above
 *
 *	dest    : a pointer to a memory zone where the read sequence
 *	          will be stored
 *
 *	forward : the input file from which forward sequences are read
 *
 *	reverse : the input file from which reverse sequences are read
 *
 *	maxsize : the maximal size of the read sequence
 *
 *  The function return the length of the forward sequence or 0 on error
 *  Different read length for forward and reverse reads is considered as
 *  an error.
 */

uint32_t readPairedFastq(char* dest,
		 	 	 	     FILE* forward,
		 	 	 	     FILE* reverse,
		 	 	 	     int32_t maxsize,
		 	 	 	     uint32_t readLength)
{
	int32_t forwardLength;
	int32_t forwardLength16;
	int32_t reverseLength=0;
	char*   rdest;
	char*   c;
	int32_t rsize;

	bzero(dest,maxsize);

	if (readLength > 0)
	{

		/* If the read length is even then shorten it by one base */
	    if ((readLength & 1) ==0)
	    {
	    	readLength--;
	    	fprintf(stderr,"Read length adjusted to %d\n",readLength);
	    }

		forwardLength16 = round16(readLength);

		if (forwardLength16*2 > maxsize)
			return 0;

		rdest = dest + forwardLength16;
		rsize = maxsize - forwardLength16;
	}
	else
		forwardLength16=0;


	// we read the forward sequence

	do {

        // Skip the too short reads
		for (forwardLength = readFastq(dest,forward,maxsize);
			 forwardLength>0 && forwardLength<readLength;
			 forwardLength = readFastq(dest,forward,maxsize))
			// skip the reverse read and take the next forward
			reverseLength = readFastq(dest,reverse,maxsize);

		// If readLength is not specify set up it from the length of the first sequence
		if (forwardLength16==0)
		{
			readLength = forwardLength;
			/* If the read length is even then shorten it by one base */
		    if ((readLength & 1) ==0)
		    {
		    	readLength--;
		    	fprintf(stderr,"Read length adjusted to %d\n",readLength);
		    }

			forwardLength16 = round16(readLength);
			if (forwardLength16*2 > maxsize)
				return 0;

			rdest = dest + forwardLength16;
			rsize = maxsize - forwardLength16;
		}



		// founded a good forward get the corresponding reverse
		reverseLength = readFastq(rdest,reverse,rsize);

		} while ( forwardLength > 0 &&
		 	      reverseLength > 0 &&
		 	      reverseLength < readLength );

	// No more sequences
	if (forwardLength==0 || reverseLength==0)
		return 0;

	if ((forwardLength >= readLength) && (reverseLength >= readLength)) {
		for (c=dest+readLength;
			  c < rdest;
			  c++) *c=0;

		for (c=rdest+readLength;
			  c < (dest+maxsize);
			  c++) *c=0;
	}

	// we return the length of one read
	return readLength;

}

uint8_t checkACGT(const char* src, size_t size)
{
	size_t  i;
	uint8_t rep=TRUE;

	size/=16;

	for (i=0;rep && i < size; i++, src+=16)
		rep &= is16ACGT(src);

	return rep;
}

buffer_t * loadPairedFastq(FILE* forward,
 			 		       FILE* reverse,
 			 	 	 	   size_t maxread,
					       size_t maxbuffersize,
					       uint32_t readLength
		                  )
{

		// We allocate on the stack an over sized buffer for the
	    // ascii sequence

#define MASK  ((size_t)0xF)
#define CLEAN ((size_t)~MASK)

	char     readbuffer[2048];

	uint32_t buffersize;
	char*    reads;
	char*    index;
	char*    bufferend;
//	uint32_t readLength;
	uint32_t recordLength;
	uint32_t nextprint=0;
	uint32_t* encodedseqs;
	buffer_t* seqbuffer;


	fprintf(stderr,"\nReading sequence reads...\n\n");

	// we compute the first aligned address on 16 bytes word
	// include in the buffer

	reads = (char*) &readbuffer;
	if ((size_t)reads & MASK)
		reads = (char*)(((size_t)reads & CLEAN) + 0x10);

			// we adjust the buffer size according to the alignment

	buffersize= 2048 - (reads - (char*)(&readbuffer));

	readLength = readPairedFastq(reads,forward,reverse,buffersize,readLength);

	seqbuffer  = newBuffer(maxbuffersize,readLength,maxread);
	encodedseqs= (uint32_t*)(seqbuffer->records);

	printf("maximum reads : %zu\n",seqbuffer->maxrecord);


	while (readLength && (seqbuffer->readCount+2) <= seqbuffer->maxrecord)
	{
		if (seqbuffer->readCount > nextprint)
		{
			fprintf(stderr,"%9d sequences read\r",nextprint);
			nextprint+=DISPLAYSTEP;
		}

		recordLength = round16(readLength)*2;
		bufferend = reads + recordLength;
		if (checkACGT(reads,recordLength))
		{
			for (index=reads; index < bufferend; index+=16, encodedseqs++)
				*encodedseqs=encode16nuc(index);

			seqbuffer->readCount+=2;
		}

		readLength = readPairedFastq(reads,forward,reverse,buffersize,readLength);
		//DEBUG("Filled %d/%d",seqbuffer->readCount,seqbuffer->maxrecord);
	}


	fprintf(stderr,"%9zd sequences read\n",seqbuffer->readCount);

	return seqbuffer;

#undef MASK
#undef CLEAN
}
