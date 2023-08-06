/*
 * lookfor.c
 *
 *  Created on: 3 oct. 2012
 *      Author: coissac
 */

#include <string.h>

#include "orgasm.h"
#include "_sse.h"
/**
 * Rigth shift a nucleic sequence encoded with the encode
 * encode.
 *
 * dest : a 16bytes aligned pointer to the place where to store
 *        the shiftedkey. If dest is NULL a static internal buffer
 *        is used.
 *
 * key  : a 16bytes aligned pointer to the key to shift.
 *
 * shift: a value between 0 and 3 indicating the count of base pair
 *        to shift. 0 leads to no action. Value greater than 3 are
 *        reduced to this interval
 *
 * keyLength: a pointer to the length of the compressed key expressed
 *            in bytes.
 *
 * returns a pointer to the shifted key.
 *
 * WARNING even if dest is not NULL, the returned pointer can be
 * different than dest. So alwaus use the returned pointer. The
 * returned pointer is always 16bytes aligned
 */
pnuc shiftKey(pnuc dest, pnuc key,uint32_t shift, uint32_t keyLength)
{
	static char buffer[512] __attribute__ ((aligned (16))); // Force the alignment of the buffer
	uint32_t  n16bytes;
	uint32_t  remains;
	uint32_t  i;

	register um128 out;
	register um128 tmp;

	uint8_t mask;
	uint8_t cmask;
	uint8_t rmask;
	uint8_t save;
	uint8_t saveLast;
	uint8_t lshift;
	uint8_t rshift;


	pnuc rep;


	if (dest == NULL)
		dest = (pnuc) buffer;

	ASSERT(((size_t)dest & 0xF)==0,"Pointer %p is not 16bytes aligned",dest)

	rep = dest;

	// Limit shift in the [0;3] interval
	shift = shift & 0x3;

	// Shift == 0 is no shift so no computation
	if (shift==0) return key;

	// a shift of x bases is a shift of 2x bits
	rshift = shift << 1;


	lshift = 8 - rshift;

	//
	// Example :
	//
	// Shift = 3
	// rshift= 3 * 2 = 6
	// lshift= 8 - 6 = 2
	//
	// mask = (1 << 6) - 1 = 0b01000000 - 1 = 0b00111111
	// cmask= 0b11000000
	// rmask= 0b11111111 >> 6 = 0b00000011

	mask = (1 << rshift) - 1;
	cmask= ~mask;
	rmask= (~0) >> rshift;

	// The shifted key occupied one extra byte
	keyLength++;

	// Computes the count of complete 16 bytes packs in the key
	n16bytes = keyLength >>4;

	// The count of bytes after the last 16 bytes packs
	remains  = keyLength & 0xF;


	save = 0;


	for (i=0; i < n16bytes; i++, key+=16,dest+=16)
	{
		out.i = _MM_LOAD_SI128((const __m128i*)key);
		saveLast = out.u8[15];
		tmp.i = _MM_SRLI_EPI64(_MM_AND_SI128(out.i,
				 _MM_SET1_EPI8(cmask)),rshift);
		out.i = _MM_SLLI_EPI64(_MM_AND_SI128(out.i,_MM_SET1_EPI8(mask)),
														   lshift);
		out.i = _MM_SLLI_SI128(out.i,1);
		out.i = _MM_OR_SI128(out.i,tmp.i);

		if (i>0)
			out.u8[0]|= save << lshift; // BUG ??? change rshift to lshift
//		else                            // Not useful
//			out.u8[0]&= rmask;

		save = saveLast;

		_MM_STORE_SI128((__m128i*)dest,out.i);
	}

	for (i=0; i < remains; i++, key++,dest++)
	{
		saveLast = *key;
		*dest = (saveLast >> rshift) | (save << lshift);
		save = saveLast;
	}

	return rep;
}

/**
 * Compare the prefix of a key encoded by the encode function over
 * the length 'length' expressed in base pair with a prefix of same
 * length corresponding to the read r1 from buffer.
 *
 * buffer : a pointer to a read buffer
 * r1     : the identifer of the read to compare
 * key    : a pointer to the encoded second sequence involved in the comparison
 * length : the length of the prefix to compare
 *
 * return 0 if both the prefix are equal, -1 if the r1 sequence is lexicographically
 * before key and +1 otherwise.
 *
 */
