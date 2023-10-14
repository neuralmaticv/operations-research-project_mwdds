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
  - [Uputstvo za lokalno pokretanje](#uputstvo-za-lokalno-pokretanje)
  - [Neki korisni linkovi:](#neki-korisni-linkovi)
  - [Licenca](#licenca)
---

## Opis projekta
**Tema projekta:** Minimum weight directde dominating set problem

**Autori:** [Vladimir Mijić](https://github.com/neuralmaticv) i [Bojan Gavrić](https://github.com/BokaG)
#### Problem
U teoriji grafova, minimalni dominantni skup u usmjerenom težinskom grafu (minimum weighted directed dominating set - MWDDS) problem je optimizacioni problem koji se odnosi na
pronalaženje najmanjeg podskupa čvorova u usmjerenom težinskom grafu (težine su na čvorovima) tako da svaki čvor 
tog grafa može biti dosegnut iz najmanje jednog čvora koji se nalazi u tom podskupu. Takav podskup se naziva dominantni skup.   
 
MWDDS problem je NP težak problem, što znači da ga je teško riješiti i da nije poznat efikasan algoritam za pronalaženje tačnog rješenja. Ali je moguće pronaći približna rješenja različitim pristupima.

Prvi pristup rješavanju MWDDS problema je korištenje heurističkog algoritma, kao što je pohlepno ili lokalno pretraživanje,
za pronalaženje približnog rješenja. Heuristički algoritmi mogu biti brzi u pronalasku rješenja, ali ne garantuju da će 
to rješenje biti optimalno.  

Drugi pristup za rješavanje ovog problema je putem Integer linear programming (ILP).  
ILP model možemo formulisati:  
* G=(V, E) je usmjereni graf, gdje je V skup čvorova, a E je skup grana.
* Neka je n = |V| i m = |E|
* Neka je $x_i$ binarna varijabla koja označava da li je čvor *i* uključen u dominantni skup (tada $x_i$ = 1), u suprotnom ( $x_i$ = 0)  

Cilj je minimizovati sumu težina onih čvorova koji se nalaze u dominantnom skupu.  
  
$$min (\sum_{i}^{V} w_i * x_i)$$


gdje sa $w_i$ označavamo težinu čvora *i*.  

Ograničnja obezbjeđuju da svaki čvor u grafu može biti dosegnut iz najmanje jednog čvora iz dominantnog skupa.  


<p align="center">
$x_i + \sum_{v_j \in \overset{-}{N}_G(v_i)} x_j \geq 1 \quad \forall v_i \in V$
</p>
  
<br>
Ovaj problem ima mnogo praktičnih primjena:  

1. Dizajniranje i analiza telekomunikacionih mreža - npr. može se koristiti za pronalaženje najmanjeg skupa pristupnih tačaka kako bi se osigurala pokrivenost i efikasnost mreže (i slični problemi iz drugih oblasti gdje je potrebno pronaći neku grupu tačaka);
2. Dizajniranje VLSI integrisanih kola;
3. Rudarenju podataka (data mining), bioinformatici, itd. 


#### Zadatak
1) Definicija prostora pretrage, funkcije cilja, funkcija prilagodljivosti (po mogućnosti), komponente rješenja.
2) Pohlepni pristup rješavanju problema gdje treba definisati  pohlepnu funkciju, dodavanje komponente u rješenje.
3) Odabrati genetski ili VNS pristup
     - Za genentski: definisati jedinku, operator selekcije, ukrštanja, operator mutacije.
     - Za VNS: definisati lokalnu pretragu, strukture okolina, objasniti zašto su baš takve uzete.

4) Implementirati model u [PuLP](https://coin-or.github.io/pulp/)

---

### Struktura repozitorijuma:
- `/docs` 	seminarski rad i još neki radovi na ovu temu
- `/instances` 	instance grafova, podijeljene u kategorije - test, small, medium, large
- `/main`	Python skripte koje sadrže implementacije algoritama
- `/notebooks` 	Jupyter notebook-ovi za testiranje algoritama i vizualizaciju.
- `/results` 	eksperimentalni rezultati
- `/utils`  pomoćne skripte
---

### Rezultati
![Primjer minimalnog dominantnog skupa u usmjerenom težinskom grafu](https://github.com/neuralmaticv/operations-research-project_mwdds/blob/main/instances/images/instance_05_06_graph_bhs.png)

![Rezultati za testne instance](https://github.com/neuralmaticv/operations-research-project_mwdds/blob/main/results/images/small_results_overview_bhs.png)

---

### Literatura

* Nakkala, M.R., Singh, A. (2020). Heuristics for Minimum Weight Directed Dominating Set Problem. In: Singh, P., Sood, S., Kumar, Y., Paprzycki, M., Pljonkin, A., Hong, WC. (eds) Futuristic Trends in Networks and Computing Technologies. FTNCT 2019. Communications in Computer and Information Science, vol 1206. Springer, Singapore. [link](https://doi.org/10.1007/978-981-15-4451-4_39)

* Albuquerque, M., & Vidal, T. (2018). An efficient matheuristic for the minimum-weight dominating set problem. Applied Soft Computing, 72, 527-538. [link](https://doi.org/10.1016/j.asoc.2018.06.052)

* Jovanovic, R., Tuba, M., & Simian, D. (2010). Ant colony optimization applied to minimum weight dominating set problem. 12th WSEAS International Conference on Automatic Control, Modelling and Simulation, ACMOS '10. 322-326. [link](https://www.researchgate.net/publication/262354402_Ant_colony_optimization_applied_to_minimum_weight_dominating_set_problem)

* Vazirani, V. V. (2003). Approximation algorithms. Springer. [link](https://link.springer.com/book/10.1007/978-3-662-04565-7)

* Williamson, D. P., & Shmoys, D. B. (2011). The design of approximation algorithms. Cambridge University Press. [link](https://www.designofapproxalgs.com/index.php)

* Đukanović, M., & Matić, D. (2022). Uvod u operaciona istraživanja. Prirodno-matematički fakultet, Univerzitet u Banjoj Luci. [link](https://drive.google.com/file/d/18arqs1f0SVbmAzVdUGGJfMxRIP306byn/view)

---

### Uputstvo za lokalno pokretanje
1. Klonirajte repozitorij na svoj lokalni računar:  
   ova komanda će kreirati folder `mwdds_test` i u njemu klonirati projekat
   ```bash
   git clone https://github.com/neuralmaticv/operations-research-project_mwdds.git mwdds_test
   cd mwdds_test
   ```
3. Kreiranje virtuelnog okruženja i instaliranje potrebnih paketa
   ```bash
   python -m venv venv

   # za operativni sistem zasnovan na UNIX-u
   source venv/bin/activate

   # za operativni sistem Windows
   venv\Scripts\activate

   pip install -r requirements.txt
   ```
4. Pokretanje Jupyter Notebook-a:
   ```bash
   jupyter notebook
   ```
   Jupyter Notebook će se pokrenuti u vašem web pregledaču i sada možete otvoriti postojeće notebook-ove iz foldera `/notebooks` i raditi s njima.

   
---

### Neki korisni linkovi:

* [NetworkX package](https://networkx.org/documentation/stable/index.html)

* [Generator for docstrings](https://github.com/airtai/docstring-gen)

* [Network Repository - An Interactive Scientific Network Data Repository](https://networkrepository.com/)

---

* [The House of Graphs - Database of interesting graphs](https://houseofgraphs.org/)

* [Stanford Large Network Dataset Collection](https://snap.stanford.edu/data/)

* [igraph package](https://igraph.readthedocs.io/en/0.10.2/index.html)

* [graph tool package](https://graph-tool.skewed.de/)

* [Sage](https://doc.sagemath.org/html/en/reference/index.html)


### Licenca
[GNU General Public License v3.0](https://github.com/neuralmaticv/operations-research-project_mwdds/blob/main/LICENSE)
