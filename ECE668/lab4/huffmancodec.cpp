/* 
Name : Varun Praveen
Course: ECE-6680
Assignment No: Lab 4
Contact: pravee2@clemson.edu
Description: This code implements a huffman compression algorithm with varible bit compression. The output file is of the following pattern:

HEADER
VARIABLE BIT PATTERN

HEADER: [DICTIONARY COUNT] [DICTIONARY SYMBOLS] [SYMBOL FREQUENCY]
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <vector>
#include <algorithm>
#include <math.h>

/**********************		Compare function for qsort   	****************************/
int compare_function(const void* a, const void* b)
{
	unsigned char *x = (unsigned char *)a;				
	unsigned char *y = (unsigned char *)b;
 	return *x - *y;

}
/* 	Compare function for sorting of frequencies 	*/
int compare_function_int(const void *a, const void* b)
{
	int *x = (int *)a;
	int *y = (int *)b;
	return *x - *y;

}
/* Tree nodes for huffman tree*/
struct node
{
	unsigned char val;
	int freq;
	struct node* left;
	struct node* right;
	unsigned char code;
};

typedef struct node Node;

/* 	sort function for tree nodes 	*/
bool sortCompare(struct node A, struct node B){	return A.freq>B.freq;}

/* invalid logic for element search in a tree */
Node* getleaf(Node *root, unsigned char sym)
{
	if(root!=NULL)
	{	
		if(root->val == sym)
			return root;
		else
		{
			getleaf(root->left,sym);
			getleaf(root->right,sym);
		}
	}
	else
		return NULL;
}
/* Traversing tree to search for a symbol in the tree with root node as root */
Node* getleaf_logic2(Node *root, unsigned char symbol)
{
	Node *temp;
	temp = (Node*)malloc(sizeof(Node));
	if(root==NULL)
		return NULL;
	else
	{	
		if(root->val == symbol)
			return root;
		else
		{
			temp = getleaf_logic2(root->left, symbol);
			if(temp==NULL)
				temp = getleaf_logic2(root->right, symbol);
			return temp;
		}
	}
}

/* Traversing binary tree to find the symbol and derive code for the symbol */
bool getCode(unsigned char symbol,int* size, int* &pattern, Node *root)
{
	bool code;
	if(root==NULL)
		return 0;
	else
	{
		if(root->val == symbol)
			return 1;
		else
		{
			(*size)++;
			pattern = (int*)realloc(pattern, (*size)*sizeof(int));
			pattern[*size-1] =0;
			code = getCode(symbol,size,pattern,root->left);
			if(!code)
			{	
				pattern[*size-1] = 1;
				code = getCode(symbol,size,pattern,root->right);			
			}
			if(!code)
				(*size)--;
			return code;

		}		
	}
				

}

/* Pre order printing of tree elements */
void elementPrint( Node *root ) 
{
	if(root!=NULL)
	{
		std::cout<< "Root Val: " << root->val << "\t" << "Root Frequency: " << root->freq << std::endl;
		elementPrint(root->left);
		elementPrint(root->right);
	}
} 

/* Counting number of nodes in the tree*/
int NodeCount(Node *root)
{
	if(root == NULL)
		return 0;
	else
	{
		int count=1;
		count += NodeCount(root->left);
		count += NodeCount(root->right);	
		return count;				

	}
}



