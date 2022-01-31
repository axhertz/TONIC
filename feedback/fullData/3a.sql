/*+HashJoin(mi t)HashJoin(mk k)NestLoop(mi t mk k)*/ time: 40.00199508666992 / 40.00199508666992
/*+NestLoop(mi t)HashJoin(mk k)NestLoop(mi t mk k)*/ time: 40.002140522003174 / 40.002140522003174
/*+HashJoin(mi t)HashJoin(mk k)HashJoin(mi t mk k)*/ time: 1.9123857021331787 / 1.8966014385223389
/*+HashJoin(mi t)NestLoop(mk k)HashJoin(mi t mk k)*/ time: 2.525921106338501 / 2.5238828659057617
/*+NestLoop(mi t)HashJoin(mk k)HashJoin(mi t mk k)*/ time: 1.8142030239105225 / 3.083181619644165
/*+NestLoop(mi t)NestLoop(mk k)HashJoin(mi t mk k)*/ time: 2.4506657123565674 / 2.446298360824585
/*+NestLoop(mi t)HashJoin(mk k)HashJoin(mi t mk k)*/ best_time: 1.8142030239105225 / 1.8142030239105225
