#include<stdio.h>
#include<stdlib.h>

int main(int argc, char *argv[])
{
	FILE 			*fpt,*fpt_out;
	unsigned char		byte;
	int 			count;
	int 			i;
	
	if(argc!=2)
	{
		printf("Invalid usage: bytedump [filename]\n");
		exit(0);	
	}
	

	fpt = fopen(argv[1], "rb");
	fpt_out = fopen("bytedump.txt","wb");
	if(fpt==NULL)
	{
		printf("File %s not found \n Exiting execution\n", argv[1]);
		exit(0);
	}
	
	count = 0;
	i=fread(&byte,1,1,fpt);
	do	
	{
		count++;
		fprintf(fpt_out,"Byte value[%d] read is %d : %c \n", count, byte, byte);
		i = fread(&byte, 1,1, fpt);

	}while(i!=0);	
	fclose(fpt_out);
	fclose(fpt);
	return 0;
}	
