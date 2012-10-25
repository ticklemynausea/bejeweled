
import logic
import sys
import time

time_1 = []
time_2 = []
time_3 = []

iter_1 = []
iter_2 = []
iter_3 = []

chain_1 = []
chain_2 = []
chain_3 = []

jewel_1 = []
jewel_2 = []
jewel_3 = []

score_1 = []
score_2 = []
score_3 = []

argdepth = int(sys.argv[1])
argplay = int(sys.argv[2])

argplayer = sys.argv[3]

print argplayer

for plays in range(argplay):
	time_i = time.time()
	game = logic.Logic(
			limit=200, 
			player=argplayer, 
			columns=8, 
			rows=8, 
			colours=7, 
			depth=argdepth, 
			minenergy=5, 
			pause=False, 
			graphical=False, 
			energythreshold=10, 
			shorten=True)
	resultado = game.play()
	#print "\n\n\n\n\n\n\n\nIteracoes: ", resultado[0],"\nTotalChain: ", resultado[1], "\nJoias: ", resultado[2], "\nScore: ", resultado[3], "\nDEPTH: ", depth
	time_f = time.time()

	iter_3.append(resultado[0])
	chain_3.append(resultado[1])
	jewel_3.append(resultado[2])
	score_3.append(resultado[3])
	time_3.append(time_f-time_i)
	

mean_iter_3 = sum(iter_3)/len(iter_3)
min_iter_3 = min(iter_3)
max_iter_3 = max(iter_3)

for i in iter_3:
	i -= mean_iter_3
	i = i**2
desvio_i3 = sum(iter_3)/(len(iter_3)-1)


mean_time_3 = sum(time_3)/len(time_3)
min_time_3 = min(time_3)
max_time_3 = max(time_3)

for i in iter_3:
	i -= mean_time_3
	i = i**2
desvio_t3 = sum(time_3)/(len(time_3)-1)

mean_score = sum(score_3)/len(score_3)
min_score = min(score_3)
max_score = max(score_3)

for i in score_3:
	i -= mean_score
	i = i**2
desvio_s3 = sum(score_3)/(len(score_3)-1)


mean_chain = sum(chain_3)/len(chain_3)
min_chain = min(chain_3)
max_chain = max(chain_3)
for i in chain_3:
	i -= mean_chain
	i = i**2
desvio_c3 = sum(chain_3)/(len(chain_3)-1)


mean_joi = sum(jewel_3)/len(jewel_3)
min_joi = min(jewel_3)
max_joi = max(jewel_3)
for i in jewel_3:
	i -= mean_joi
	i = i**2
desvio_j3 = sum(jewel_3)/(len(jewel_3)-1)

print "\n\n\n\n"

print argplayer
print "Depth ", argdepth
print "Runs ", argplay
print "\nIteracoes"
print "\tMinimo", min_iter_3
print "\tMaximo ", max_iter_3
print "\tMedia ", mean_iter_3
print "\tDesvio ",desvio_i3
print "Tempo"
print "\tMinimo ", min_time_3
print "\tMaximo ", max_time_3
print "\tMedio ", mean_time_3
print "\tDesvio ", desvio_t3
print "\tTOTAL APROX ", mean_time_3*argplay
print "Pontos"
print "\tMinimo ", min_score
print "\tMaximo ", max_score
print "\tMedio ", mean_score
print "\tDesvio ", desvio_s3
print "Chain"
print "\tMinimo ", min_chain
print "\tMaximo ", max_chain
print "\tMedio ", mean_chain
print "\tDesvio ", desvio_c3
print "Joias"
print "\tMinimo ", min_joi
print "\tMaximo ", max_joi
print "\tMedio ", mean_joi
print "\tDesvio ", desvio_j3


f = open("output2.txt", "w")
print >> f, argplayer
print >> f, "Depth ", argdepth
print >> f, "Runs ", argplay
print >> f, "\nIteracoes"
print >> f, "\tMinimo", min_iter_3
print >> f, "\tMaximo ", max_iter_3
print >> f, "\tMedia ", mean_iter_3
print >> f, "\tDesvio ",desvio_i3
print >> f, "Tempo"
print >> f, "\tMinimo ", min_time_3
print >> f, "\tMaximo ", max_time_3
print >> f, "\tMedio ", mean_time_3
print >> f, "\tDesvio ", desvio_t3
print >> f, "\tTOTAL APROX ", mean_time_3*argplay
print >> f, "Pontos"
print >> f, "\tMinimo ", min_score
print >> f, "\tMaximo ", max_score
print >> f, "\tMedio ", mean_score
print >> f, "\tDesvio ", desvio_s3
print >> f, "Chain"
print >> f, "\tMinimo ", min_chain
print >> f, "\tMaximo ", max_chain
print >> f, "\tMedio ", mean_chain
print >> f, "\tDesvio ", desvio_c3
print >> f, "Joias"
print >> f, "\tMinimo ", min_joi
print >> f, "\tMaximo ", max_joi
print >> f, "\tMedio ", mean_joi
print >> f, "\tDesvio ", desvio_j3

print >> f, "\n\n\n\n"
print >> f, "\n\n\n\n"
