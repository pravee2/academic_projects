/*
Name: Varun Praveen
CUID: C15618128
Email: pravee2@clemson.edu
Course: ECE-6680
Description:This code implements LZW decompression
*/



#include"header.h"


int main(int argc, char *argv[])
{



FILE 			*fpt_in,*fpt_out;
int 			i,j;
int 			count, iter;
int 			fileSize;							//Size of file to be compressed		
int 			dictSize;							//Size of dictionary
unsigned char 		byte;								//buffer byte
unsigned short		code[MAXCOUNT];							//dictionary table containing code values
unsigned short 		currcode, prevcode;						//current iteration code and previous iteration code
unsigned char		**dictionary;							//dictionary entries
unsigned char 		p,c;								
unsigned char		*xstring,ystring,*xPlusYstring;					//x and y buffer characters
int 			dlength[MAXCOUNT];						//dictionary table containing length of each dictionary entry
int 			xlength,xPlusYlength;						//length of buffer strings
int 			k,l,m;								//iterators	
int			elemindict;

// invalid usage check
if(argc!=3)
{
	printf("Invalid Usage!\nUsage: lzwcomp [input filename] [output filename]\n");
	exit(0);
}

fpt_in = fopen(argv[1], "rb");		

//invalid filename check
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

//fileSize--;
//fileSize--;

fseek(fpt_in,0, SEEK_SET );
printf("Filesize : %d\n", fileSize);

fpt_out = fopen(argv[2],"wb");

/****************************** INTIALIZING DICTIONARY WITH ROOTS **********************************/

dictionary = (unsigned char**)malloc(65536*sizeof(unsigned char*));

for(i=0;i<256;i++)
{
	dictionary[i] = (unsigned char*)calloc(1,sizeof(unsigned char));
	dictionary[i][0] = i;
//	printf("dictionary[%d] = %s\n", i, dictionary[i]);
	dlength[i] = 1;
	code[i] = i;
}

iter = 1;

dictSize = 256;

j = fread(&currcode,sizeof(unsigned short),1,fpt_in);
fwrite(dictionary[currcode],sizeof(unsigned char),dlength[currcode],fpt_out);

//pstring = (unsigned char*)calloc(1,1);
//*pstring = '\0';

fileSize-=j*(sizeof(unsigned short));

//printf("Filesize after first write: %d\n",fileSize);

/*while(fileSize>0)*/
//decompression procedure
do{
	prevcode = currcode;
	j = fread(&currcode,sizeof(unsigned short),1,fpt_in);
	fileSize-=j*2;
//	printf("Filesize after first write: %d\n",fileSize);
//	printf("currcode : %d\n", currcode);
	//check if current code lies in dictionary
	if(currcode <dictSize)
	{
		fwrite(dictionary[currcode],sizeof(unsigned char),dlength[currcode],fpt_out);
		xstring = (unsigned char*)calloc(dlength[prevcode],sizeof(unsigned char));
		for(k=0;k<dlength[prevcode];k++)
			xstring[k] = dictionary[prevcode][k];
		ystring = dictionary[currcode][0];
		xPlusYstring = concat(xstring,ystring);
		for(k=0;xPlusYstring[k]!='\0';k++);
		xPlusYlength = k;
		k=0;
		//making new dictionary entry		
		if(dictSize<65536)
		{
			dictionary[dictSize] = (unsigned char*)malloc(xPlusYlength*sizeof(unsigned char));
			for(l=0;l<xPlusYlength;l++)
				dictionary[dictSize][l] = xPlusYstring[l];
			l=0;
			dlength[dictSize] = xPlusYlength;
			code[dictSize] = dictSize;
			dictSize++;	
		}
		free(xstring);
		free(xPlusYstring);		
	}
	//check if current code lies outside dictionary
	if(currcode>=dictSize)
	{

		xstring = (unsigned char*)calloc(dlength[prevcode],sizeof(unsigned char));
		for(k=0;k<dlength[prevcode];k++)
			xstring[k] = dictionary[prevcode][k];
		ystring = dictionary[prevcode][0];
		xPlusYstring = concat(xstring,ystring);
		for(k=0;xPlusYstring[k]!='\0';k++);
		xPlusYlength = k;
		k=0;
		fwrite(xPlusYstring,sizeof(unsigned char),xPlusYlength,fpt_out);	
		//dictionary entry
		if(dictSize<65536)
		{
			dictionary[dictSize] = (unsigned char*)malloc(xPlusYlength*sizeof(unsigned char));
			for(l=0;l<xPlusYlength;l++)
				dictionary[dictSize][l] = xPlusYstring[l];
			l=0;
			dlength[dictSize] = xPlusYlength;
			code[dictSize] = dictSize+1;
			dictSize++;	
		}
		free(xstring);
		free(xPlusYstring);
	}
}while(fileSize>0);
//do
//{




//}while(/*!feof(fpt_in)*/fileSize>0);




//printf("Dictionary Size:%d\n",dictSize);
/*for(i=dictSize-(dictSize-256)-1;i<dictSize;i++)
{
	printf("dictionary [%d] : ", i);
	for(k=0;k<dlength[i];k++)
		printf("%c\t",dictionary[i][k]);
	printf("dlength: %dend\n", dlength[i]);
}
*/

fclose(fpt_in);
fclose(fpt_out);
free(dictionary);
//free(pstring);
//free(pPlusCstring);
return 0;	

}
