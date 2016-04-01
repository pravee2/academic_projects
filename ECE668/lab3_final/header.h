#include <stdio.h>
#include <stdlib.h>


#define READSIZE 25						        //restrict this to 100-255
#define MAXCOUNT 65536
#define MINCOUNT 1

unsigned char* concat(unsigned char *A, unsigned char B)
{
	unsigned char* output;
	size_t i,j;
	int N;
	
	for(i=0;A[i]!='\0';i++);
	
	N=i;
	
//	printf("Array 1 size: %d\n", N);
	output = (unsigned char*)malloc((N+1)*sizeof(unsigned char));
	
	
	for(i=0;i<N;i++)
		output[i] = A[i];
	
	output[i] = B;
	
	for(j=0; output[j]!='\0';j++);
	N=j;

//	printf("Post concatenation: %d\n",N);	
	return output;
}
