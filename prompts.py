"""
prompts.py
-------------
This module contains the prompts and labels commonly used for reporting. The prompts were designed for the proof of concept
available in app.py.
"""

language_column_map = {"English": "en", "French": "fr", "German": "de"}

iqaasl = "https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/"
bafu_theme = "https://www.bafu.admin.ch/bafu/en/home/topics/waste/dossiers/waste-along-swiss-rivers-and-lakes.html"

land_use_rates_description = (
    "\nThe sampling stratification and trash density table quantifies the change in trash density based on the proportion of the buffer " 
    "zone that is dedicated to a particular land use feature. Each survey location is surrounded by a buffer zone of radius = 1 500 meters. "
    "The buffer zone is comprised of land-use features, each land use feature occupies a proportion of the buffer zone (0 - 100%). "
    "The sampling stratification and trash density table quantifies the change in trash density based on the proportion of the "
    "buffer zone that is dedicated to a particular land use feature.\n"
)
land_use_description = (
    "\nEach survey location is surrounded by a buffer zone of radius = 1 500 meters. "
    "The buffer zone is comprised of land-use features, each land use feature occupies a proportion of the buffer zone (0 - 100%). "
    "The land-use-profile is measured by considering the dry land proportion of the buffer dedicated to each of land use feature that is present in the buffer zone. "
    "Each location has the same size buffer zone. For lakeside locations the surface area of the water feature is substracted from the buffer surface area. "
    "What changes is how the land use features are distributed within the buffer zone. We assume that locations that have a similar distribution of features in "
    "the buffer zone should have similar survey results. The sampling stratification tells us under what conditions the surveys were collected and "
    "what proportions of the samples were taken according to those conditions.\n"
)

def abstract_prompt(language, feature_type, objects, cantons):
    """Prompt for the abstract generation task."""

    if feature_type == "lake":
        lakes_or_rivers = "lakes"
    elif feature_type == "river":
        lakes_or_rivers = "rivers"
    else:
        lakes_or_rivers = "lakes and rivers"

    aprompt = (
        f"You are a data scientist. You are writing the description of the data from a scatterplot. The data is  from"
        f" observations of {objects} found along {lakes_or_rivers} in {', '.join(cantons)}. The data has been selected by the client."
        " These observations are given in pieces per meter per sample. A sample is defined by a location and a date",
        ". Your task is to write an informative abstract about the user provided report. Each report has the following"
        " sections:\n\nTitle, subtitle, summary",
        "statistics, administrative boundaries,",
        " the named features, and the material composition. After these sections the aggregated survey data is grouped",
        " for different regions and features. Each report is concluded with an inventory of each of the objects selected",
        " by the client.\n\nYour abstract must include information about the cities cantons or",
        " features included in the report. It must also include the names of the objects (look in the inventory) which"
        " are the subject of the report.",
        " The fail rate is the rate at which we expect to find at least one of the objects at a survey.",
        " From the summary statistics include The total number (quantity) of objects, the number of samples",
        " (summary statistics) and start and end date of samples should also be mentioned.",
        " The objects in the report are selected by the client. The report is about those objects and nothing more.",
        " You must answer in paragraph form, limit your response to two paragraphs.\n\nThis is an abstract for a",
        " professional document. We do not need any general closing comments.",
        f" only concerns the contents of the report.\n\nPlease reply in the following language: {language}."
    )
    return ''.join(aprompt)

