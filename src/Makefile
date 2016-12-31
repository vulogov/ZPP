PYINC = $(shell python-config --includes)
PYLIB = $(shell python-config --libs)
.SUFFIXES:
.SUFFIXES: .o .c .py
SRC = zpp_config.py prefork.py zpp_log.py zpp_clp.py zpp_lib.py zpp_hb_lib.py zpp_zoo.py zpp_clips_shell.py
COBJ = ${SRC:.py=.c}
OBJ = zpp.o ${COBJ:.c=.o}
ZPP = zpp

all: $(SRC) $(ZPP)
$(ZPP): $(OBJ)
	gcc -o $@ $(PYINC) $(OBJ) $(PYLIB)
zpp.c: zpp.py
	cython --embed zpp.py
zpp.o: zpp.c
	gcc -c $(PYINC)  zpp.c
.py.c:
	cython -o $@ $<
.c.o:
	gcc -c $(PYINC) $< -o $@
clean:
	rm -f *.c *.o zpp
