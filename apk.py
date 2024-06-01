import pandas as pd
from bokeh.io import output_file, show
from bokeh.models import CheckboxGroup, CustomJS, ColumnDataSource, DateRangeSlider
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.palettes import Category10, Category20
from bokeh.layouts import column, row, Spacer


# Charger les données
data = pd.read_csv('bokeh-app-main\\powerconsumption.csv', parse_dates=['Datetime'], date_parser=lambda x: pd.to_datetime(x, format='%m/%d/%Y %H:%M'))

# Créer une figure Bokeh pour la consommation d'énergie
p = figure(title="Évolution de la consommation d'énergie des trois zones (KW)",
           x_axis_type="datetime", width=650, height=275)

# Créer une figure Bokeh pour les flux
p2 = figure(title="Évolution du Flux diffus général et du flux diffus (kW/m²)",
            x_axis_type="datetime", width=650, height=275)

# Initialiser une liste pour stocker les lignes de données pour chaque zone
lines = []
lines2 = []

# Créer une couleur pour chaque zone
colors = Category10[3]
colors2 = Category20[20][:2]  # Utilisation des deux premières couleurs de Category20

# Parcourir les zones et créer une ligne pour chaque zone
for i, zone in enumerate(["Zone1", "Zone2", "Zone3"]):
    # Créer une source de données pour la zone spécifique
    source = ColumnDataSource(data=dict(
        Datetime=data["Datetime"],
        PowerConsumption=data[f"PowerConsumption_{zone}"]
    ))
    
    # Créer une ligne pour la zone
    line = p.line(x="Datetime", y="PowerConsumption", source=source,
                  color=colors[i], line_width=2, alpha=0.8, legend_label=zone)
    
    # Ajouter la ligne à la liste
    lines.append(line)

# Parcourir les flux et créer une ligne pour chaque flux
for j, flux in enumerate(["GeneralDiffuseFlows", "DiffuseFlows"]):
    # Créer une source de données pour le flux spécifique
    source = ColumnDataSource(data=dict(
        Datetime=data["Datetime"],
        flux=data[flux]
    ))
    
    # Créer une ligne pour le flux
    line2 = p2.line(x="Datetime", y="flux", source=source,
                    color=colors2[j], line_width=2, alpha=0.8, legend_label=flux)
    
    # Ajouter la ligne à la liste
    lines2.append(line2)

# Ajouter une légende à la figure
p.legend.location = "top_left"
p2.legend.location = "top_right"

# Créer une boîte à cocher pour chaque zone
checkboxes = CheckboxGroup(labels=["Zone1", "Zone2", "Zone3"], active=[0, 1, 2])
checkboxes2 = CheckboxGroup(labels=["GeneralDiffuseFlows", "DiffuseFlows"], active=[0, 1])

# Créer une fonction de rappel pour mettre à jour la visibilité des lignes en fonction de la boîte à cocher
callback = CustomJS(args=dict(lines=lines, checkboxes=checkboxes), code="""
    // Obtenir les indices des zones sélectionnées
    var selected_zones = checkboxes.active;
    
    // Parcourir toutes les lignes et mettre à jour leur visibilité
    for (var i = 0; i < lines.length; i++) {
        if (selected_zones.includes(i)) {
            lines[i].visible = true;
        } else {
            lines[i].visible = false;
        }
    }
""")

# Créer une fonction de rappel pour mettre à jour la visibilité des lignes en fonction de la boîte à cocher
callback2 = CustomJS(args=dict(lines=lines2, checkboxes=checkboxes2), code="""
    // Obtenir les indices des flux sélectionnés
    var selected_flux = checkboxes.active;
    
    // Parcourir toutes les lignes et mettre à jour leur visibilité
    for (var i = 0; i < lines.length; i++) {
        if (selected_flux.includes(i)) {
            lines[i].visible = true;
        } else {
            lines[i].visible = false;
        }
    }
""")

# Lier la fonction de rappel à la boîte à cocher
checkboxes.js_on_change("active", callback)
checkboxes2.js_on_change("active", callback2)

source = ColumnDataSource(data)

# Créer une figure
p3 = figure(x_axis_type='datetime', title='Evolution de l\'humidité en fonction du temps', height=275, width=650)
p3.xaxis.axis_label = 'Temps'
p3.yaxis.axis_label = 'Humidité'

# Ajouter une ligne pour l'humidité
p3.line('Datetime', 'Humidity', source=source, line_width=2, color=Category20[20][4], legend_label='Humidité relative (%)')


# Créer un DateRangeSlider pour définir l'intervalle de temps
date_range_slider = DateRangeSlider(value=(data['Datetime'].min(), data['Datetime'].max()),
                                    start=data['Datetime'].min(), end=data['Datetime'].max(), step=1, title="Intervalle de Temps")

# JavaScript callback3 pour mettre à jour la source des données
callback3 = CustomJS(args=dict(source=source, date_range_slider=date_range_slider, original_source=source.data), code="""
    var data = source.data;
    var original_data = original_source;
    var start_date = new Date(date_range_slider.value[0]);
    var end_date = new Date(date_range_slider.value[1]);
    
    // Filtrer les données en fonction du DateRangeSlider
    var new_time = [];
    var new_humidity = [];
    
    for (var i = 0; i < original_data['Datetime'].length; i++) {
        var current_date = new Date(original_data['Datetime'][i]).getTime();
        if (current_date >= start_date.getTime() && current_date <= end_date.getTime()) {
            new_time.push(original_data['Datetime'][i]);
            new_humidity.push(original_data['Humidity'][i]);
        }
    }
    
    source.data = {'Datetime': new_time, 'Humidity': new_humidity};
    source.change.emit();
""")

