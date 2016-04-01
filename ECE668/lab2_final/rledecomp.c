/*
Name: Varun Praveen
CUID: C15618128
Email: pravee2@clemson.edu
Course: ECE-6680
Description:This code implements a marker based RLE decompression
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define READSIZE 50						        //restrict this to 100-255
#define MAXCOUNT 255
#define MINCOUNT 1

int main(int argc, char *argv[])
{



FILE 			*fpt_in,*fpt_out;
int 			i,j;
int 			count, iter;
int 			fileSize;
unsigned char 		runcount;					//count value to be output to the file
unsigned char		byte_A, byte_B;					//the two bytes read from the file
unsigned char		byte,data, data_pair[2];			//data buffers to hold one byte of data	
int 			flag_rle;					//rle decompression on/off flag

if(argc!=3)
{
	printf("Invalid Usage!\nUsage: rledecomp [input filename] [output filename]\n");
	exit(0);
}


/**********************************DECOMPRESSION ALGORITHM**************************************/
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
//printf("Read size is : %d\n",READSIZE);
fileSize = fileSize - 1;					//accomodating end of file return character
fpt_out = fopen(argv[2],"wb");

/*
for(i=0;i<READSIZE;i++)
	printf("calloc intiliazed buffer[%d] = [%d]",i,buffer[i]);
*/

// reading data in to a buffer

j=0;
iter = 1;
do
{
	//printf("*****************ITERATION NO. %d ************************\n", iter);
	j+= fread(data_pair, 1, 2, fpt_in);			//reading byte pairs for decompression
	//printf("J at the beginning of the do-while: %d\n", j);
	if(data_pair[0] == 0 && data_pair[1] == 255)		//checking flag size
	{
		do
		{
			j+=fread(&byte_A,1,1,fpt_in);				
			flag_rle = 1;
			if(byte_A != 0)
				fwrite(&byte_A,1,1,fpt_out);	//fout non rle data
			else
			{
				fread(&byte_B,1,1,fpt_in);
				if(byte_B == 255)		//check for end of rle coding
				{
					flag_rle = 0;
					j=j+1;
				}
				else
				{
					fseek(fpt_in,-1,SEEK_CUR);
				}	
			}
			
		}while(flag_rle==1);		
	}
	else							//else output rle data pair
	{
		count = data_pair[0];
		data = data_pair[1];
		for(i=0;i<count;i++)				//flusing output uncompressed data to the output file
			fwrite(&data,1,1,fpt_out);		

	}
//	printf("The value of j : %d\n", j);
	fileSize -= j;
	j=0;
//	printf("File size left: %d\n", fileSize);
	iter++;

	
}while(fileSize>0);						//termination condition at EOF



fclose(fpt_in);
fclose(fpt_out);
	
return 0;	
	
	
}