def scatterplot_prompt(start, end, interval, group_mean, objects, color, feature_type, cantons, language):
    """
    Generates a scatter plot prompt based on the provided parameters.
    """
    if feature_type == "lake":
        lakes_or_rivers = "lakes"
    elif feature_type == "river":
        lakes_or_rivers = "rivers"
    else:
        lakes_or_rivers = "lakes and rivers"



    prompt = (
        f"You are a data scientist. You are writing the description of the data from a scatterplot. The data is  from"
        f" observations of {objects} found along {lakes_or_rivers} in {', '.join(cantons)}. The data has been selected by the client."
        " These observations are given in pieces of trash per meter per sample. A sample is defined by a location and a date",
        ". Your task is to summarize the data in the plot AND identify any important features in the data.",
        " The plot characteristics are as follows::\n\n1. x axis: date of the sample\n2. y axis: pieces per meter, the sum of all",
        f" the objects found divided by the length of the shoreline that was surveyed.\n3. groups: {color} the regional aggregation",
        f" of the surveys.\n4. x axis start date {start}, x axis end date {end}\n5. y axis 90% interval: {interval}\n\n",
        f"The results by groups are as follows: {group_mean}\n\n.",
        "Your summary must be brief and to the point. The client has an image of the plot and your summary is to help them understand.",
        " Your audience is professional and they know how to read a scatterplot. Your summary should be about the data."
        " You must answer in paragraph form in a concise and factual manner. Limit your response to two paragraphs. No titles or labels are wanted.\n\n",
        f"No general statements or closing comments are requested. Your answer must be in the following language: {language}."
    )

    return ''.join(prompt)

def barchart_prompt(data, grouped_data, x_axis, y_axis, language):
    """Creates a prompt for a barchart given the data and the x and y axis labels"""

    # grouped_data = handle_grouped_data_for_barchart(data, x_axis, y_axis)
    feature_type = data['feature_type'].unique()
    if len(feature_type) > 1:
        lakes_or_rivers = "lakes and rivers"
    elif feature_type[0] == 'l':
        lakes_or_rivers = "lakes"
    else:
        lakes_or_rivers = "rivers"
    c_selected = data['canton'].unique()
    description_column = language_column_map[language]
    objects = data[description_column].unique()
    prompt = (
        f"You are a data scientist. You are writing the description of the data from a bar plot. The data is  from"
        f" observations of {', '.join(objects)} found along {lakes_or_rivers} in {', '.join(c_selected)}. The data has been selected by the client."
        f"Your task is to summarize the data in the bar chart AND identify any important features in the data.",
        f"The barchart characteristics are as follows::\n\n1. x axis: {x_axis} this is one of the following: canton,"
        " city, feautre_name, object. canton and city refer to locations in switzerland. feature_name refers to specific lakes or rivers.\n"
        f"2. yaxis : {y_axis} this is one of the following quantity, pcs/m, number of samples. Quantity refers to the"
        " number of objects found by x-axis category. pcs/m refers to the average number of objects observed per meter of shoreline."
        " number of samples refers to the number of times that samples were taken per xaxis category. Or you could say number of trips to the beach\n\n"
        f" the data used to create the chart is below:\n\n{grouped_data.to_markdown()}\n\n",
        "Identify the min and max values in the charts. Identify or define the x labels provide details."
        " The client has an image of the plot and your summary is to help them understand.",
        " Your audience is professional and they know how to read a barplot. Your summary should be about the data. Further analysis"
        " is not needed. You must answer in paragraph form in a concise and factual manner.\n\n",
        f"Your answer must be in the following language: {language}."
    )

    return ''.join(prompt)

