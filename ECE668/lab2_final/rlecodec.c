/*
Name: Varun Praveen
CUID: C15618128
Email: pravee2@clemson.edu
Course: ECE-6680
Description:This code implements a marker based RLE compression
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define READSIZE 25						        //restrict this to 100-255
#define MAXCOUNT 255
#define MINCOUNT 1

int main(int argc, char *argv[])
{



FILE 			*fpt_in,*fpt_out;
int 			i,j;
int 			count, iter;
int 			fileSize;			
unsigned char 		runcount;						//count value to be output to the file
unsigned char		byte_A, byte_B;						//the two bytes read from the file
unsigned char		byte;							//temporary buffer byte
unsigned char 		*buffer;						//data buffer into the compression algorithm
unsigned char 		unequal_count, output_pair[2];				//RLE data pair output
unsigned char 		flag[2] = {0,255};					//flag out to mark start and end of RLE compression
unsigned char 		BUFFERSIZE = 0;						//data buffer size

if(argc!=3)
{
	printf("Invalid Usage!\nUsage: rlecodec [input filename] [output filename]\n");
	exit(0);
}



fpt_in = fopen(argv[1], "rb");		

if(fpt_in == NULL)
{
	printf("Invalid file name for input file: %s \n", argv[1]);
	exit(0);
}


fileSize = 0;
// computing file size
while(j = fread(&byte,1, 1,fpt_in)!=0)
{ 
	fileSize++;
}

fseek(fpt_in,0, SEEK_SET );

//printf("File size is : %d\n",fileSize);
//READSIZE = fileSize;
//printf("File size is : %d\n",READSIZE);
//fileSize = fileSize - 1;

fpt_out = fopen(argv[2],"wb");

/*
for(i=0;i<READSIZE;i++)
	printf("calloc intiliazed buffer[%d] = [%d]",i,buffer[i]);
*/

// reading data in to a buffer
iter = 1;
/**************************************COMPRESSION ALGORITHM*****************************************************/
do
{
	if(fileSize > READSIZE)							//defining buffer size to max(READSIZE,remaining filesize)
		BUFFERSIZE = READSIZE;
	else
		BUFFERSIZE = fileSize;	
	buffer = (unsigned char*)calloc(BUFFERSIZE, sizeof(unsigned char));	//data buffer to check ahead for RLE requirement
	j = fread(buffer, sizeof(unsigned char), BUFFERSIZE, fpt_in);		//buffer input
	runcount = 1;
	unequal_count = 0;
//	printf("\n**********************************ITERATION %d**************************************\n", iter);
//	printf("The return value of fread is : %d\n", j);

	
	for(i=0;i<BUFFERSIZE-1;i++)
	{
//		printf("Buffer Value [%d]: %d\t%c\n", i,buffer[i], buffer[i]);
		if(buffer[i] != buffer[i+1])					//buffer count to changing 
		{
			unequal_count++;				
		}
	}	

//	printf("Unequal count: %d\n", unequal_count);

	if(unequal_count > BUFFERSIZE/2)					//writing non RLE buffer to output file
	{
		fwrite(flag,1,2,fpt_out);					//start of RLE flag
		fwrite(buffer,1, BUFFERSIZE, fpt_out);				//data output flush
		fwrite(flag,1,2,fpt_out);					//end of RLE flag
	}	
	else									//RLE section
	{
		for(i=1;i<BUFFERSIZE;i++)					//RLE algorithm to count runs 
		{
			byte_A = buffer[i-1];
			byte_B = buffer[i];		
			if(i == BUFFERSIZE-1)					//accounting for data at the end of the buffer
			{
				if(byte_A == byte_B)
				{
					runcount++;
					output_pair[0] = runcount;
					output_pair[1] = byte_A;
					fwrite(output_pair, 1, 2, fpt_out);
//					printf("output pair [%d %c] \n", output_pair[0], output_pair[1]);
				}
				else
				{
					output_pair[0] = runcount;
					output_pair[1] = byte_A;
					fwrite(output_pair, 1, 2, fpt_out);
					output_pair[0] = 1;
					output_pair[1] = byte_B;
					fwrite(output_pair, 1, 2, fpt_out);	
				}			
			}
			else if(byte_A==byte_B)
			{
				if(runcount<BUFFERSIZE)	
					runcount++;
				else	
				{
					output_pair[0] = runcount;
					output_pair[1] = byte_A;	
					fwrite(output_pair, 1, 2, fpt_out);
//					printf("output pair [ %d %c ] \n",output_pair[0], output_pair[1]);
					runcount = 1;
				}
			}
			else
			{
				output_pair[0] = runcount;
				output_pair[1] = byte_A;
				fwrite(output_pair, 1, 2, fpt_out);
				runcount = 1;	
//				printf("output pair [ %d %c ] \n",output_pair[0], output_pair[1]);
			}		
		}	
	}	
//j = fread(buffer, sizeof(unsigned char), READSIZE, fpt_in);
//	printf("The value of j : %d\n", j);
	fileSize -= j;
//	printf("File size left: %d\n", fileSize);
	free(buffer);
	iter++;
}while(fileSize>0);



fclose(fpt_in);
fclose(fpt_out);
	
return 0;	
	
	
}