int8_t cmpPrefix(buffer_t *buffer,uint32_t r1,pnuc key,uint32_t length)
{
	uint32_t shift;
	uint32_t i;

	uint8_t  bmask[]={255,192,240,252};
	uint8_t  mask;
	uint8_t  *pr1;
	uint8_t  *pr2;
	uint8_t  vr1=0;
	uint8_t  vr2=0;

	shift = CODELENGTH(length);
	mask  = bmask[length % 4];

	// DEBUG("pos : %d mask : %d,%x",pos,shift,mask);

	pr1 = ((uint8_t*)(buffer->records)) + buffer->recordSize * r1;
	pr2 = (uint8_t*)key;
	i=0;

	do {
		vr1 = *pr1;
		vr2 = *pr2;

		if (i==(shift-1))
		{
			vr1&=mask;
			vr2&=mask;
		}

		i++; pr1++; pr2++;

	} while( i < shift && vr2==vr1);

	return (vr1==vr2) ? 0 : ((vr1 < vr2) ? -1:1);

}


/**
 * Compare the prefix of a key encoded by the encode function over
 * the length 'length' expressed in base pair with a prefix of same
 * length corresponding to the read r1 from buffer.
 *
 * buffer : a pointer to a read buffer
 * r1     : the identifer of the read to compare
 * key    : a pointer to the encoded second sequence involved in the comparison
 * length : the length of the prefix to compare
 *
 * return 0 if both the prefix are equal, -1 if the r1 sequence is lexicographically
 * before key and +1 otherwise.
 *
 * INTERNAL FUNCTION DO NOT USE DIRECTLY
 *
 */


int8_t cmpCompPrefix(buffer_t *buffer,uint32_t r1,pnuc key, uint32_t length)
{
	int32_t i;
	uint32_t querylength;
	uint32_t readlength;
	uint8_t  mask;
	uint8_t  *pr1;
	uint8_t  *pr2;
	uint8_t  vr1=0;
	uint8_t  vr2=0;

	// Compute the length of compacted sequences
	querylength = CODELENGTH(length);
	readlength  = CODELENGTH(buffer->readSize);

	// Mask used to clean the left side of the query and subject
	mask= ((uint8_t)(~0)) >> (((4-(length & 3)) & 3) << 1);

	// DEBUG("pos : %d mask : %d,%x",pos,shift,mask);

	pr1 = ((uint8_t*)(buffer->records)) + buffer->recordSize * r1 + readlength - 1;
	pr2 = ((uint8_t*)(key)) + querylength - 1;

	i=querylength-1;

	do {
		vr1 = *pr1;
		vr2 = *pr2;

		if (i==0)
		{
			vr1&=mask;
			vr2&=mask;
		}

		i--; pr1--; pr2--;

	} while( i >=0 && vr2==vr1);

	vr1 = complement4nuc[vr1];
	vr2 = complement4nuc[vr2];

	return (vr1==vr2) ? 0 : ((vr1 < vr2) ? -1:1);

}


int32_t lookForForward(buffer_t *buffer, pnuc key, size_t length, int32_t* count)
{
	int32_t initcode;
	int32_t start;
	int32_t end;
	int32_t l_start;
	int32_t l_end;
	int32_t middle;
	int32_t comp;
//	int32_t comp1;

	// I set read count to 0
	*count=0;

	// and extract the 8 first nucleotides
	initcode = *((uint16_t*)key);

#ifdef LITTLE_END
	initcode = ((initcode & 255) << 8) | (initcode >> 8);
#endif

	// I use the hash table for identifying positions of reads
	// starting with these 8 nucleotides

	start=buffer->index1[initcode];

	if (initcode < 0xFFFF)
		end = buffer->index1[initcode+1];
	else
		end = buffer->readCount;


	// in this case no reads begin with the 8mer
	if (start==end)
	{
		*count=0;
		return 0;
	}

	// I start a bsearch between start and end

//	middle = (start + end) / 2;
//	comp = cmpPrefix(buffer,middle,key,length);

	end--;
	l_end=end;

	while (start!=end)
	{
		middle = (start + end) / 2;
		comp = cmpPrefix(buffer,middle,key,length);

		if (comp < 0) start=middle+1;
		if (comp >= 0)
		{
			end=middle;
			if (comp > 0)
				l_end=end;
		}

	}

	comp = cmpPrefix(buffer,start,key,length);

	// No match found

	if (comp!=0)
	{
		*count=0;
		return 0;
	}

	l_start=start;

	while (l_start!=l_end)
	{
		middle = (l_start + l_end) / 2 + 1;
		comp = cmpPrefix(buffer,middle,key,length);

		if (comp <= 0) l_start=middle;
		if (comp > 0)  l_end=middle-1;
	}

	*count = l_end-start+1;

	return start;

}