def reporter_prompt(summary, scatterplot, barchart, inventory, rough_draft):
    aprompt = (
                "You are helping a data scientist write a summary report of volunteer observations of objects found along",
                " lakes and rivers in Switzerland. The data is collected using the JRC/EU method counting beach litter. This",
                " method is defined in the _Guide for monitoring marine litter in european seas_. Your other reference document",
                " is the federal report on litter density of swiss lakes (IQAASL) published in 2021 and available here:\n\n",
                "[IQAASL End of Sampling 2021](https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/)\n\n",
                "The client has already prepared a rough draft of the report as well as a bar chart, scatter plot and map.",
                " Your task is to answer the clients questions reference these reports. The client is preparing a decision",
                " support document and is relying on you for brief answers that can be supported by the documents provided",
                " below or the previously mentioned references. The client has provided the following documents:\n\n",
                f"summary: {summary}\n\n",
                f"scatterplot: {scatterplot}\n\n",
                f"barchart: {barchart}\n\n",
                f"inventory: {inventory}\n\n",
                f"rough draft: {rough_draft}\n\n",
                "!Instructions!\n\n"
                "The column names and descriptions for inventory items:\n1. object: the use or plain language description"
                "\n2. code: the MLW code for the item\n3. quantity: the total number of items found\n4. pcs/m: the average number"
                " of items per meter of shoreline.\n5 % of total: the proportion of the current set of data.\n6. number of samples:"
                " the number of samples collected\n7. fail rate: the proportion of samples that contained at least one of the objects, the chance of finding at least on of the objects at a survey\n\n",
                "You are to discuss plastics, trash or litter in the environment, citizen-science, swiss or european policy",
                " concerning plastics and trash in the environment, probability and statistics, calculus, bayes theorem, bayesian statistics",
                " other topics of a sensitive or sexual nature are not to be considered.",
            )
    return ''.join(aprompt)

# labels
report_assistant_text = {
    "English": (
        "### The Report Assistant\n\n"
        f"The report assistant is a supplement to the 2022 Swiss Federal Report on Trash Density along lakes and rivers: [IQAASL End of Sampling 2021]({iqaasl}). "
        f"It is also an accompaniment to the FOEN theme: [waste along lakes and rivers]({bafu_theme}). "
        "The assistant helps stakeholders generate customized reports quickly. "
        "Reports can be tailored to specific needs, whether for a municipality, lake, or canton.\n\n"
        "By leveraging large language models (LLMs), it enables interactive data exploration. "
        "Stakeholders can explore, filter, and analyze data interactively. "
        "They can ask questions and receive clear, contextual explanations of the output. "
        "This empowers stakeholders to make informed decisions based on observed conditions."
    ),
    "French": (
        "### L'Assistant de Rapport\n\n"
        "L'assistant de rapport est un complément au Rapport fédéral suisse 2022 sur la densité des déchets le long des lacs et des rivières : [IQAASL Fin de l'échantillonnage 2021]({iqaasl}). "
        "Il est également un accompagnement au thème de l'OFEV [les déchets le long des lacs et des rivières]({bafu_theme}). "
        "L'assistant aide les parties prenantes à générer rapidement des rapports personnalisés. "
        "Les rapports peuvent être adaptés à des besoins spécifiques, qu'il s'agisse d'une municipalité, d'un lac ou d'un canton.\n\n"
        "En exploitant des modèles de langage avancés (LLMs), il permet une exploration interactive des données. "
        "Les parties prenantes peuvent explorer, filtrer et analyser les données de manière interactive. "
        "Elles peuvent poser des questions et recevoir des explications contextuelles claires sur les résultats. "
        "Cela permet aux parties prenantes de prendre des décisions éclairées basées sur les conditions observées."
    ),
    "German": (
        "### Der Berichtsassistent\n\n"
        "Der Berichtsassistent ist eine Ergänzung zum Schweizerischen Bundesbericht 2022 über die Abfalldichte entlang von Seen und Flüssen: [IQAASL End of Sampling 2021]({iqaasl}). "
        "Er ist auch eine Begleitung zum BAFU-Thema [Abfälle entlang von Seen und Flüssen]({bafu_theme}). "
        "Der Assistent hilft Stakeholdern, schnell maßgeschneiderte Berichte zu erstellen. "
        "Berichte können auf spezifische Bedürfnisse zugeschnitten werden, sei es für eine Gemeinde, einen See oder einen Kanton.\n\n"
        "Durch den Einsatz großer Sprachmodelle (LLMs) ermöglicht er eine interaktive Datenexploration. "
        "Stakeholder können Daten interaktiv erkunden, filtern und analysieren. "
        "Sie können Fragen stellen und klare, kontextbezogene Erklärungen zu den Ergebnissen erhalten. "
        "Dies ermöglicht es Stakeholdern, fundierte Entscheidungen auf der Grundlage beobachteter Bedingungen zu treffen."
    )
}