date_range_slider.js_on_change('value', callback3)






# Préparer les données
source_temp = ColumnDataSource(data)

# Créer une figure
p4 = figure(x_axis_type='datetime', title='Evolution de la température en fonction du temps', height=275, width=650)
p4.xaxis.axis_label = 'Temps'
p4.yaxis.axis_label = 'Temperature'

# Ajouter une ligne pour la température
p4.line('Datetime', 'Temperature', source=source_temp, line_width=2, color=Category20[20][6], legend_label='Température (°C)')

# Créer un DateRangeSlider pour définir l'intervalle de temps
date_range_slider_temperature = DateRangeSlider(value=(data['Datetime'].min(), data['Datetime'].max()),
                                    start=data['Datetime'].min(), end=data['Datetime'].max(), step=1, title="Intervalle de Temps")

# JavaScript callback4 pour mettre à jour la source des données
callback4 = CustomJS(args=dict(source=source_temp, date_range_slider=date_range_slider_temperature, original_source=source_temp.data), code="""
    var data = source.data;
    var original_data = original_source;
    var start_date = new Date(date_range_slider.value[0]);
    var end_date = new Date(date_range_slider.value[1]);
    
    // Filtrer les données en fonction du DateRangeSlider
    var new_time = [];
    var new_Temperature = [];
    
    for (var i = 0; i < original_data['Datetime'].length; i++) {
        var current_date = new Date(original_data['Datetime'][i]).getTime();
        if (current_date >= start_date.getTime() && current_date <= end_date.getTime()) {
            new_time.push(original_data['Datetime'][i]);
            new_Temperature.push(original_data['Temperature'][i]);
        }
    }
    
    source.data = {'Datetime': new_time, 'Temperature': new_Temperature};
    source.change.emit();
""")

date_range_slider_temperature.js_on_change('value', callback4)





data5 = pd.read_csv('bokeh-app-main\\powerconsumption.csv', parse_dates=["Datetime"], date_parser=lambda x: pd.to_datetime(x, format="%m/%d/%Y %H:%M"))

# Calculer l'indice de Thom pour chaque ligne
data5["THI"] = data5["Temperature"] - ((0.55 - 0.0055 * data5["Humidity"]/100.0) * (data5["Temperature"] - 14.5))

# Préparer les données
source_5 = ColumnDataSource(data5)

# Créer une figure principale
main_plot = figure(x_axis_type="datetime", title="Evolution de l'indice de Thom en fonction du temps ", height=275, width=600)
main_plot.xaxis.axis_label = "Temps"
main_plot.yaxis.axis_label = "Indice de Thom °C"

# Ajouter une ligne pour l'indice de Thom
main_plot.line("Datetime", "THI", source=source_5, line_width=2, legend_label="Indice de Thom")

# Créer un curseur de plage de dates pour définir l'intervalle de temps
date_range_slider_5 = DateRangeSlider(value=(data5["Datetime"].min(), data5["Datetime"].max()),
                                    start=data5["Datetime"].min(), end=data5["Datetime"].max(), step=1, title="Plage de Dates")

# JavaScript callback pour mettre à jour la source des données en fonction du curseur de plage de dates
callback_5 = CustomJS(args=dict(source=source_5, date_range_slider=date_range_slider_5, original_source=source_5.data), code="""
    var data = source.data;
    var original_data = original_source;
    var start_date = new Date(date_range_slider.value[0]);
    var end_date = new Date(date_range_slider.value[1]);
    
    // Filtrer les données en fonction du curseur de plage de dates
    var new_time = [];
    var new_thi = [];
    
    for (var i = 0; i < original_data["Datetime"].length; i++) {
        var current_date = new Date(original_data["Datetime"][i]).getTime();
        if (current_date >= start_date.getTime() && current_date <= end_date.getTime()) {
            new_time.push(original_data["Datetime"][i]);
            new_thi.push(original_data["THI"][i]);
        }
    }
    
    source.data = {"Datetime": new_time, "THI": new_thi};
    source.change.emit();
""")

date_range_slider_5.js_on_change("value", callback_5)


# Créer une mise en page pour chaque figure et ses contrôles, en centrant les sliders
p_layout = column(p, checkboxes)
p2_layout = column(p2, checkboxes2)

# Créer une colonne pour la figure p3 avec le date_range_slider
p3_layout = column(p3, date_range_slider, sizing_mode='scale_width')

# Créer une colonne pour la figure p4 avec le date_range_slider_temperature
p4_layout = column(p4, date_range_slider_temperature, sizing_mode='scale_width')

# Créer une colonne pour la figure principale avec le date_range_slider_5
p5_layout = column(main_plot, date_range_slider_5, sizing_mode='scale_width')

# Créer une mise en page pour afficher les figures et les boîtes à cocher
layout = column(
    row(p_layout, p2_layout),
    row(p3_layout, p4_layout),
    row(Spacer(width=300), p5_layout, Spacer(width=300))  # Centrer p5_layout en ajoutant des espaces de chaque côté
)


# Enregistrer la sortie dans un fichier HTML et l'afficher
output_file("visualisation.html")
show(layout)
