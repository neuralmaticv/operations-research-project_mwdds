# Projekat za predmet Operaciona istraživanja

## Sadržaj:
- [Projekat za predmet Operaciona istraživanja](#projekat-za-predmet-operaciona-istraživanja)
  - [Sadržaj:](#sadržaj)
  - [Opis projekta](#opis-projekta)
    - [Problem](#problem)
    - [Zadatak](#zadatak)
    - [Struktura repozitorijuma:](#struktura-repozitorijuma)
    - [Rezultati](#rezultati)
    - [Literatura](#literatura)
    - [Neki korisni linkovi:](#neki-korisni-linkovi)
    - [TODO lista:](#todo-lista)
    - [Licenca](#licenca)

---

## Opis projekta
**Tema projekta:** Minimum weight directed dominating set problem

**Autori:** [Vladimir Mijić](https://github.com/neuralmaticv) 

### Problem
U teoriji grafova, minimum weighted directed dominating set (MWDDS) problem je optimizacioni problem koji se odnosi na
pronalaženje najmanjeg podskupa čvorova u usmjerenom težinskom grafu (težine su na čvorovima) tako da svaki čvor 
tog grafa može biti dosegnut iz najmanje jednog čvora koji se nalazi u tom podskupu. Takav podskup se naziva dominirajući skup.   
 
MWDDS problem je NP težak problem, što znači da ga je teško riješiti i da nije poznat efikasan algoritam za pronalaženje tačnog rješenja. Ali je moguće pronaći približna rješenja različitim pristupima.

Prvi pristup rješavanju MWDDS problema je korištenje heurističkog algoritma, kao što je pohlepno ili lokalno pretraživanje,
za pronalaženje približnog rješenja. Heuristički algoritmi mogu biti brzi u pronalasku rješenja, ali ne garantuju da će 
to rješenje biti optimalno.  

Drugi pristup za rješavanje ovog problema je putem Integer linear programming (ILP).  
ILP model možemo formulisati:  
* G=(V, E) je usmjereni graf, gdje je V skup čvorova, a E je skup grana.
* Neka je n = |V| i m = |E|
* Neka je $x_i$ binarna varijabla koja označava da li je čvor *i* uključen u dominirajući skup (tada $x_i$ = 1), u suprotnom ( $x_i$ = 0)  

Cilj je minimizovati sumu težina onih čvorova koji se nalaze u dominirajućem skupu.  
  
$$min (\sum_{i}^{V} w_i * x_i)$$


gdje sa $w_i$ označavamo težinu čvora *i*.  

Ograničnja obezbjeđuju da svaki čvor u grafu može biti dosegnut iz najmanje jednog čvora iz dominirajućeg skupa.  


<p align="center">
$\sum_{(i,j) \in E} x_j \ge x_i$, for all $i \in V$
</p>
  
<br>
Ovaj problem ima mnogo praktičnih primjena:  

1. Dizajniranje i analiza telekomunikacionih mreža - npr. može se koristiti za pronalaženje najmanjeg skupa pristupnih tačaka kako bi se osigurala pokrivenost i efikasnost mreže (i slični problemi iz drugih oblasti gdje je potrebno pronaći neku grupu tačaka);
2. Dizajniranje VLSI integrisanih kola;
3. Bioinformatici, itd. 

---

### Zadatak
1) Definicija prostora pretrage, funkcije cilja, funkcija prilagodljivosti (po mogućnosti), komponente rješenja.
2) Pohlepni pristup rješavanju problema gdje treba definisati  pohlepnu funkciju, dodavanje komponente u rješenje.
3) Odabrati genetski ili VNS pristup
     - Za genentski: definisati jedinku, operator selekcije, ukrštanja, operator mutacije.
     - Za VNS: definisati lokalnu pretragu, strukture okolina, objasniti zašto su baš takve uzete.

4) Implementirati model u [PuLP](https://coin-or.github.io/pulp/)


### Struktura repozitorijuma:
- `/docs` 	neki radovi na ovu temu
- `/instances` 	instance grafova, podijeljene po dimenziji u tri skupa
- `/main`	implementacije algoritama
- `/notebooks` 	primjeri korištenja algoritama
- `/results` 	rezultati i seminarski rad
- `/utils`  pomoćne skripte za rad sa grafovima

### Rezultati
`TODO: dodati tabelarni prikaz ili screenshot-ove`


### Literatura

* Nakkala, M.R., Singh, A. (2020). Heuristics for Minimum Weight Directed Dominating Set Problem. In: Singh, P., Sood, S., Kumar, Y., Paprzycki, M., Pljonkin, A., Hong, WC. (eds) Futuristic Trends in Networks and Computing Technologies. FTNCT 2019. Communications in Computer and Information Science, vol 1206. Springer, Singapore. [link](https://doi.org/10.1007/978-981-15-4451-4_39)

* Albuquerque, M., & Vidal, T. (2018). An efficient matheuristic for the minimum-weight dominating set problem. Applied Soft Computing, 72, 527-538. [link](https://doi.org/10.1016/j.asoc.2018.06.052)

* Jovanovic, R., Tuba, M., & Simian, D. (2010). Ant colony optimization applied to minimum weight dominating set problem. 12th WSEAS International Conference on Automatic Control, Modelling and Simulation, ACMOS '10. 322-326. [link](https://www.researchgate.net/publication/262354402_Ant_colony_optimization_applied_to_minimum_weight_dominating_set_problem)


### Neki korisni linkovi:

* [Google Colab](https://colab.research.google.com/)

* [Generator for docstrings](https://github.com/airtai/docstring-gen)

* [Network Repository - An Interactive Scientific Network Data Repository](https://networkrepository.com/)

* [The House of Graphs - Database of interesting graphs](https://houseofgraphs.org/)

* [Stanford Large Network Dataset Collection](https://snap.stanford.edu/data/)

* [NetworkX package](https://networkx.org/documentation/stable/index.html)

* [igraph package](https://igraph.readthedocs.io/en/0.10.2/index.html)

* [graph tool package](https://graph-tool.skewed.de/)

* [Sage](https://doc.sagemath.org/html/en/reference/index.html)


### TODO lista:
- [ ] Pustiti algoritme na nekim instancama iz rada "Ant Colony Optimization Applied to Minimum Weight Dominating Set Problem" - [instance su dostupne ovdje](https://mail.ipb.ac.rs/~rakaj/home/BenchmarkMWDSP.htm)
- [ ] Uraditi paralelizaciju
1. Greedy algoritam:
    - [ ] prilikom sortiranja cvorova, uzeti u obzir i stepen cvora. (npr. `Wi*(1 - (Di * 0.001)`)
2. Genetski algoritam:
   - [ ] uvesti elitizaciju (elitism) - odabrati samo par najboljih jedinki
   - [ ] penalizovati nedopustiva rjesenja
   - [ ] dodati local search  


### Licenca
[GNU General Public License v3.0](https://github.com/neuralmaticv/operations-research-project_mwdds/blob/main/LICENSE)