data_info_text = {
    "English": (
        "**Where does the data come from?** The data was collected by volunteers and experts from NGOs all over Switzerland.\n\n"
        "Collecting data is simple, go to the beach, walk along the water and count and identify the man-made objects you find.\n\n"
        "**Based on field experience**, this app is built on methodologies and insights from the following works:\n\n"
        "- [IQAASL End of Sampling 2021](https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/)\n"
        "- [Solid Waste Team](https://hammerdirt-analyst.github.io/solid-waste-team/titlepage.html)\n"
        "- [Land Use](https://hammerdirt-analyst.github.io/landuse/titlepage.html)\n"
        "- [Plastock](https://associationsauvegardeleman.github.io/plastock/)\n"
        "- [Finding One Object](https://hammerdirt-analyst.github.io/finding-one-object/titlepage.html)\n\n"
        "**Open Source and Transparent**\n\n"
        "The app's source code, data, and documentation are available for review and collaboration:\n"
        "[Explore the documentation and source code here](https://hammerdirt-analyst.github.io/feb_2024/titlepage.html#).\n\n"
    ),
    "French": (
        "**D'où viennent les données?** Les données ont été collectées par des bénévoles et des experts d'ONG partout en Suisse.\n\n"
        "Collecter des données est simple, rendez-vous sur une plage, marchez le long de l'eau et comptez et identifiez les objets fabriqués par l'homme que vous trouvez.\n\n"
        "**Basé sur l'expérience de terrain**, cette application est basée sur des méthodologies et des idées issues des travaux suivants:\n\n"
        "- [IQAASL End of Sampling 2021](https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/)\n"
        "- [Solid Waste Team](https://hammerdirt-analyst.github.io/solid-waste-team/titlepage.html)\n"
        "- [Land Use](https://hammerdirt-analyst.github.io/landuse/titlepage.html)\n"
        "- [Plastock](https://associationsauvegardeleman.github.io/plastock/)\n"
        "- [Finding One Object](https://hammerdirt-analyst.github.io/finding-one-object/titlepage.html)\n\n"
        "**Source ouverte et transparente**\n\n"
        "Le code source, les données et la documentation de l'application sont disponibles pour examen et collaboration:\n"
        "[Explorez la documentation et le code source ici](https://hammerdirt-analyst.github.io/feb_2024/titlepage.html#).\n\n"
    ),
    "German": (
        "**Woher stammen die Daten?** Die Daten wurden von Freiwilligen und Experten von NGOs aus der ganzen Schweiz gesammelt.\n\n"
        "Das Sammeln von Daten ist einfach: Gehen Sie an den Strand, laufen Sie am Wasser entlang und zählen und identifizieren Sie die von Menschen hergestellten Objekte, die Sie finden.\n\n"
        "**Basierend auf Felderfahrungen**, diese App basiert auf Methoden und Erkenntnissen aus den folgenden Arbeiten:\n\n"
        "- [IQAASL End of Sampling 2021](https://hammerdirt-analyst.github.io/IQAASL-End-0f-Sampling-2021/)\n"
        "- [Solid Waste Team](https://hammerdirt-analyst.github.io/solid-waste-team/titlepage.html)\n"
        "- [Land Use](https://hammerdirt-analyst.github.io/landuse/titlepage.html)\n"
        "- [Plastock](https://associationsauvegardeleman.github.io/plastock/)\n"
        "- [Finding One Object](https://hammerdirt-analyst.github.io/finding-one-object/titlepage.html)\n\n"
        "**Offen und Transparent**\n\n"
        "Der Quellcode, die Daten und die Dokumentation der App sind zur Überprüfung und Zusammenarbeit verfügbar:\n"
        "[Entdecken Sie die Dokumentation und den Quellcode hier](https://hammerdirt-analyst.github.io/feb_2024/titlepage.html#).\n\n"
    )
}

