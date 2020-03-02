#include <stdio.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <ctype.h>
#include <fcntl.h>
#include <cups/ppd.h>
#include <cups/raster.h>

#define	OTHER_WIDTH			48

#define	CUT_TIMING_PAGE_END		0x01U
#define	CUT_TIMING_DOCUMENT_END		0x02U
#define	CUT_TYPE_FULL			0x04U
#define	CUT_TYPE_PARTIAL		0x08U

typedef struct _options {
	unsigned char	PaperCut;
	unsigned char	FeedSizeBeforePrinting;
	unsigned char	FeedSizeAfterPrinting;
} OPTIONS;

typedef unsigned char	BOOL;

#ifndef TRUE
	#define	TRUE	1
	#define	FALSE	0
#endif

static volatile BOOL Canceled;

static void CancelJob(int sig)
{
	Canceled = TRUE;
}


static void GetPageSize(ppd_file_t * ppd, int *page_width, int *page_height)
{
ppd_choice_t * choice;
ppd_option_t * option;
char width[32],height[32];
char *pageSize,*work;
int idx;
int i,j;

	choice = ppdFindMarkedChoice(ppd, "PageSize");
	if (choice == NULL) {
		option = ppdFindOption(ppd, "PageSize");
		choice = ppdFindChoice(option,option->defchoice);
	}
	memset(width, 0x00, sizeof(width));
	memset(height, 0x00, sizeof(height));

	pageSize = choice->choice;
	idx = 0;

	if (pageSize[idx] != 0x00) {
		work = &pageSize[idx];
		if((work[0] == 'w')||
		   (work[0] == 'W'))
		{
			j = 0;
			for(i=1;isdigit(work[i]);i++) {
				width[j++] = work[i];
			}
			width[j] = 0x00;
			if((work[i] == 'h')||
			   (work[i] == 'H'))
			{
				j = 0;
				for(i++;isdigit(work[i]);i++) {
					height[j++] = work[i];
				}
				height[j] = 0x00;
			}
		}
	}
	*page_width = (int)atof(width);
	*page_height = (int)atof(height);
}


static void SetupOptions(ppd_file_t *ppd, OPTIONS* options)
{
ppd_choice_t	*choice;
ppd_option_t	*option;
	
	// Read Paper Cut option
	options->PaperCut = 0;

	choice = ppdFindMarkedChoice(ppd, "PaperCut");
	if (choice == NULL) {
		option = ppdFindOption(ppd, "PaperCut");
		choice = ppdFindChoice(option,option->defchoice);
	}

	if (choice != NULL) {
		if (strcmp(choice->choice, "PageEndFull") == 0) {
			options->PaperCut = CUT_TIMING_PAGE_END | CUT_TYPE_FULL;
		}
		else if (strcmp(choice->choice, "PageEndPartial") == 0) {
			options->PaperCut = CUT_TIMING_PAGE_END | CUT_TYPE_PARTIAL;
		}
		else if (strcmp(choice->choice, "DocEndFull") == 0) {
			options->PaperCut = CUT_TIMING_DOCUMENT_END | CUT_TYPE_FULL;
		}
		else if (strcmp(choice->choice, "DocEndPartial") == 0) {
			options->PaperCut = CUT_TIMING_DOCUMENT_END | CUT_TYPE_PARTIAL;
		}
	}

	// Read "Feed Size Before Printing" option
	options->FeedSizeBeforePrinting = 0;
	choice = ppdFindMarkedChoice(ppd, "FeedSizeBeforePrinting");
	if (choice == NULL) {
		option = ppdFindOption(ppd, "FeedSizeBeforePrinting");
		choice = ppdFindChoice(option,option->defchoice);
	}

	if (choice != NULL) {
		if (strncmp(choice->choice, "BF", 2) == 0) {
			int i;
			for (i = 2;  choice->choice[i] && (i < 4);  i++) {
				options->FeedSizeBeforePrinting *= 10;
				options->FeedSizeBeforePrinting += choice->choice[i] - '0';
			}
		}
	}

	// Read "Feed Size After Printing" option
	options->FeedSizeAfterPrinting = 0;
	choice = ppdFindMarkedChoice(ppd, "FeedSizeAfterPrinting");
	if (choice == NULL) {
		option = ppdFindOption(ppd, "FeedSizeAfterPrinting");
		choice = ppdFindChoice(option,option->defchoice);
	}

	if (choice != NULL) {
		if (strncmp(choice->choice, "AF", 2) == 0) {
			int i;
			for (i = 2;  choice->choice[i] && (i < 4);  i++) {
				options->FeedSizeAfterPrinting *= 10;
				options->FeedSizeAfterPrinting += choice->choice[i] - '0';
			}
		}
	}
}


static void PaperFeed(unsigned char mm)
{
	if (mm != 0) {
		unsigned char dot = mm * 8;	// 203dpi
		unsigned char command[3];
		
		command[0] = 0x1b;
		command[1] = 0x4a;
		command[2] = dot;
		fwrite(command, sizeof(command), 1, stdout);
	}
}

static void PaperCut(unsigned char paperCutOption)
{
static const unsigned char commandFullCut[2] = { 0x1b, 0x69 };
static const unsigned char commandPartialCut[2] = { 0x1b, 0x6d };
	
	if (paperCutOption & CUT_TYPE_FULL) {
		// Full Cut
		fwrite(commandFullCut, sizeof(commandFullCut), 1, stdout);
	}
	else if (paperCutOption & CUT_TYPE_PARTIAL) {
		// Partial Cut
		fwrite(commandPartialCut, sizeof(commandPartialCut), 1, stdout);
	}
}

