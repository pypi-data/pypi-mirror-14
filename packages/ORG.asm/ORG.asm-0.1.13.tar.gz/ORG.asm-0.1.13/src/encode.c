/*
 * encode.c
 *
 *  Created on: 11 juil. 2012
 *      Author: coissac
 */

#include <inttypes.h>
#include <stdlib.h>
#include "orgasm.h"
#include "_sse.h"

//#include "debug.h"

/**
 * Round an unsigned 32 bits int x to the minimum
 * multiple of 16 greater or equal to x
 */

uint32_t round16(uint32_t x)
{
	// This just check the special case where
	// x is an exact multiple of 16

	if ((x & 0xF) == 0)
		return x;

	return (x & 0xFFFFFFF0) + 0x10;

}

/**
 * Round an unsigned 32 bits int x to the minimum
 * multiple of 8 greater or equal to x
 */

uint32_t round8(uint32_t x)
{
	// This just check the special case where
	// x is an exact multiple of 16

	if ((x & 0x7) == 0)
		return x;

	return (x & 0xFFFFFFF8) + 0x8;

}


/**
 * Round an unsigned 32 bits int x to the minimum
 * multiple of 4 greater or equal to x
 */

uint32_t round4(uint32_t x)
{
	// This just check the special case where
	// x is an exact multiple of 4

	if ((x & 0x3) == 0)
		return x;

	return (x & 0xFFFFFFFC) + 0x4;

}

/**
 * Round an unsigned 32 bits int x to the minimum
 * power of 2 greater or equal to x
 *
 */

uint32_t round2(uint32_t x)
{
	uint32_t p;

	// This just check the special case where
	// x is an exact power of 2

	if (!(x & (x-1)))
		return x;

/*
#ifdef __intel__

	// on Intel platform, the bsr instruction return the index
	// of the first bit set to 1 on the right side of the word

	asm("bsr   %%eax, %%ebx;" : "=b" (p) : "a" (x));
	p++;
#else
*/
	p=0;
	while(x) x>>=1,p++;
/*#endif*/

	return (1 << p);
}

/*
 *  Encode a four nucleotides string in a byte
 *  based on a 2 bits code per nucleotide
 *  Just A, C, G and T nucleotides can be encoded
 *  UIPAC code return undetermined code.
 *  the encoding is not sensible to the case.
 *
	065      101    41   01000001        A
    067      103    43   01000011        C
    071      107    47   01000111        G
    084      124    54   01010100        T
    097      141    61   01100001        a
    099      143    63   01100011        c
    103      147    67   01100111        g
    116      164    74   01110100        t
                              **
    The two bits in the binary ASCII code
    pointed out by the two stars can be
    selected to encode the nucleotide quickly
    on to bytes codes independently of upper
    or lower case:

    	a : 00 -> 0
    	c : 01 -> 1
    	t : 10 -> 2
    	g : 11 -> 3

*/


uint8_t encode4nuc(const char* seq)
{
	uint32_t  out;

	out=*((uint32_t*)seq);

#ifdef LITTLE_END
	out = out >> 24 | \
		  out << 24 | \
		  ((out >> 8) & 0x0000FF00) | \
		  ((out << 8) & 0x00FF0000);
#endif

	out>>=1;
	out&=0x03030303;
	out= (out | (out >>  6)) & 0x0F0F0F0F;
	out= (out | (out >> 12)) & 0x000000FF;

	return (uint8_t)out;
}

/**
 * MACRO define for computing binary equivalence operator
 *
 *      eq  | 0 | 1 |
 *     -----+---+---|
 *       0  | 1 | 0 |
 *     -----+---+---|
 *       1  | 0 | 1 |
 *     -----+---+---|
 */

#define EQ(x,y) ((x) & (y)) | ((~(x)) & (~(y)))

/**
 * MACRO based on EQ macro testing equivalence of the
 * for bytes constituting a 32bits word with four time
 * the same 8bits word.
 */

#define EQNUC(x,n) EQ(out,((n) | ((n) << 8) | ((n) << 16) | ((n) << 24)))

/**
 * Check if the four next nucleotides pointed by
 * the seq pointer are all A, C, G or T.
 *
 * The function return a value equal to zero if
 * at least one of the four is not an A, G, G or T
 */
uint8_t is4ACGT(const char* seq)
{
	// FIXME: there is a logical bug in this function
	//        if the nucleotides are equal the eq operator
	//        return 0xFF but not 0 if they are different

	uint32_t out;

	out=*((uint32_t*)seq);
	out&=~(0xDFDFDFDF);
	out = EQNUC(out,'A') | \
		  EQNUC(out,'C') | \
		  EQNUC(out,'G') | \
		  EQNUC(out,'T');

	return out==0xFFFFFFFF;

}

