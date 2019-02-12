CCC= g++
PARAMETERS = -O3 -lm 

fisherVector: main.o fisherVector.o
	$(CCC) $(PARAMETERS) -o fisherVector main.o fisherVector.o

main.o: main.cpp
	$(CCC) $(PARAMETERS) -c main.cpp -o main.o

fisherVector.o: fisherVector.cpp
	$(CCC) $(PARAMETERS) -c fisherVector.cpp -o fisherVector.o

clean:
	rm -f *.o fisherVector *~
