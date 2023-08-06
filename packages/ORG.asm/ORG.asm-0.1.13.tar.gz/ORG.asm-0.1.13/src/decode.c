/*
 * decode.c
 *
 *  Created on: 24 sept. 2012
 *      Author: coissac
 */



#include "orgasm.h"

/**
 * decode a sequence encoded in the two bits format.
 *
 * buffer   : pointer to the sequence buffer containing sequences
 * recordid : position of the sequence in the buffer
 * begin    : first nucleotide to decode
 * length   : length of the sequence to decode
 * dest     : a pointer to a memory area where the function saves
 *            the decodes sequence. if dest is NULL, then an internal
 *            buffer is used. If dest is specified it must point to
 *            a memory area at least large enough to store a full read
 *
 * Returns  : a pointer to the decoded sequence. The sequence is returned
 *            as a NULL terminated string. The returned pointer is not
 *            always equal to dest and can point to an internal part of
 *            the destination buffer
 */
char * decode(buffer_t *buffer, uint32_t recordid, uint32_t begin, int32_t length, char *dest)
{
	static char internal[MAXREADLEN+9];
	uint64_t*   idest;
	uint32_t    from;
	uint32_t    shift;
	uint32_t    i;
	uint32_t    lcompact;
//	uint32_t    mask;
	uint16_t    *compactseq;

	if (dest==NULL) dest = internal;

	dest = (char*)PTR8(dest);
	idest = (uint64_t*)dest;

	from = recordid * buffer->recordSize + ((begin >> 2) & 0xFFFFFFFE);
	shift = begin & 7;
	lcompact = (length+shift) / 8 + (((length+shift) & 7) ? 1:0);

	for (compactseq = (uint16_t*)(buffer->records + from), i=0;
		 i < lcompact;
		 compactseq++,i++, idest++)
		*idest=decode16bitsnuc[*compactseq];

	dest[length + shift]=0;

	return dest + shift;
}


char *decodeComp(buffer_t *buffer, uint32_t recordid, uint32_t begin, int32_t length, char *dest)
{
	static char internal[MAXREADLEN+9];
	       char internal2[MAXREADLEN+9];
	uint64_t*   idest;
	uint32_t    from;
	uint32_t    shift;
	int32_t     i;
	uint32_t    lcompact;
//	uint32_t    mask;
	uint16_t    *compactseq;
	size_t      lkey;
	char*       key;
	char*       dest2;

	if (dest==NULL) dest = internal;

	dest = (char*)PTR8(dest);
	dest2 = (char*)PTR8(internal2);
	idest = (uint64_t*)dest;

	from = buffer->readSize - begin;

	// lkey -> length of the compacted sequence to unpack
	// old  version potentially with a bug
	// lkey = CODELENGTH(buffer->readSize) - (begin >> 2) + 1;
	lkey = CODELENGTH(from);

	// key -> pointer to the byte of the compacted sequence containing
	//        the position begin on the complementary sequence
	// old  version potentially with a bug
	// key  = READEND(buffer,buffer->order1[recordid]) - (begin >> 2);
	key  = READSTART(buffer,buffer->order1[recordid])+lkey-1;


	// reverse complement the read in the dest2 buffer in a compact form
	for (i=0; i<lkey;i++)
		dest2[i]=complement4nuc[*(((uint8_t*)(key)-i))];

	// (buffer->readSize & 3) : base count encoded by the last byte

	// old  version potentially with a bug
	// shift = (begin & 3) + (buffer->readSize & 3);
	shift = (4 - (from & 3)) & 3;


    ASSERT (shift <4,"There is a bug readsize = %zu begin = %d shift=%d",buffer->readSize,begin,shift)

	lcompact = (length+shift) / 8 + (((length+shift) & 7) ? 1:0);

	for (compactseq = (uint16_t*)(dest2), i=0;
		 i < lcompact;
		 compactseq++,i++, idest++)
		*idest=decode16bitsnuc[*compactseq];

	dest[length + shift]=0;

	return dest + shift;
}

char *getRead(buffer_t *buffer, int32_t recordid, uint32_t begin, int32_t length, char *dest)
{
	static char internal[MAXREADLEN+9];

	if (dest==NULL)
		dest = internal;

	if (recordid > 0)
	{
		recordid--;
		return decode(buffer, recordid, begin, length, dest);
	}
	else if(recordid < 0)
	{
		recordid=-recordid;
		recordid--;
		recordid=buffer->complement[recordid];

		return decodeComp(buffer, recordid, begin, length, dest);
	}

	return NULL;
}

char * decodeSequence(pnuc buffer, uint32_t begin, int32_t length, char *dest)
{
	static char internal[MAXREADLEN+20];
	uint64_t*   idest;
	uint32_t    from;
	uint32_t    shift;
	uint32_t    i;
	uint32_t    lcompact;
//	uint32_t    mask;
	uint16_t    *compactseq;

	if (dest==NULL) dest = internal;

	dest = (char*)PTR8(dest);
	idest = (uint64_t*)dest;

	from = ((begin >> 2) & 0xFFFFFFFE);
	shift = begin & 7;
	lcompact = (length+shift) / 8 + (((length+shift) & 7) ? 1:0);

	for (compactseq =(uint16_t*)(buffer + from), i=0;
		 i < lcompact;
		 compactseq++,i++, idest++)
		*idest=decode16bitsnuc[*compactseq];

	dest[length + shift]=0;

	return dest + shift;
}