intro_one = {
    "English": """
    This is an application of large language models (LLMs) and machine learning to provide summary reports of volunteer observations of marine litter using the OSPAR, JRC, or NOAA methods for counting beach litter.
    """,
    "French": """
    Ceci est une application de modèles de langage avancés (LLMs) et d'apprentissage automatique pour fournir des rapports résumés des observations bénévoles des déchets marins en utilisant les méthodes OSPAR, JRC ou NOAA pour le comptage des déchets sur les plages.
    """,
    "German": """
    Dies ist eine Anwendung großer Sprachmodelle (LLMs) und maschinellen Lernens, um zusammenfassende Berichte über die Beobachtungen von Freiwilligen zu Meeresmüll zu erstellen, basierend auf den OSPAR-, JRC- oder NOAA-Methoden zur Erfassung von Strandmüll.
    """
}
intro_two = {
    "English": """
    The inspiration for this is the millions of people each year throughout the world who spend the time to collect the data.
    """,
    "French": """
    L'inspiration pour cela vient des millions de personnes à travers le monde qui, chaque année, prennent le temps de collecter les données.
    """,
    "German": """
    Die Inspiration dafür sind die Millionen von Menschen weltweit, die jedes Jahr Zeit investieren, um die Daten zu sammeln.
    """}

English_instructions = (
    "Make a summary of data and select chart contents.\n\n"
    "1. Select a canton, city, lake or river.\n"
    "2. Select your date range.\n"
    "3. Select the objects of interest.\n"
    "4. Apply filters.\n"
    "5. Make rough drafts.\n"
    "6. Define chart contents and create summary of chart.\n"
    "7. Chat with data.\n\n"
)

French_instructions = (
    "Faites un résumé des données et sélectionnez le contenu du graphique.\n\n"
    "1. Sélectionnez un canton, une ville, un lac ou une rivière.\n"
    "2. Sélectionnez votre plage de dates.\n"
    "3. Sélectionnez les objets d'intérêt.\n"
    "4. Appliquez des filtres.\n"
    "5. Faites des brouillons.\n"
    "6. Définissez le contenu du graphique et créez un résumé du graphique.\n"
    "7. Discutez avec les données.\n\n"
)

German_instructions = (
    "Erstellen Sie eine Datenzusammenfassung und wählen Sie die Diagramminhalte aus.\n\n"
    "1. Wählen Sie einen Kanton, eine Stadt, einen See oder einen Fluss aus.\n"
    "2. Wählen Sie Ihren Datumsbereich aus.\n"
    "3. Wählen Sie die interessierenden Objekte aus.\n"
    "4. Wenden Sie Filter an.\n"
    "5. Erstellen Sie grobe Entwürfe.\n"
    "6. Definieren Sie die Diagramminhalte und erstellen Sie eine Zusammenfassung des Diagramms.\n"
    "7. Chatten Sie mit den Daten.\n\n"
)



engish_filtertwo = ('Confirm your selections before making a rough draft.\n'
                    'You can adjust your selections by clicking the "clear filters" button below.\n'
                    'if you selected no objects the report will be for all objects found in the selected region and date range.\n'
                    'in this case the list of selected codes will not appear in the display below.'
                    )
french_filtertwo = ('Confirmez vos sélections avant de rédiger un brouillon.\n'
                    'Vous pouvez ajuster vos sélections en cliquant sur le bouton "effacer les filtres" ci-dessous.\n'
                    'Si vous n\'avez sélectionné aucun objet, le rapport portera sur tous les objets trouvés dans la région et la plage de dates sélectionnées.\n'
                    'dans ce cas, la liste des codes sélectionnés n\'apparaîtra pas dans l\'affichage ci-dessous.'
                    )
