# Foreword

| <a href="intro_de.html" > Deutsch </a> | [Italiano](italiano_intro) | [Francais](francais_intro) |

The aim of this project was to collect data and develop the necessary infrastructure to accurately assess the composition and abundance of anthropogenic material along selected Swiss rivers and lakes and present those findings in a consolidated web-based report.

There are at least three manuscripts being prepared that use data or explore techniques in this report:

__Detecting accumulation and leakage with Spearman's Rho__, *collaboration with Louise Schreyers, [Wageningen University and Research](https://www.wur.nl/).* [Repository](https://github.com/hammerdirt-analyst/landuse)

__The probability of finding an object__, *collaboration with Romain Tramoy, Laboratoire Eau Environment et Systèmes Urbains [LEESU](https://www.leesu.fr/), Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Montserrat Filella, [_Department F.-A. Forel, University of Geneva_](https://www.unige.ch/forel/fr/).* [Repository](https://github.com/hammerdirt-analyst/finding-one-object)

__Monitoring trash with the next generation of Solid waste engineers 2016-2021__, *collaboration with Bhavish Patel, [_Paul Scherer Institute_](https://www.psi.ch/en), Christian Ludwig, [_Paul Scherrer Institute_](https://www.psi.ch/en)/[_EPFL_](https://www.epfl.ch/en/).* [Repository](https://github.com/hammerdirt-analyst/swe)

## Assessment method

In 2008 the first international guide to monitoring beach-litter was published by the United Nations Environment Program (UNEP) and Intergovernmental Oceanographic Commission (IOC) {cite}`unepseas`. This method was reproduced by the OSPAR Commission in 2010 {cite}`ospard10`.  In 2013 the EU released Guidance on Monitoring of Marine Litter in European Seas (The guide) {cite}`mlwguidance`. Switzerland is a member of OSPAR and has over 1,400 samples using the methods described in The guide. 

*A beach-litter survey is the accounting of visible anthropogenic material identified within a delimited area that is bordered on one side by a lake, river or ocean.*

* Locations are defined by their GPS points 
* Length and width are measured for each survey area 
* Visible pollutants within the survey area are collected, classified, counted and weighed
* All items are classified based on code definitions included in _The guide_.

To identify objects of regional interest supplementary codes were added. For example, codes were developed for items such as pheromone bait containers and ski poles to account for the occurrence of these objects when identified in certain regions. Identifying and quantifying items allows researchers and stakeholders to determine probable sources and define reduction strategies targeting specific items. 

For more information: [Code groups](codegroups).

## Assessment metric

The median value (50th percentile) of the survey results is reported as the number of objects per 100m (p/100m) of shoreline. This is the method described in EU Marine Beach Litter Baselines {cite}`eubaselines` and is the standard used in this report. The 100-meter shoreline standard used in the marine environment is appropriate for coastal regions of the European continent. However, urbanization and topography present unique challenges when selecting locations suitable to safely conduct yearlong shoreline litter surveys.

Limiting surveys to 100 meters of exposed shoreline would have dramatically reduced the number of available survey locations as well as the use of preexisting data. Thus, the IQAASL reflects local topography with a median survey length of 45m, and an average of 51m. Surveys less than 10m were not considered in the baseline analysis. The survey results are converted to p/100m by multiplying the survey result by 100.

### Collecting data

A beach litter survey can be conducted by anybody at anytime. If the survey is conducted according to the method described in The Guide {cite}`mlwguidance` or [Beach litter baselines](threshhold) the result can be compared directly to the charts in this report. There is no need to enter the data into the system to compare results. 

__Collecting data__ for the report (or the next report) requires some on the job training and an evaluation. It usually takes 3-5 surveys to acclimate an individual to the task. Most of the time is spent identifying objects and the importance of maintaining a field notebook. The advantage to contributing data is that the reporting procedure is automated and there is always access to the results. 

## Using this report

It is important to understand the difference between the _median_ {cite}`mediandef` and the _average_ {cite}`meandeff` when interpreting the results. Except for monthly results the survey results are given as the __median__ p/100m for the location in question. 

As an example, consider the __median__ survey result for the most common objects on Thunersee and Brienzersee.


```{figure} resources/images/intro/thunersee_brienzersee_20_0.png
---
width: 600px
name: mcommonforeword
---

` `

```

{numref}`Figure {number}: <mcommonforeword>` _Interpreting the survey results. The aggregated results from all survey areas are on the far-right column, preceded by the aggregated results from Thunersee and Brienzersee. The first six columns are the municipalities from where the samples were taken. This standard is maintained throughout the document. The number represents the median survey value for that object. If that object is not found in at least half of the surveys then the median value will be zero. The median value is a reasonable estimate of the number of objects likely to be found if a litter survey were repeated_. 

The results for plastic construction waste indicate that it was more prevalent in Bönigen (4.5p/100m) and Unterseen (1.5p/100m) versus the other municipalities where the median value is zero. However Industrial sheeting and cigarettes were identified at all municipalities in at least 1/2 the surveys. 

In practical terms there was a better chance of finding plastic construction waste on the beach in Bönigen and Unterseen than the other municipalities. However, the chances of finding industrial sheeting were approximately equal anywhere but the most might be found at at Brienze (67p/100m). 

The [key indicators](keyindicators) chapter gives a precise definition of each of the basic statistics that can be derived from the survey results and how they are used for identifying zones of accumulation and significant events. The methods used to calculate the different environmental variables are explained in [_The land use profile_](luseprofile). The codes and descriptions used to identify the items as well as the different economic groupings are covered in detail in [_Code groups_](codegroups). How samples are collected and the methods for identifying extreme values and calculating baselines for a region can be found in [_Beach litter baselines_](threshhold).

The results for each municipality are included with the lake or river to which they belong. A more detailed report can be produced for any municipality in this document. 

### Contributing to this report

This report is versioned therefore it is very easy to submit articles or analysis that correct, clarify or improve the content. The easiest way to contribute is to send a pull request to [end of sampling repo](https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021). Submissions are accepted in all official Swiss national languages.

<br />

(italiano_intro)=
# Prefazione

Il presente progetto mira a raccogliere dati e a sviluppare l’infrastruttura necessaria per valutare accuratamente la composizione e l’abbondanza di materiale antropogenico lungo fiumi e laghi svizzeri selezionati nonché a presentare questi risultati in un rapporto consolidato basato su web.  

I risultati di queste indagini saranno utilizzati per esplorare altri metodi per rilevare le zone di accumulo.

__Rilevamento dell'accumulo e della perdita con il Rho di Spearman__, *collaborazione con Louise Schreyers, [Wageningen University and Research](https://www.wur.nl/).* [Repository](https://github.com/hammerdirt-analyst/landuse)

__La probabilità di trovare un oggetto__, *collaborazione con Romain Tramoy, Laboratoire Eau Environment et Systèmes Urbains [LEESU](https://www.leesu.fr/), Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Montserrat Filella, [_Department F.-A. Forel, University of Geneva_](https://www.unige.ch/forel/fr/).* [Repository](https://github.com/hammerdirt-analyst/finding-one-object)

__Monitoraggio dei rifiuti con la prossima generazione di ingegneri ambientali 2016-2021__, *collaborazione con Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Christian Ludwig, [_Paul Scherer Institute_](https://www.psi.ch/en)/[_EPFL_](https://www.epfl.ch/en/).* [Repository](https://github.com/hammerdirt-analyst/swe)

## Metodo di valutazione

Nel 2008 è stata pubblicata la prima guida internazionale per il monitoraggio del beach litter dal Programma delle Nazioni Unite per l’ambiente (UNEP) e dalla Commissione oceanografica intergovernativa (COI) {cite}`unepseas`. Questo metodo è stato riprodotto dalla Commissione OSPAR nel 2010 {cite}`ospard10`.  Nel 2013 l’UE ha pubblicato una guida sul monitoraggio dei rifiuti marini nei mari europei (La guida) {cite}`mlwguidance`.     . La Svizzera è membro di OSPAR e ha più di 1.400 campioni che utilizzano i metodi descritti in tale guida. 

*Con un’indagine di beach litter si conta il materiale antropogenico visibile identificato all’interno di un’area delimitata che confina su un lato con un lago, un fiume o un oceano.*

* Le posizioni sono definite dai loro punti GPS. 
* La lunghezza e la larghezza sono misurate per ogni area d’indagine. 
* Le sostanze inquinanti visibili all'interno dell’area d’indagine vengono raccolte, classificate, contate e pesate. 
* Tutti gli articoli sono classificati in base alle definizioni dei codici inclusi nella guida. 

Per identificare oggetti di interesse regionale sono stati aggiunti codici supplementari. Per esempio, sono stati sviluppati codici per oggetti come contenitori di esche a feromoni e bastoncini da sci per rendere conto della presenza di questi oggetti quando identificati in determinate regioni. Identificare e quantificare gli oggetti permette ai ricercatori e alle parti interessate di determinare le probabili fonti e definire strategie di riduzione mirate a oggetti specifici.  

Per maggiori informazioni: [Gruppi di codici - english](codegroups).


## Metrica di valutazione 

Il valore mediano (50ºpercentile) dei risultati dell’indagine viene riportato come numero di oggetti per 100 m (p/100 m) di costa. Questo è il metodo descritto in EU Marine Beach Litter Baselines (Linee guida sui rifiuti ritrovati sulle spiagge marine) {cite}`eubaselines` ed è lo standard usato in questo rapporto. Lo standard di 100 metri di costa usato nell’ambiente marino è appropriato per le regioni costiere del continente europeo. Tuttavia, l’urbanizzazione e la topografia presentano sfide particolari se si tratta di selezionare luoghi adatti a condurre in modo sicuro indagini annuali sui rifiuti costieri. 

Limitare le indagini a 100 metri di costa esposta avrebbe ridotto drasticamente il numero di luoghi d’indagine disponibili e l’uso di dati preesistenti. Pertanto, l’IQAASL riflette la topografia locale con una lunghezza mediana di sondaggio di 45 m e una media di 51 m. I sondaggi inferiori a 10 m non sono stati considerati nell’analisi di base. I risultati dei sondaggi vengono convertiti in p/100 m moltiplicando il risultato del sondaggio per 100. 


### Raccolta di dati

Un’indagine sul beach litter può essere condotta da chiunque in qualsiasi momento. Se l’indagine viene condotta secondo il metodo descritto nella guida {cite}`mlwguidance` o nel [Beach litter baselines](threshhold) il risultato può essere confrontato direttamente con i grafici di questo rapporto. Non è necessario inserire i dati nel sistema per confrontare i risultati.  

__La raccolta di dati__ per il rapporto (o il prossimo rapporto) richiede un po’ di addestramento e una valutazione. Di solito sono necessari 3-5 rilevamenti per comprendere adeguatamente il compito. La maggior parte del tempo viene spesa per identificare gli oggetti e l’importanza di mantenere un taccuino da campo. Il vantaggio di contribuire ai dati è che la procedura di reporting è automatizzata e si ha sempre accesso ai risultati.  

##  Usare questo rapporto 

È importante capire la differenza tra la _mediana_ {cite}`mediandef` e la _media_ {cite}`meandeff` quando si interpretano i risultati. Tranne che per i risultati mensili, i risultati dell’indagine sono dati come la mediana p/100 m per la località in questione. 

Come esempio, prendiamo in considerazione il risultato __mediano__ del sondaggio per gli oggetti più comuni ritrovati sul Lago di Thun e sul Lago di Brienz. 


```{figure} resources/images/intro/thunersee_brienzersee_it.png
---
width: 600px
name: mcommonforeword_it
---s

` `

```

{numref}`Figura {number}: <mcommonforeword_it>` _Interpretazione dei risultati dell’indagine. I risultati aggregati di tutte le aree d’indagine sono nella colonna all’estrema destra, preceduti dai risultati aggregati del Lago di Thun e del Lago di Brienz. Le prime sei colonne sono i comuni da cui sono stati prelevati i campioni. Questo standard è mantenuto in tutto il documento. Il numero rappresenta il valore mediano del sondaggio per quell’oggetto. Se quell’oggetto non viene trovato in almeno la metà delle indagini, allora il valore mediano sarà zero. Il valore mediano è una stima ragionevole del numero di oggetti che probabilmente verrebbero trovati se si ripetesse un’indagine sui rifiuti_.

I risultati per i rifiuti edili in plastica mostrano che erano più diffusi a Bönigen (4,5 p/100 m) e Unterseen (1,5 p/100 m) rispetto agli altri comuni dove il valore mediano è zero. Tuttavia lamiere industriali e sigarette sono state identificate in tutti i comuni in almeno 1/2 delle indagini.  

In termini pratici c’erano più possibilità di trovare rifiuti edili in plastica sulla spiaggia a Bönigen e Unterseen che negli altri comuni. Tuttavia le possibilità di trovare teli industriali erano all’incirca uguali ovunque ma il massimo si poteva trovare a Brienz (67 p/100 m). 

Il capitolo degli [Indicatori chiave - english ](keyindicators) dà una definizione precisa di ciascuna delle statistiche di base che si possono ricavare dai risultati dell’indagine e come vengono usate per identificare zone di accumulo ed eventi significativi. I metodi usati per calcolare le diverse variabili ambientali sono spiegati in [Il profilo dell’uso del suolo - english](luseprofile). I codici e le descrizioni usati per identificare gli elementi e i diversi raggruppamenti economici sono trattati in dettaglio in [Gruppi di codici - english](codegroups). Come si raccolgono i campioni e i metodi per identificare i valori estremi e calcolare le linee di base per una regione si trovano in [_Beach litter baselines_](threshhold).

I risultati per ogni comune indicano il lago o il fiume a cui appartengono. Si può produrre un rapporto più dettagliato per ogni comune in questo documento.  

### Contribuire a questo rapporto 

Questo rapporto indica la versione quindi è molto facile inviare articoli o analisi che correggono, chiariscono o migliorano il contenuto. Per contribuire, basta inviare una richiesta di pull a [fine repo di campionamento](https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021). Si accettano richieste redatte in tutte le lingue nazionali ufficiali svizzere.

(francais_intro)=
# Avant-propos

L'objectif de ce projet était de collecter des données et de développer l'infrastructure nécessaire pour évaluer avec précision la composition et l'abondance des matières anthropogènes le long de certains lacs et rivières suisses et de présenter ces résultats dans un rapport consolidé basé sur le Web. 

Les résultats de ces inventaires sont utilisés pour explorer d'autres méthodes de détection des zones d'accumulation.

__Détection de l'accumulation et des fuites avec Spearman's Rho__, *collaboration avec Louise Schreyers, [Wageningen University and Research](https://www.wur.nl/).* [Repository](https://github.com/hammerdirt-analyst/landuse)

__La probabilité de trouver un objet__, *collaboration avec Romain Tramoy, Laboratoire Eau Environment et Systèmes Urbains [LEESU](https://www.leesu.fr/), Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Montserrat Filella, [_Department F.-A. Forel, University of Geneva_](https://www.unige.ch/forel/fr/).* [Repository](https://github.com/hammerdirt-analyst/finding-one-object)

__Surveillance des déchets avec la prochaine génération d'ingénieurs écologues 2016-2021__, *collaboration avec Bhavish Patel, [_Paul Scherrer Institute_](https://www.psi.ch/en), Christian Ludwig, [_Paul Scherer Institute_](https://www.psi.ch/en)/[_EPFL_](https://www.epfl.ch/en/).* [Repository](https://github.com/hammerdirt-analyst/swe)


## Méthode d'évaluation

En 2008, le premier guide international de surveillance des déchets de plage a été publié par le Programme des Nations Unies pour l'environnement (PNUE) et la Commission océanographique intergouvernementale (COI) {cite}`unepseas`. Cette méthode a été reproduite par la Commission OSPAR en 2010 {cite}`ospard10`. En 2013, l'UE a publié un guide sur la surveillance des déchets marins dans les mers européennes (le guide) {cite}`mlwguidance`. La Suisse est membre d'OSPAR et dispose de plus de 1 400 inventaires utilisant les méthodes décrites dans Le guide. 

*Un __inventaire de déchets__ de plage consiste à comptabiliser les matériaux anthropogènes visibles identifiés dans une zone délimitée qui est bordée d'un côté par un lac, une rivière ou un océan. *

* Les emplacements sont définis par leurs points GPS 
* La longueur et la largeur sont mesurées pour chaque inventaire 
* Les polluants visibles dans la zone d'étude sont collectés, classés, comptés et pesés. 
* Tous les articles sont classés en fonction des définitions de code incluses dans Le guide.  

Afin d'identifier les objets d'intérêt régional, des codes supplémentaires ont été ajoutés. Par exemple, des codes ont été développés pour des objets tels que les conteneurs d'appâts à phéromones et les bâtons de ski afin de tenir compte de l'occurrence de ces objets lorsqu'ils sont identifiés dans certaines régions. L'identification et la quantification des objets permettent aux chercheurs et aux parties prenantes de déterminer les sources probables et de définir des stratégies de réduction ciblant des objets spécifiques.   

Pour plus d'informations: [Groupes de codes - english](codegroups).

## Mesure d'évaluation 

La valeur médiane ( 50e percentile) des résultats des inventaires est rapportée comme le nombre d'objets par 100m (p/100m) de rivage. C'est la méthode décrite dans le document EU Marine Beach Litter Baselines [HG19] et c'est la norme utilisée dans ce rapport. La norme de 100 mètres de rivage utilisée dans le milieu marin est appropriée pour les régions côtières du continent européen. Cependant, l'urbanisation et la topographie présentent des défis uniques lors de la sélection de lieux adaptés. La sécurité et l'accès tout au long de l'année doivent être pris en considération.  

La valeur médiane ( 50e percentile) des résultats des inventaires est rapportée comme le nombre d'objets par 100m (p/100m) de rivage. C'est la méthode décrite dans le document EU Marine Beach Litter Baselines [HG19] et c'est la norme utilisée dans ce rapport. La norme de 100 mètres de rivage utilisée dans le milieu marin est appropriée pour les régions côtières du continent européen. Cependant, l'urbanisation et la topographie présentent des défis uniques lors de la sélection de lieux adaptés. La sécurité et l'accès tout au long de l'année doivent être pris en considération.  

### Collecte des données

Un inventaire de déchets de plage peut être menée par n'importe qui, à tout moment. Si l'inventaire est menée selon la méthode décrite dans le Guide {cite}`mlwguidance`  ou les [Beach litter baselines - english](threshhold) le résultat peut être comparé directement aux graphiques de ce rapport. Il n'est pas nécessaire de saisir les données dans le système pour comparer les résultats.   

La collecte de données pour le rapport (ou le rapport suivant) nécessite une certaine formation sur le tas et une évaluation. Il faut généralement 3 à 5 enquêtes pour acclimater une personne à la tâche. La majeure partie du temps est consacrée à l'identification des objets et à l'importance de tenir un carnet de terrain. L'avantage de contribuer aux données est que la procédure de rapport est automatisée et qu'il est toujours possible d'accéder aux résultats. 

##  Utilisation de ce rapport 

Il est important de comprendre la différence entre la médiane {cite}`mediandef` et la moyenne {cite}`meandeff` lors de l'interprétation des résultats. À l'exception des résultats mensuels, les résultats des inventaires sont donnés comme la médiane p/100m pour l'emplacement en question.  

À titre d'exemple, considérons le résultat médian des inventaires pour les objets les plus courants sur Thunersee et le Brienzersee.  


```{figure} resources/images/intro/thunersee_brienzersee_fr.png
---
width: 600px
name: mcommonforeword_fr
---

` `

```

{numref}`Figura {number}: <mcommonforeword_fr>` _Interprétation des résultats de l' inventaire. Les résultats agrégés de toutes les zones d'enquêtes figurent dans la colonne d'extrême droite, précédés des résultats agrégés de Thunersee et Brienzersee. Les six premières colonnes correspondent aux municipalités où les échantillons ont été prélevés. Cette norme est maintenue tout au long du document. Le chiffre représente la valeur médiane de l' inventaire pour cet objet. Si cet objet n'est pas trouvé dans au moins la moitié des inventaires, la valeur médiane sera de zéro. La valeur médiane est une estimation raisonnable du nombre d'objets susceptibles d'être trouvés si un inventaire de déchets sauvages était répétée._

Les résultats pour les déchets de construction en plastique indiquent qu'ils étaient plus répandus à Bönigen (4,5p/100m) et Unterseen (1,5p/100m) par rapport aux autres municipalités où la valeur médiane est de zéro. Cependant, la bâche industrielle et les cigarettes ont été identifiées dans toutes les municipalités dans au moins la moitié des inventaires.  

Concrètement, il y avait plus de chances de trouver des déchets de construction en plastique sur la plage à Bönigen et Unterseen que dans les autres communes. En revanche, les chances de trouver des bâches industrielles étaient à peu près égales partout, mais c'est à Brienze que l'on pouvait en trouver le plus (67p/100m). 

Le chapitre sur les [indicateurs clés - english ](keyindicators) donne une définition précise de chacune des statistiques de base qui peuvent être dérivées des résultats de l' inventaire et de la manière dont elles sont utilisées pour identifier les zones d'accumulation et les événements significatifs. Les méthodes utilisées pour calculer les différentes variables environnementales sont expliquées dans [Le profil d'utilisation des sols - english](luseprofile). Les codes et les descriptions utilisés pour identifier les éléments ainsi que les différents groupements économiques sont traités en détail dans [Groupes de codes - english](codegroups). La manière dont les échantillons sont collectés et les méthodes d'identification des valeurs extrêmes et de calcul des lignes de base pour une région se trouvent dans [_valeurs de reference - english_](threshhold).

Les résultats de chaque municipalité sont inclus avec le lac ou la rivière à laquelle ils appartiennent. Un rapport plus détaillé peut être produit pour n'importe quelle municipalité dans ce document.    

### Contribuer à ce rapport 

Ce rapport est versionné, il est donc très facile de soumettre des articles ou des analyses qui corrigent, clarifient ou améliorent le contenu. Pour contribuer, envoyez une demande de retrait à [repo de fin d'échantillonnage](https://github.com/hammerdirt-analyst/IQAASL-End-0f-Sampling-2021).     Les soumissions sont acceptées dans toutes les langues nationales officielles de la Suisse. 