uint8_t is16ACGT(const char* seq)
{
	um128 out;

	// Load the 16 nucleotides
	out.i = _MM_LOAD_SI128((const __m128i*)seq);

	//Switch tu Uppercase

	out.i = _MM_AND_SI128(out.i,_MM_SET1_EPI8(0xDF));

	// Compare with A, C, G, T and 0

	out.i = _MM_OR_SI128(
			 _MM_OR_SI128(
		       _MM_OR_SI128(
			    _MM_OR_SI128(_MM_CMPEQ_EPI8(out.i,_MM_SET1_EPI8('A')),
				  		     _MM_CMPEQ_EPI8(out.i,_MM_SET1_EPI8('C'))),
				  		     _MM_CMPEQ_EPI8(out.i,_MM_SET1_EPI8('G'))),
				  		     _MM_CMPEQ_EPI8(out.i,_MM_SET1_EPI8('T'))),
				  		     _MM_CMPEQ_EPI8(out.i,_MM_SETZERO_SI128()));

	// Return true if the 16 nucleotides are in [A,C,G,T,0]

	return _MM_MOVEMASK_EPI8(out.i) == 0xFFFF;


}

/**
 * encode 16 nucleotide in parallel using SSE instructions.
 * the seq pointer has to be 16 bytes aligned.
 * The function use the same two bits code than the encode4nuc
 * function encoded above.
 *
 */
uint32_t encode16nuc(const char* seq)
{
	um128 out;
	uint32_t result;

	out.i = _MM_LOAD_SI128((const __m128i*)seq);

	DEBUG("%16s",out.c);
	DEBUG("%:vX",out.i);
	DEBUG("%:08vlX",out.i);

#ifdef LITTLE_END
	out.i = _MM_OR_SI128(                                                        \
			   _MM_OR_SI128(                                                     \
				  _MM_OR_SI128(_MM_SRLI_EPI32(out.i,24),                         \
			                   _MM_SLLI_EPI32(out.i,24)),                        \
			_MM_AND_SI128(_MM_SRLI_EPI32(out.i,8),_MM_SET1_EPI32(0x0000FF00))),  \
		    _MM_AND_SI128(_MM_SLLI_EPI32(out.i,8),_MM_SET1_EPI32(0x00FF0000)));
#endif

	DEBUG("%16s",out.c);
	DEBUG("%:vX",out.i);
	DEBUG("%:08vlX",out.i);

	/*
	 * Equivalent to :
	 *
	 * out>>=1;
	 * out&=0x03030303;
     */

	out.i = _MM_AND_SI128(_MM_SRLI_EPI32(out.i,1),_MM_SET1_EPI8(3));
	DEBUG("%:vX",out.i);
	DEBUG("%:08vlX",out.i);

	/*
	 * Equivalent to :
	 *
	 * out= (out | (out >>  6)) & 0x0F0F0F0F;
	 */

	out.i = _MM_AND_SI128(_MM_OR_SI128(_MM_SRLI_EPI32(out.i,6),out.i),_MM_SET1_EPI8(0xF));
	DEBUG("%:vX",out.i);
	DEBUG("%:08vlX",out.i);

	/*
	 * Equivalent to :
	 *
	 * out= (out | (out >> 12)) & 0x000000FF;
	 */

	out.i = _MM_AND_SI128(_MM_OR_SI128(_MM_SRLI_EPI32(out.i,12),out.i),_MM_SET1_EPI32(0xFF));
	DEBUG("%:vX",out.i);
	DEBUG("%:08vlX",out.i);

#ifdef LITTLE_END
	result  = ((uint32_t) out.u8[12] << 24) | \
		 	  ((uint32_t) out.u8[ 8] << 16) | \
		 	  ((uint32_t) out.u8[ 4] <<  8) | \
		 	  ((uint32_t) out.u8[ 0]);
#else
	result  = ((uint32_t) out.u8[ 0] << 24) | \
		 	  ((uint32_t) out.u8[ 4] << 16) | \
		 	  ((uint32_t) out.u8[ 8] <<  8) | \
		 	  ((uint32_t) out.u8[12]);
#endif

	return result;
}

/*
 * Encode a full sequence in binary format using the two bits code
 * define in the comment of the encode4nuc function
 *
 */
pnuc encodeSequence(pnuc dest, char* src, uint32_t length)
{
	static char buffer[512];
	char      read[512];
	char     *pread;
	uint32_t  recordLength;
	uint32_t* encodedseqs;
	char*     bufferend;
	char     *index;

	pread = (char*) PTR16(read);
	bzero(read,512);
	strncpy(pread,src,length);

	if (dest == NULL)
		dest = (pnuc) PTR16(buffer);

	ASSERT(((size_t)dest & 0xF)==0,"Pointer %p is not 16bytes aligned",src)

	encodedseqs = (uint32_t*)dest;
	recordLength = round16(length);
	bufferend = pread + recordLength;

	if (checkACGT(pread,recordLength))
	{
		for (index=pread; index < bufferend; index+=16, encodedseqs++)
			*encodedseqs=encode16nuc(index);
	}
	else
		return NULL;

	return dest;
}