german_filtertwo = ('Bestätigen Sie Ihre Auswahl, bevor Sie einen Entwurf erstellen.\n'
                    'Sie können Ihre Auswahl anpassen, indem Sie unten auf die Schaltfläche "Filter löschen" klicken.\n'
                    'Wenn Sie keine Objekte ausgewählt haben, bezieht sich der Bericht auf alle in der ausgewählten Region und im ausgewählten Datumsbereich gefundenen Objekte.\n'
                    'In diesem Fall wird die Liste der ausgewählten Codes nicht im folgenden Display angezeigt.'
                    )

french_filterone = 'Appliquez les filtres de localisation, puis vous pouvez sélectionner un ou plusieurs objets. Si vous ne sélectionnez aucun objet, le rapport inclura tous les objets trouvés dans la plage de dates et les filtres géographiques.'
german_filterone = 'Wenden Sie die Standortfilter an, dann können Sie ein oder mehrere Objekte auswählen. Wenn Sie keine Objekte auswählen, enthält der Bericht alle Objekte, die im Datumsbereich und innerhalb der geografischen Filter gefunden wurden.'
english_filterone = 'Apply the location filters, then you can select one object or multiple objects. If you select none of the objects, the report will include all objects found within the date range and geographic filters.'

labels = {
    "language": {
        "English": "Language",
        "French": "Langue",
        "German": "Sprache"
    },
    "filtering_data": {
        "English": "Filtering Data",
        "French": "Filtrage des données",
        "German": "Daten filtern"
    },
    "date_range": {
        "English": "Date Range",
        "French": "Plage de dates",
        "German": "Datumsbereich"
    },
    "canton": {
        "English": "Canton",
        "French": "Canton",
        "German": "Kanton"
    },
    "city": {
        "English": "City",
        "French": "Ville",
        "German": "Stadt"
    },
    "feature_type": {
        "English": "Feature Type",
        "French": "Type de caractéristique",
        "German": "Merkmaltyp"
    },
    "clear_filters": {
        "English": "Clear Filters",
        "French": "Effacer les filtres",
        "German": "Filter löschen"
    },
    "apply_filters": {
        "English": "Apply location filters",
        "French": "Appliquer les filtres de localisation",
        "German": "Standortfilter anwenden"
    },
    "objects": {
        "English": "Objects of Interest",
        "French": "Objets d'intérêt",
        "German": "Interessante Objekte"
    },
    "feature_name": {
        "English": "Feature Name",
        "French": "Nom du lac/rivière",
        "German": "Merkmalsname"
    },
    "step_1": {
        "English": "Step 1",
        "French": "Étape 1",
        "German": "Schritt 1"
    },
    "step_2": {
        "English": "Step 2",
        "French": "Étape 2",
        "German": "Schritt 2"
    },
    "step_3": {
        "English": "Step 3",
        "French": "Étape 3",
        "German": "Schritt 3"
    },
    "selected_parameters": {
        "English": "Selected Parameters",
        "French": "Paramètres sélectionnés",
        "German": "Ausgewählte Parameter"
    },
    "whats_this":{
        "English": "Some background information",
        "French": "Quelques informations générales",
        "German": "Einige Hintergrundinformationen"
    },
    "parameter_selection": {
        "English": "Parameter Selection",
        "French": "Sélection des paramètres",
        "German": "Parameterauswahl"
    },
    "step_1_subheader": {
        "English": ":orange[Step 1: Select regions or feature of interest]",
        "French": ":orange[Étape 1 : Sélectionnez les régions ou caractéristiques d'intérêt]",
        "German": ":orange[Schritt 1 : Wählen Sie Regionen oder interessante Merkmale aus]"
    },
    "step_2_subheader": {
        "English": ":orange[Step 2: Select date range]",
        "French": ":orange[Étape 2 : Sélectionnez la plage de dates]",
        "German": ":orange[Schritt 2: Wählen Sie den Datumsbereich aus]"
    },
    "step_3_subheader": {
        "English": ":orange[Step 3: Select objects of interest]",
        "French": ":orange[Étape 3 : Sélectionnez les objets d'intérêt]",
        "German": ":orange[Schritt 3: Wählen Sie interessante Objekte aus]"
    },
    "step_4_subheader": {
        "English": ":orange[Step 4: Confirm selections]",
        "French": ":orange[Étape 4 : Confirmer les sélections]",
        "German": ":orange[Schritt 4: Auswahl bestätigen]"
    },
    "step_5_subheader": {
        "English": ":orange[Step 5: Make rough draft]",
        "French": ":orange[Étape 5 : Rédigez un brouillon]",
        "German": ":orange[Schritt 5: Entwurf erstellen]"
    },
    "step_6_subheader": {
        "English": ":orange[Step 6: Scatterplot parameters]",
        "French": ":orange[Étape 6 : Nuage de points]",
        "German": ":orange[Schritt 6: Streuplot-Parameter]"
    },
    "step_7_subheader": {
        "English": ":orange[Step 7: Barchart parameters]",
        "French": ":orange[Étape 7 : Diagramme en barres]",
        "German": ":orange[Schritt 7: Balkendiagramm-Parameter]"
    },
    "start_date": {
        "English": "Start Date",
        "French": "Date de début",
        "German": "Anfangsdatum"
    },
    "end_date": {
        "English": "End Date",
        "French": "Date de fin",
        "German": "Enddatum"
    },
    "selected_date_range": {
        "English": "Selected Date Range",
        "French": "Plage de dates sélectionnée",
        "German": "Ausgewählter Datumsbereich"
    },
    "selected_parameters_subheader": {
        "English": "Selected Parameters",
        "French": "Paramètres sélectionnés",
        "German": "Ausgewählte Parameter"
    },
    "apply_filters_button": {
        "English": "Apply Filters",
        "French": "Appliquer les filtres",
        "German": "Filter anwenden"
    },
    "filters_applied_message": {
        "English": "Filters applied! ",
        "French": "Filtres appliqués ! ",
        "German": "Filter angewendet!"
    },
    "make_roughdraft": {
        "English": "Make Roughdraft",
        "French": "Créer un brouillon",
        "German": "Entwurf erstellen"
    },
    "survey_results": {
        "English":"Survey results",
        "French": "Résultats de l'enquête",
        "German": "Umfrageergebnisse"
    },
    "discussion": {
        "English": "Discussion",
        "French": "Discussion",
        "German": "Diskussion"
    },
    "shoreline_litter_assessment": {
        "English": "Shoreline litter assessment",
        "French": "Évaluation des déchets sur le littoral",
        "German": "Bewertung des Küstenmülls"
    },
    "summary": {
        "English": "Summary",
        "French": "Résumé",
        "German": "Zusammenfassung"
    },
    "rough_draft": {
        "English": "Rough draft",
        "French": "Brouillon",
        "German": "Entwurf"
    },
    "inventory": {
        "English": "Inventory",
        "French": "Inventaire",
        "German": "Inventar"
    },
    "confirmfilters": {
        "English": "Confirm Filters",
        "French": "Confirmer les filtres",
        "German": "Filter bestätigen"
    },
    "nofilters": {
        "English": "You have not selected any filters. This will return all data.",
        "French": "Vous n'avez sélectionné aucun filtre. Cela renverra toutes les données.",
        "German": "Sie haben keine Filter ausgewählt. Dies wird alle Daten zurückgeben."
    },
    "no_rough_draft_message" :{
        "English": "No rough-draft created",
        "French": "Aucun brouillon créé",
        "German": "Kein Entwurf erstellt"
    },
    "no_filter_warning": {
        "English": "You have not selected any filters. This will return all data.",
        "French": "Vous n'avez sélectionné aucun filtre. Cela renverra toutes les données.",
        "German": "Sie haben keine Filter ausgewählt. Dies wird alle Daten zurückgeben."
    },
    "please_apply_filters": {
        "English": "Please apply filters to see available objects.",
        "French": "Veuillez appliquer des filtres pour voir les objets disponibles.",
        "German": "Bitte wenden Sie Filter an, um verfügbare Objekte anzuzeigen."
    },
    "no_data_warning": {
        "English": "After applying the filters there must be data. Adjust filters and try again.",
        "French": "Après avoir appliqué les filtres, des données doivent être disponibles. Ajustez les filtres et réessayez.",
        "German": "Nach dem Anwenden der Filter müssen Daten vorhanden sein. Passen Sie die Filter an und versuchen Sie es erneut."
    },
    "confirm_filter": {
        "English": engish_filtertwo,
        "French": french_filtertwo,
        "German": german_filtertwo
    },
    "filters_confirmed_message": {
        "English": "Filters confirmed",
        "French": "Filtres confirmés",
        "German": "Filter bestätigt"
    },

    "filter_one_instructions": {
        "English": english_filterone,
        "French": french_filterone,
        "German": german_filterone
    },

    "confirm_denied" :  {
        "English": "Please apply the location filters and select any objects if you need to.",
        "French": "Veuillez appliquer les filtres de localisation et sélectionner des objets si nécessaire.",
        "German": "Bitte wenden Sie die Standortfilter an und wählen Sie bei Bedarf Objekte aus."
    },
    "update_captions": {
        "English": "You need to update the chart explanations before you can chat.",
        "French": "Vous devez mettre à jour les explications du graphique avant de pouvoir discuter.",
        "German": "Sie müssen die Diagrammerklärungen aktualisieren, bevor Sie chatten können."
    },
    "select_feature_type": {
        "English": "Select feature type",
        "French": "Sélectionnez le type de fonctionnalité",
        "German": "Funktionstyp auswählen"
    },
    "map_markers": {
        "English": "Map markers",
        "French": "Marqueurs de carte",
        "German": "Kartenmarkierungen"
    },
    "intro_one": intro_one,
    "intro_two": intro_two,
    "instruction_labels": {
        "English": English_instructions,
        "French": French_instructions,
        "German": German_instructions
    },
"pieces_per_meter": {
    "English": "pieces/meter",
    "French": "pièces/mètre",
    "German": "Stücke/Meter"
},
"color_markers_by" :{
    "English": "Color markers by",
    "French": "Colorier les marqueurs par",
    "German": "Markierungen einfärben nach"
},
"quantity": {
    "English": "quantity",
    "French": "quantité",
    "German": "Menge"
},
"number of samples": {
    "English": "number of samples",
    "French": "nombre d'échantillons",
    "German": "Anzahl der Proben"
},
"object": {
    "English": "object",
    "French": "objet",
    "German": "Objekt"
},

"pcs/m" : {
    "English": "pieces/meter",
    "French": "pièces/mètre",
    "German": "Stücke/Meter"
},
"explain_graphic" : {
    "English": "Explain graphic",
    "French": "Expliquer le graphique",
    "German": "Grafik erklären"
},
    "l": {"English": "Lake", "French": "Lac", "German": "See"},
    "r": {"English": "River", "French": "Rivière", "German": "Fluss"},
    "both": {"English": "Both", "French": "Les deux", "German": "Beide"}




}

def translate_columns(language):
    # Translation dictionaries for column names
    translations = {
        "French": {
            "code": "code",
            "object": "objet",
            "quantity": "quantité",
            "pcs/m": "pcs/m",
            "% of total": "% du total",
            "number of samples": "Nombre d'échantillons",
            "fail rate": "taux d'échec"
        },
        "German": {
            "code": "Code",
            "object": "Objekt",
            "quantity": "Menge",
            "pcs/m": "Stk/m",
            "% of total": "% des Gesamt",
            "number of samples": "Proben nummer",
            "fail rate": "Fehlerrate"
        }
    }

    # Return the translation dictionary for the requested language
    if language in translations:
        return translations[language]
    else:
        raise ValueError(f"Language '{language}' not supported. Choose 'French' or 'German'.")
