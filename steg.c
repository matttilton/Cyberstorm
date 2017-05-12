#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void usage(char*);

int main(int argc, char** argv)
{
	//method and action types
	enum methods
	{
		bit = 1,
		byte
	};

	enum actions
	{
		store = 1,
		retrieve
	};

	// constants
	#define SENTINEL_LEN 6

	// variables
	enum methods method = 0;
	enum actions action = 0;
	int offset = -1;
	int interval = 1;
	char *pass = "";
	unsigned char sentinel[SENTINEL_LEN] = { 0x0, 0xff, 0x0, 0x0, 0xff, 0x0 }; // sentinel
	FILE *file;
	char *wrapper_file = "", *hidden_file = "";
	unsigned char *buff_hidden, *buff_wrapper;
	unsigned long len_hidden, len_wrapper, len_wrapper_needed;
	int i, j, k;

	//all is well?
	if(argc < 4 && argc > 7)
	{
		usage(argv[0]);
		exit(0);
	}
	// get command line args
	else
	{
		for(i=1; i<argc; i++)
		{
			if(strcmp(argv[i], "-b") ==0)
				method = bit;
			else if (strcmp(argv[i], "-B") == 0)
				method = byte;
			else if (strcmp(argv[i], "-s") == 0)
				action = store;
			else if (strcmp(argv[i], "-r") == 0)
				action = retrieve;
			else if (strncmp(argv[i], "-o", 2) == 0)
			{
				argv[i] += 2;
				wrapper_file = (char*)malloc(strlen(argv[i]) + 1);
				offset = atoi(strcpy(wrapper_file, argv[i]));
				wrapper_file = "";
			}
			else if (strncmp(argv[i], "-i", 2) == 0)
			{
				argv[i] += 2;
				wrapper_file = (char*)malloc(strlen(argv[i]) + 1);
				interval = atoi(strcpy(wrapper_file, argv[i]));
				wrapper_file = "";
			}
			else if (strncmp(argv[i], "-p", 2) == 0)
			{
				argv[i] += 2;
				wrapper_file = (char*)malloc(strlen(argv[i]) + 1);
				pass = strcpy(wrapper_file, argv[i]);
				wrapper_file = "";
			}
			else if (strncmp(argv[i], "-w", 2) == 0)
			{
				argv[i] += 2;
				wrapper_file = (char*)malloc(strlen(argv[i]) + 1);
				strcpy(wrapper_file, argv[i]);
			}
			else if (strncmp(argv[i], "-h", 2) == 0)
			{
				argv[i] += 2;
				wrapper_file = (char*)malloc(strlen(argv[i]) + 1);
				strcpy(hidden_file, argv[i]);
			}
		}
		if (method < bit || action < store || (offset < 0 && strcmp(pass, "") == 0))
		{
			usage(argv[0]);
			exit(0);
		}

		if(strcmp(pass, "") != 0)
		{
			offset = 0;
			for(j=0; j<strlen(pass); j++)
				offset += pass[j];
			offset %= 10240;
		}
	}

	//read hidden data
	if (action == store)
	{
		file = fopen(hidden_file, "rb");
		if(!file)
		{
			fprintf(stderr, "Error opening hidden file: %s\n", hidden_file);
			exit(0);
		}
		fseek(file, 0, SEEK_END);
		len_hidden = ftell(file) + SENTINEL_LEN;
		fseek(file, 0, SEEK_SET);
		buff_hidden = (unsigned char*)malloc(len_hidden + 1);
		if(!buff_hidden)
		{
			fprintf(stderr, "Error allocationg hidden file buffer\n");
			exit(0);
		}
		fread(buff_hidden, len_hidden, 1, file);
		fclose(file);

		// append the sentinel bytes
		for (i=SENTINEL_LEN; i>0; i--)
			buff_hidden[len_hidden-i] = sentinel[SENTINEL_LEN-i];
	}

	//read wrapper data
	file = fopen(wrapper_file, "rb");
	if(!file)
	{
		fprintf(stderr, "Error opening wrapper file: %s\n", wrapper_file);
		exit(0);
	}
	fseek(file, 0, SEEK_END);
	len_wrapper = ftell(file);
	//when reading, temporarily set hidden file length to wrapper file length
	if (action == retrieve)
		len_hidden = ftell(file);
	fseek(file, 0, SEEK_SET);
	buff_wrapper = (unsigned char*)malloc(len_wrapper + 1);
	if (action == retrieve)
		buff_hidden = (unsigned char*)malloc(len_wrapper + 1);
	if(!buff_wrapper)
	{
		fprintf(stderr, "Error allocating wrapper file buffer\n");
		exit(0);
	}
	fread(buff_wrapper, len_wrapper, 1, file);
	fclose(file);
	
	len_wrapper_needed = offset + len_hidden *interval * ((method == bit) ? 8 : 1);
	if (action == store && len_wrapper < len_wrapper_needed)
	{
		fprintf(stderr, "Wrapper file size is %lu, hidden file size is %lu\n", len_wrapper, len_hidden);
		fprintf(stderr, "With an offset of %i and an interval of %i, wrapper size is %lu\n", offset, interval, len_wrapper_needed);
		exit(0);
	}

	i = offset;
	j = 0;
	//embed hidden data in wrapper data
	if (action == store)
	{
		while (j < len_hidden)
		{
			if (method == bit)
			{
				// each byte of the hidden data is stored in the LSB
				for (k=0; k<8; k++)
				{
					//first isolate the 7 MSBs of the wrapper byte
					buff_wrapper[i] &= -1;
					// isolate the LSB of the hidden byte and store
					buff_wrapper[i] |= ((buff_hidden[j] & 0x80) >> 7);
					// shift right
					buff_hidden[j] <<= 1;
					i += interval;
				}
				j++;
			}
			else
			{
				//embed the data
				buff_wrapper[i] = buff_hidden[j++];
				i += interval;
				if (i > len_wrapper)
				{
					fprintf(stderr, "Error seeking to next interval");
					exit(0);
				}
			}
		}
	}
	//retrieve hidden data from wrapper data
	else
	{
		unsigned char byte;
		unsigned char sentinel_in[SENTINEL_LEN];
		int l = 0;

		while (i < len_wrapper)
		{
			if (method == bit)
			{
				//start with a fresh byte
				byte = 0;

				// fill the entire byte using shifts with 8 bytes fro...
				for (k=0; k<8; k++)
				{
					byte |= (buff_wrapper[i] & 0x1);
					if (k < 7)
						byte <<= 1;
					i += interval;
				}
				//we need to capture the sentinel
				//so store into a temp sentinel and compare
				if (byte != sentinel[l])
				{
					//if we have previous sentinel part matches
					if( l > 0)
					{
						for (k=0; k<l; k++)
							buff_hidden[j++] = sentinel_in[k];
						l=0;
					}
					//and now tack on the new byte
					buff_hidden[j++] = byte;
				}
				//we have a sentinel part match
				else
				{
					//if we have filled the sentinel, we're done
					if(l == SENTINEL_LEN-1)
						break;
					//otherwise just tack the new sentinel part on
					sentinel_in[l++] = byte;
				}
			}
			else
			{
				//start with a fresh byte
				byte = buff_wrapper[i];
				//we need to capture the sentinel
				//so store into a temp sentinel and compare
				if(byte != sentinel[l])
				{
					//if we have previous sentinel part matches
					if(l > 0)
					{
						for (k=0; k<l; k++)
							buff_hidden[j++] = sentinel_in[k];
						l=0;
					}
					//and now tack on the new byte
					buff_hidden[j++] = byte;
				}
				//we have a sentinel part match
				else
				{
					//if we have filled the sentinel, we're done
					if(l == SENTINEL_LEN-1)
						break;
					//otherwise, just tack the new sentinel part on
					sentinel_in[l++] = byte;
				}
			i += interval;
			if (i > len_wrapper)
			{
				fprintf(stderr, "Error, seeking to next interval \n");
				exit(0);
			}
			}
		}
	}
	//write output data
	if(action == retrieve)
	{
		len_wrapper = j;
		buff_wrapper = (unsigned char*)malloc(len_wrapper + 1);
		memcpy(buff_wrapper, buff_hidden, len_wrapper);
	}
	file = freopen(NULL, "wb", stdout);
	if (!file)
	{
		fprintf(stderr, "Error opening output stream\n");
		exit(0);
	}
	fwrite(buff_wrapper, 1, len_wrapper, file);
	fclose(file);

	//free pointers
	free(wrapper_file);
	if(action == store)
		free(hidden_file);
	free(buff_hidden);
	free(buff_wrapper);
	return 0;
}

void usage(char *n)
{
	fprintf(stderr, "Usage: %s -(bB) -(sr) -o<val> [-i<val>] -w<val> [-h<val>]\n", n);
	fprintf(stderr, "-b\t\tUse the bit method\n");
	fprintf(stderr, "-s\t\tUse the byte method\n");
	fprintf(stderr, "-r\t\tRetrieve hidden data\n");
	fprintf(stderr, "-o<val>\tSet offset to <val>\n");
	fprintf(stderr, "-i<val>\tSet interval to <val>\n");
	fprintf(stderr, "-w<val>\tSet wrapper file to <val>\n");
	fprintf(stderr, "-h<val>\tSet hidden file to <val>\n");
}
