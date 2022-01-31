/*+HashJoin(mi t)HashJoin(mk k)NestLoop(mi t mk k)*/ time: 40.010948181152344 / 40.010948181152344
/*+HashJoin(mi t)HashJoin(mk k)HashJoin(mi t mk k)*/ time: 2.242128610610962 / 2.2649343013763428
/*+HashJoin(mi t)NestLoop(mk k)HashJoin(mi t mk k)*/ time: 3.017612934112549 / 3.06387996673584
/*+NestLoop(mi t)HashJoin(mk k)HashJoin(mi t mk k)*/ time: 2.4854650497436523 / 3.4105989933013916
/*+NestLoop(mi t)NestLoop(mk k)HashJoin(mi t mk k)*/ time: 3.3614413738250732 / 3.3600900173187256
/*+HashJoin(mi t)HashJoin(mk k)HashJoin(mi t mk k)*/ best_time: 2.242128610610962 / 2.242128610610962
