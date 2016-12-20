PYINC = $(shell python-config --includes)
PYLIB = $(shell python-config --libs)

all: zpp
zpp: prefork.o zpp.o
	gcc -o zpp $(PYINC) zpp.o prefork.o $(PYLIB)
zpp.c: zpp.py
	cython --embed zpp.py
zpp.o: zpp.c
	gcc -c $(PYINC)  zpp.c
prefork.c: prefork.py
	cython prefork.py
prefork.o: prefork.c
	gcc -c $(PYINC) prefork.c
clean:
	rm -f zpp.c prefork.c *.o zpp