int32_t nextForward(buffer_t *buffer, int32_t current, size_t length, int32_t* endoflist)
{

	int32_t pos= current+1;
	pnuc    key= (pnuc)((uint8_t*)(buffer->records) + buffer->recordSize * current);
	int     comp=cmpPrefix(buffer,pos,key,length);

	if (comp==0)
		return pos;

	*endoflist=1;
	return 0;
}


//static char* bin8(int val){
//
//	static char buf[9] = {0};
//
//	int i = 30;
//
//	for(i=7; i>=0 ; --i, val >>= 1)
//		buf[i] = "01"[val & 1];
//
//	return buf;
//
//}


/**
 *
 * buffer    : a pointer to a read index structure
 * pnuc      : a pointer
 * key       : a pointer to the encoded query
 * length    : the length of the query
 * endoflist : set to 0 by the function if it finds a solution to 1 otherwise
 *
 */
int32_t lookForReverse(buffer_t *buffer, pnuc key, size_t length, int32_t* count)
{
	static uint8_t  bmask[]={255,192,240,252};
	char internalbuffer[512]  __attribute__ ((aligned (16))); // Force the alignment of the buffer;
	char internalbuffer2[512] __attribute__ ((aligned (16))); // Force the alignment of the buffer;
	pnuc 	 dest;
	pnuc 	 dest2;
	int32_t  rshift;
	uint32_t i;
	int32_t  initcode;
	int32_t  start;
	int32_t  end;
	int32_t  l_start;
	int32_t  l_end;
	int32_t  middle;
	int32_t  comp;
	uint32_t lkey;

	// I set the end of list flag to 0
	*count=0;

	dest =  (pnuc) internalbuffer;
	dest2 = (pnuc) internalbuffer2;
	//shift= 4 - (length & 3);

	lkey=CODELENGTH(length);               //-> we compute the compressed query length

	// then we reverse complement the sequence

	for (i=0; i<lkey;i++)
		dest2[i]=complement4nuc[(uint8_t)key[lkey-1-i]];

	// We have now to "bit align" the end of the key with the end of the reads

	rshift= buffer->readSize & 3;

	if (rshift > 0)
	{
//		printf("Rshift = %d\n",rshift);
//		int  ib;
//		for (ib=0;ib<lkey;ib++)
//		    printf ("%8s ",bin8(dest2[ib]));
//		printf("\n");

		dest = shiftKey(dest, dest2, rshift, lkey);
		dest[lkey]&=bmask[rshift];

//		for (ib=0;ib<=lkey;ib++)
//		    printf ("%8s ",bin8(dest[ib]));
//		printf("\n");

		// Set the last bits of the query to 0

		// we have to increase match length to take into account the
		// unfully filled last byte of the reads and key

		length+= 4 - rshift;

		// And adjust consequently the address and length of the key
		dest+= lkey + 1;
		lkey = CODELENGTH(length);
		dest-= lkey;
	}
	else
		dest = dest2;

	// Now dest point to the key to use

	initcode = *(((uint16_t*)(dest + lkey))-1);
#ifdef LITTLE_END
	initcode = complement4nuc[initcode & 0x00FF] | (complement4nuc[(initcode >> 8) & 0x00FF] << 8);
#else
	initcode = (complement4nuc[initcode & 0x00FF] << 8) | complement4nuc[(initcode >> 8) & 0x00FF ];
#endif

	// I use the hash table for identifying positions of reads
	// starting with these 8 nucleotides

	start=buffer->index2[initcode];


	if (initcode < 0xFFFF)
		end = buffer->index2[initcode+1];
	else
		end = buffer->readCount;

	// in this case no reads begin with the 8mer
	if (start==end)
	{
		*count=0;
		return 0;
	}

	// I start a bsearch between start and end

	end--;
	l_end=end;

	while (start!=end)
	{
		middle = (start + end) / 2;
		comp = cmpCompPrefix(buffer,buffer->order1[middle],dest,length);

		if (comp < 0)  start=middle+1;
		if (comp >= 0)
		{
			end=middle;
			if (comp > 0)
				l_end=end;
		}

	}

	comp = cmpCompPrefix(buffer,buffer->order1[start],dest,length);

	// No match found

	if (comp!=0)
	{
		*count=0;
		return 0;
	}

	l_start=start;

	while (l_start!=l_end)
	{
		middle = (l_start + l_end) / 2 + 1;
		comp = cmpCompPrefix(buffer,buffer->order1[middle],dest,length);

		if (comp <= 0) l_start=middle;
		if (comp > 0)  l_end=middle-1;
	}

	*count = l_end-start+1;
//	printf("%d-%d ->%d\n",start,l_end,*count);

	return start;

}

