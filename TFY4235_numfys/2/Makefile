CC = gcc

INCLUDES = -I${realpath ./include}

CFILES   = 	$(wildcard src/*.c)

OBJFILES = $(CFILES:.c=.o)
OUT      = BBM

CFLAGS  = -g -Wall ${INCLUDES}
LDLIBS  = -lm
LDFLAGS = -g -lm

$(OUT): $(OBJFILES)

.PHONY: clean
clean:
	rm -f $(OBJFILES) $(OUT)