int main( int argc, char *argv[])
{


FILE 				*fpt_in, *fpt_out, *fpt_inter;
int 				i,j,k;
unsigned char 			*data_in, *data_stream;
unsigned char			dictionary_count;
int 				symbolCount;
unsigned char			*dictionary;
int				*frequency, *frequency_sorted;
unsigned char 			byte;
int				fileSize;
int 				treeCount=0;

std::vector<Node>dict;
dict.clear();
/* Check for usage errors */
if(argc!=3)
{
	printf("Invalid Usage: huffmancodec [input_filename] [output_filename]\n");
	exit(0);
}

/* Check for file name errors */
if(fopen(argv[1],"rb")==NULL)
{
	printf("Invalid input filename: %s\n", argv[1]);
	exit(0);
}

fpt_in = fopen(argv[1],"rb");
/* computin filesize of the file to be compressed */
fileSize = 0;
while(fread(&byte,1,1,fpt_in)!=0)
	fileSize++;

printf("File size is: %d\n",fileSize);
fseek(fpt_in, 0, SEEK_SET);


/******************************************file to be compressed opened*****************************************/

/* reading all the data in the file to form binary tree */
data_in = (unsigned char*)malloc(sizeof(unsigned char)*fileSize);
j = fread(data_in, sizeof(unsigned char), fileSize, fpt_in);
fclose(fpt_in);


fpt_in = fopen(argv[1],"rb");
/* reading all the data again to stream while compression*/
data_stream = (unsigned char*)malloc(sizeof(unsigned char)*fileSize);
j = fread(data_stream, sizeof(unsigned char), fileSize, fpt_in);


fpt_out = fopen(argv[2],"wb");
/* Sorting data in ascending order to compute number of different symbols and frequencies */
qsort(data_in,fileSize,sizeof(unsigned char),compare_function);


/**************************		Dictionary initialization		********************************/

dictionary_count = 1;
/* scan 1 to compute dictionary count : no of distinct elements in the file */
for(i=0; i<fileSize-1; i++)
	if(data_in[i] != data_in[i+1])
	{
		dictionary_count++;
//		if(i==fileSize-2)
//			dictionary_count++;
	}


printf("Number of symbols in the dictionary: %d\n", dictionary_count);

dictionary = (unsigned char*)malloc(sizeof(unsigned char)*dictionary_count);
frequency = (int*)malloc(sizeof(int)*dictionary_count);
frequency_sorted = (int*)malloc(sizeof(int)*dictionary_count);
symbolCount = 1;
k=0;

/************* 		Assigning frequency count for each data element 	***********************/
for(i=0;i<fileSize-1;i++)
{
	if(data_in[i]==data_in[i+1])
	{
		symbolCount++;
		if(i == fileSize-2)
		{
			dictionary[k] = data_in[i+1];
			frequency[k] = symbolCount;
			k++;
		}
	}		
	else
	{
		if(i == fileSize-2)
		{
			dictionary[k] = data_in[i];
			frequency[k] = symbolCount;
			k++;
			symbolCount = 1;
			dictionary[k] = data_in[i+1];
			frequency[k] = 1;
			k++;
		}
		else
		{	
			dictionary[k] = data_in[i];
			frequency[k] = symbolCount;
			k++;
			symbolCount = 1;
		}
	}
}
free(data_in);																								//freeing sorted data post frequency and dictionary entry computation
Node temp;
	
/* Creating a vector of dictionary entries to be able to form a tree */
for(i=0;i<k;i++)
{
	temp.freq = frequency[i];																				//initialising leaf nodes with dictionary elements and frequencies
	temp.val = dictionary[i];
	temp.left = NULL;																						//setting left and right child to NULL for leaf nodes
	temp.right = NULL;
	dict.push_back(temp);	
}

std::cout << "Dictionary size: " << dict.size() << std::endl;

//sort(dict.begin(),dict.end(), sortCompare);

/*for(i=0; i< dict.size(); i++)
	std::cout<< "Dictionary Element: " << dict[i].val <<"\t"<< dict[i].freq << std::endl;
*/

Node *minimum, *lastmin;

//minimum = (Node*)malloc(1*sizeof(Node));
int iter = 1;
//lastmin = (Node*)malloc(1*sizeof(Node));
/* creating dictionary tree */
while(dict.size()>1)
{
	
	minimum = (Node*)malloc(1*sizeof(Node));
	lastmin = (Node*)malloc(1*sizeof(Node));
//	memset(&temp,0,sizeof(Node));
	sort(dict.begin(), dict.end(), sortCompare);
	*minimum = dict[dict.size()-1];																			//least frequency element
	*lastmin = dict[dict.size()-2];																			//second to least frequency element
//	std::cout << "frequencies popped : Min Freq"<< minimum->freq <<"\t"<< lastmin->freq<< std::endl;
	dict.pop_back();
	dict.pop_back();
//	for(i=0;i<dict.size();i++)
//		std::cout << "Dictionary Entry: "<< dict[i].val << "\t" << dict[i].freq<< std::endl;
	temp.val = '\0';
	temp.freq = (minimum->freq) + (lastmin->freq);															//creating a parent node with frequency = sum of lowest frequencies
	temp.left = minimum;																					//assigning left child
	temp.right = lastmin;																					//assigning right chld
	dict.push_back(temp);																					//pushing tree node to dictionary
	iter++;	
//	free(minimum);
//	free(lastmin);
}

//std::cout << "New dictionary root frequency= "<< dict[0].freq << "\t" <<std::endl;

Node *root = (Node*)malloc(1*sizeof(Node));
*root = dict[0];																							//assigning root node of dictionary
Node *next, n2n;

/* computing code for each element in the dictionary */
bool codeDetect;
int *size;
int **pattern;
size = (int*)malloc(dictionary_count*sizeof(int));
pattern = (int**)malloc(dictionary_count*sizeof(int*));
unsigned int total_size = 0;

/* generating bit pattern for each dictionary item */
for(i=0; i<dictionary_count; i++)
{
	size[i] = 0;
	pattern[i] = NULL;
	codeDetect = getCode(dictionary[i], &size[i], pattern[i], root);										//traversing tree to obtain codes and code length for each symbol	
	total_size += size[i]*frequency[i];																		//total number of bits in compressed file 
}

total_size += 8-total_size%8;

//std::cout << "Total Size of output bit array: "<< total_size << std::endl;

int *outstream = (int*)calloc(total_size,sizeof(int));
unsigned int stream_index = 0;
int l;
for(i=0;i<fileSize;i++)
{
	for(j=0;j<dictionary_count;j++)
	{
		if(data_stream[i] == dictionary[j])
		{
			for(l=0;l<size[j];l++)
				outstream[stream_index+l] = pattern[j][l];													//output stream of bits
			stream_index += size[j];						
		}
	}		
}

/* Writing meta data to the dictionary : The header format is
[No. of unique symbols in dictionary] [symbol array] [respective frequency array] */

fwrite(&dictionary_count,sizeof(unsigned char),1,fpt_out);
fwrite(dictionary,sizeof(unsigned char), dictionary_count,fpt_out);
fwrite(frequency, sizeof(int),dictionary_count, fpt_out);

unsigned char outbyte;
//outbyte = (unsigned char*)malloc((total_size/8)*sizeof(unsigned char));
//std::cout<< "output by byte" <<std::endl;
for(i=0;i<total_size/8;i++)
{
	outbyte = 0;
	for(j=0;j<8;j++)
		outbyte += outstream[i*8+j]*(pow(2,7-j));
//	std::cout << (int)outbyte << std::endl;
	fwrite(&outbyte,sizeof(unsigned char),1,fpt_out);
}

std::cout<< "Compression Concluded" << std::endl;


fclose(fpt_out);
fclose(fpt_in);
free(dictionary);
free(frequency);
free(outstream);
free(data_stream);
free(root);
free(pattern);
free(size);
free(minimum);
free(lastmin);
return 0;

}