int32_t nextReverse(buffer_t *buffer, int32_t current, size_t length, int32_t* endoflist)
{

	int32_t pos= current+1;
	int32_t rshift= buffer->readSize & 3;
	size_t  lkey = length + ((rshift==0) ? 0:(4-rshift));
	pnuc    key= (pnuc)((uint8_t*)(buffer->records) + buffer->recordSize * buffer->order1[current] + CODELENGTH(buffer->readSize) - CODELENGTH(lkey));
	int     comp=cmpCompPrefix(buffer,buffer->order1[pos],key, lkey);

	if (comp==0)
	{
		*endoflist=0;
		return pos;
	}

	*endoflist=1;
	return 0;

}

int32_t lookForReads(buffer_t *buffer, pnuc key, size_t length, int32_t* endoflist)
{
	int32_t count;
	int32_t pos = lookForForward(buffer, key, length, &count);


	if (count>0)
	{
		pos++;
		*endoflist=0;
	}
	else
	{
		pos = lookForReverse(buffer, key, length, &count);
		if (count>0)
		{
			pos = - buffer->order1[pos] - 1;
			*endoflist=0;
		}
		else
			*endoflist=1;
	}

	return pos;
}

int32_t fastLookForReads(buffer_t *buffer,
		                 pnuc key,
		                 size_t length,
		                 int32_t* fcount,
		                 int32_t* rcount,
		                 int32_t* fpos,
		                 int32_t* rpos
		                 )
{
	*fpos = lookForForward(buffer, key, length, fcount);
	*rpos = lookForReverse(buffer, key, length, rcount);

	return *fcount + *rcount;
}


int32_t nextRead(buffer_t *buffer, int32_t current, size_t length, int32_t* endoflist)
{
	int32_t next=0;
	int32_t count;
	pnuc from;

	if (current == 0)
		*endoflist=1;

	if (current > 0)
	{
		current--;
		next = nextForward(buffer, current, length, endoflist);

		if (*endoflist==0)
			next++;
		else
		{
			from = (pnuc)((uint8_t*)(buffer->records) + buffer->recordSize * current);
			next = lookForReverse(buffer, from, length, &count);

			if (count>0)
			{
				next = - buffer->order1[next] -1;
				*endoflist=0;
			}
			else
				*endoflist=1;
		}

	}

	if (current < 0)
	{
		current = buffer->complement[-current -1];
		next = nextReverse(buffer, current, length, endoflist);

		if (*endoflist==0)
			next = - buffer->order1[next] -1;
	}

	return next;
}

int32_t lookForString(buffer_t *buffer, char *key, size_t length, int32_t* endoflist)
{
	char internalbuffer[512];
	pnuc dest;

	ASSERT(length>=8,"length have to be greater or equal to %d",8)


	// I encode the key string
	dest = (pnuc) PTR16(internalbuffer);
	dest = encodeSequence(dest, key, length);

	return lookForReads(buffer, dest, length, endoflist);
}

int32_t fastLookForString(buffer_t *buffer,
						  char *key,
		                  size_t length,
		                  int32_t* fcount,
		                  int32_t* rcount,
		                  int32_t* fpos,
		                  int32_t* rpos
		                 )
{
	char internalbuffer[512];
	pnuc dest;

	ASSERT(length>=8,"length have to be greater or equal to %d",8)


	// I encode the key string
	dest = (pnuc) PTR16(internalbuffer);
	dest = encodeSequence(dest, key, length);

	return fastLookForReads(buffer,dest,length,fcount,rcount,fpos,rpos);
}


int32_t lookForReadsIds(buffer_t *buffer, int32_t key, int32_t* endoflist)
{
	pnuc dest;

	if (key < 0)
		key=-key;

	dest = (pnuc)((uint8_t*)(buffer->records) + buffer->recordSize * (key-1));

	return lookForReads(buffer, dest, buffer->readSize, endoflist);
}

int32_t nextReadIds(buffer_t *buffer, int32_t current, int32_t* endoflist)
{
	return nextRead(buffer,current, buffer->readSize, endoflist);
}