int main(int argc, char* argv[])
{
cups_raster_t		*ras;
cups_page_header2_t	header;
ppd_file_t		*ppd;
int			numOptions;
cups_option_t		*cupsOptions;
int			fd;
int			page = 0;
int			y;
unsigned char		*buffer;
unsigned char		command[5];
OPTIONS			options;
int			page_width,page_height,lineSize;
	
	// Initialize //////////////////////////////////////////////////////
	setbuf(stderr, NULL);
	
	// Command line paramater check
	if ((argc < 6) || (argc > 7)) {
		fprintf(stderr, "Usage: %s job-id user title copies options [file]\n", argv[0]);
		return 1;
	}
	if (argc == 7) {
		if ((fd = open(argv[6], O_RDONLY)) == -1) {
			perror("ERROR: Unable to open raster file - ");
			return 1;
		}
	}
	else {
		fd = 0;	// standerd in
	}
	
	// Open raster stream
	ras = cupsRasterOpen(fd, CUPS_RASTER_READ);
	
	// Setup signals
	Canceled = FALSE;
	signal(SIGTERM, CancelJob);

	// Open ppd file
	numOptions = cupsParseOptions(argv[5], 0, &cupsOptions);
	if ((ppd = ppdOpenFile(getenv("PPD"))) != NULL) {
		ppdMarkDefaults(ppd);
		cupsMarkOptions(ppd, numOptions, cupsOptions);
	}

	// Get page size
	GetPageSize(ppd,&page_width,&page_height);
	page_width /= 8;

	// Setup options
	SetupOptions(ppd, &options);

	// Document start ////////////////////////////////////////
	while ((Canceled == FALSE) && cupsRasterReadHeader2(ras, &header))  {
		// Page start /////////////////////////////////////////////
		page++;
		fprintf(stderr, "PAGE: %d %d\n", page, header.NumCopies);
		
		// Paper feed
		PaperFeed(options.FeedSizeBeforePrinting);

#ifdef MODEL_SK1
		// Allocate line pixel buffer
		buffer = (unsigned char*)malloc(header.cupsBytesPerLine);
#else
		// Allocate line pixel buffer
		if(header.cupsBytesPerLine < OTHER_WIDTH) {
			// Allocate line pixel buffer
			buffer = (unsigned char*)malloc(OTHER_WIDTH);
		}
		else {
			// Allocate line pixel buffer
			buffer = (unsigned char*)malloc(header.cupsBytesPerLine);
		}
#endif

		// Page print ////////////////////////////////////////////////////
#ifdef MODEL_SK1
		if(header.cupsBytesPerLine <= page_width) {
			lineSize = header.cupsBytesPerLine;
		}
		else {
			lineSize = page_width;
		}
		command[0] = 0x1b;
		command[1] = 0x62;
		command[2] = lineSize;
		command[3] = header.cupsHeight & 0x0ffU;
		command[4] = (header.cupsHeight >> 8) & 0x0ffU;
		fwrite(command, 5, 1, stdout);
#else
		lineSize = OTHER_WIDTH;
		command[0] = 0x12;
		command[1] = 0x56;
		command[2] = header.cupsHeight & 0x0ffU;
		command[3] = (header.cupsHeight >> 8) & 0x0ffU;
		fwrite(command, 4, 1, stdout);
#endif

		for (y = 0; y < header.cupsHeight; y ++) {
#ifndef MODEL_SK1
			memset(buffer, 0, OTHER_WIDTH);
#endif
			if ((y & 0x0ff) == 0) {
				fprintf(stderr, "INFO: Printing page %d, %d%% complete...\n", page, 100 * y / header.cupsHeight);
			}
			// Read line pixels (1pixel == 1bit)
			if (cupsRasterReadPixels(ras, buffer, header.cupsBytesPerLine) == 0) {
				memset(buffer, 0, header.cupsBytesPerLine);
			}
			// Print line
			fwrite(buffer, lineSize, 1, stdout);
			fflush(stdout);
		}
		// Page finish //////////////////////////////////////////////////////
		// Free line pixel buffer
		free(buffer);
		
		if (Canceled == FALSE) {
			// Paper feed
			PaperFeed(options.FeedSizeAfterPrinting);
			
			// Paper cut
			if (options.PaperCut & CUT_TIMING_PAGE_END) {
				PaperCut(options.PaperCut);
			}
			fflush(stdout);
		}
	}
	
	// Document finish /////////////////////////////////////////////////
	if (Canceled == FALSE) {
		// Paper cut
		if (options.PaperCut & CUT_TIMING_DOCUMENT_END) {
			PaperCut(options.PaperCut);
		}
	}
	
	// Finalize ////////////////////////////////////////////////////////
	// Close raster stream
	cupsRasterClose(ras);
	if (fd != 0) {
		close(fd);
	}
	
	// Close ppd file
	ppdClose(ppd);
	
	// Free options
	cupsFreeOptions(numOptions, cupsOptions);
	
	if (page == 0) {
		fputs("ERROR: No pages found!\n", stderr);
	}
	else {
		fputs("INFO: Ready to print.\n", stderr);
	}
	
	return 0;
}

