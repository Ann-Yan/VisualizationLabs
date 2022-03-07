import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

st.title("CSE 5544 Lab 3: Ethics in Data Visualization")


df_data = pd.read_csv("https://raw.githubusercontent.com/Ann-Yan/VisualizationLabs/main/CSE5544.Lab1.ClimateData%20-%20Sheet1.csv")
df_data.rename(columns={"Country\year":"Country/Region"}, inplace=True)

#Data preprocessing - keep in final

source = df_data
omissionList = ["OECD - Total"] #"European Union (28 countries)", "OECD - Europe", "OECD America", 
source = source.loc[~source["Country/Region"].isin(omissionList)]
countries = df_data['Country/Region']
source = pd.melt(source, id_vars=["Country/Region", "Non-OECD Economies"], var_name="Year", value_vars=["1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"], value_name="Emissions")
source['Emissions'] = source['Emissions'].apply(pd.to_numeric, errors='coerce')

# #Overview scatter plot
# st.header("Overview")
# st.text("A scatter plot summary of the data, with the omission of OECD - Total.")
# source = pd.melt(source, id_vars=["Country/Region", "Non-OECD Economies"], var_name="Year", value_vars=["1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"], value_name="Emissions")
# chart = alt.Chart(source).mark_point().encode(
#     x = "Country/Region:N",
#     y = "Emissions:Q",
#     color = "Non-OECD Economies",
#     tooltip=['Country/Region', 'Non-OECD Economies', 'Year', 'Emissions']
# ).properties(
#     height=500
# ).interactive()
# st.altair_chart(chart, use_container_width = True)


#HEATMAPS
st.subheader("Heatmap Overview")

#heatmap - colorful
heatmapP1 = df_data
heatmapP1 = heatmapP1.drop(columns=['Non-OECD Economies'])
omissionList = ["OECD - Total"] #"European Union (28 countries)", "OECD - Europe", "OECD America", 
heatmapP1 = heatmapP1.loc[~heatmapP1["Country/Region"].isin(omissionList)]
heatmapP1 = pd.melt(heatmapP1, id_vars=['Country/Region'], var_name='Year')
heatmapP1.rename(columns={"value":"Emissions"}, inplace = True)
heatmapP1['Emissions'] = heatmapP1['Emissions'].apply(pd.to_numeric, errors='coerce')
#heatmapP1

hm1 = alt.Chart(heatmapP1, title="Heatmap of Global Emissions (Rainbow)").mark_rect().encode(
    x=alt.X('Country/Region:N', title = 'Country'),
    y=alt.Y('Year:O', title = 'Year'),
    color=alt.Color('Emissions:Q', scale=alt.Scale(scheme="turbo")),
    tooltip=["Country/Region", "Year", "Emissions"]
).interactive()

st.altair_chart(hm1, use_container_width = True)

#Heatmap - monochrome
heatmapP2 = heatmapP1

hm2 = alt.Chart(heatmapP2, title="Heatmap of Global Emissions (Monochrome)").mark_rect().encode(
    x=alt.X('Country/Region:N', title = 'Country'),
    y=alt.Y('Year:O', title = 'Year'),
    color=alt.Color('Emissions:Q', scale=alt.Scale(scheme="greys")),
    tooltip=["Country/Region", "Year", "Emissions"]
).interactive()

st.altair_chart(hm2, use_container_width = True)

st.subheader("Heatmap Comparisons")
st.markdown("The colorful heatmap is not as useful as the monochrome one.")
st.markdown("The colorful heatmap is just an array of hues, given some non-intuitive order.")
st.markdown("This makes it difficult for the viewer to discern the true differences between the different colors on the heatmap.")
st.markdown("Furthermore, there is no reason to have as many hues in this heatmap as is offered by the rainbow colormap.")
st.markdown("After all, there are very few structures in the data that need to be emphasized (emissions).")
st.markdown("In comparison, the monochrome is a changing of luminance.")
st.markdown("The changes in luminance are more intuitive to the viewer.")
st.markdown("Additionally, it is known that ordered colormaps, such as the one used in heatmaps, are more effective when they vary in saturation or luminance.")
st.markdown("Thus, the rainbow colormap is less effective than the monochrome one.")



st.header("Additional Visual")


#P1
with st.container():
    option = st.multiselect("Select the countries to view.", countries, ["United States"])

    st.subheader("Emissions Data by Country per Year")

    filter_data = source.loc[source["Country/Region"].isin(option)]
    #filter_data
    bar_chart = alt.Chart(filter_data).mark_bar().encode(
        column = "Year:O",
        x = alt.X("Country/Region:N", title = ""),
        y = "Emissions:Q",
        color = "Country/Region",
        tooltip = ["Country/Region", "Year", "Emissions", "Non-OECD Economies"]
    ).properties(
        width=(len(option)*10)
    ).interactive()

    st.altair_chart(bar_chart) #, use_container_width = True)


#P2
with st.container():
    filter_data2 = filter_data
    #filter_data2
    bar_chart2 = alt.Chart(filter_data2).mark_bar().encode(
        x = "Year:O",
        y = "Emissions:Q",
        color = "Country/Region",
        tooltip = ["Country/Region", "Year", "Emissions", "Non-OECD Economies"]
    ).interactive()

    st.altair_chart(bar_chart2) #, use_container_width = True)


st.markdown("The first visual shows grouped bar charts, where you can view each country's emissions per year.")
st.markdown("The second visual shows stacked bar charts, wehre you can see each country's emissions levels stacked atop one another based on year.")
st.markdown("The first visual is better than the second.")
st.markdown("The second visual's stacking makes it difficult to discern the true amount of emissions produced per country.")
st.markdown("Were a large-emitting country be shown alongside a low-emitting country, the low-emitting country would barely be seen on the plot, making it seem it produced no emissions that year.")
st.markdown("The first visual more accurately shows the magnitude of emissions each country contributed to each year.")
st.markdown("You can also easily compare how much each country's emissions have changed from year to year with both itself and to other nations.")
st.markdown("The second plot makes this comparison difficult, if not impossible to do due to the nature of the stacking.")



st.header("Code")

code = '''import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import altair as alt

st.title("CSE 5544 Lab 3: Ethics in Data Visualization")


df_data = pd.read_csv("https://raw.githubusercontent.com/Ann-Yan/VisualizationLabs/main/CSE5544.Lab1.ClimateData%20-%20Sheet1.csv")
df_data.rename(columns={"Country\year":"Country/Region"}, inplace=True)

#Data preprocessing - keep in final

source = df_data
omissionList = ["OECD - Total"] #"European Union (28 countries)", "OECD - Europe", "OECD America", 
source = source.loc[~source["Country/Region"].isin(omissionList)]
countries = df_data['Country/Region']
source = pd.melt(source, id_vars=["Country/Region", "Non-OECD Economies"], var_name="Year", value_vars=["1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"], value_name="Emissions")
source['Emissions'] = source['Emissions'].apply(pd.to_numeric, errors='coerce')


#HEATMAPS
st.subheader("Heatmap Overview")

#heatmap - colorful
heatmapP1 = df_data
heatmapP1 = heatmapP1.drop(columns=['Non-OECD Economies'])
omissionList = ["OECD - Total"] #"European Union (28 countries)", "OECD - Europe", "OECD America", 
heatmapP1 = heatmapP1.loc[~heatmapP1["Country/Region"].isin(omissionList)]
heatmapP1 = pd.melt(heatmapP1, id_vars=['Country/Region'], var_name='Year')
heatmapP1.rename(columns={"value":"Emissions"}, inplace = True)
heatmapP1['Emissions'] = heatmapP1['Emissions'].apply(pd.to_numeric, errors='coerce')
#heatmapP1

hm1 = alt.Chart(heatmapP1, title="Heatmap of Global Emissions (Rainbow)").mark_rect().encode(
    x=alt.X('Country/Region:N', title = 'Country'),
    y=alt.Y('Year:O', title = 'Year'),
    color=alt.Color('Emissions:Q', scale=alt.Scale(scheme="turbo")),
    tooltip=["Country/Region", "Year", "Emissions"]
).interactive()

st.altair_chart(hm1, use_container_width = True)

#Heatmap - monochrome
heatmapP2 = heatmapP1

hm2 = alt.Chart(heatmapP2, title="Heatmap of Global Emissions (Monochrome)").mark_rect().encode(
    x=alt.X('Country/Region:N', title = 'Country'),
    y=alt.Y('Year:O', title = 'Year'),
    color=alt.Color('Emissions:Q', scale=alt.Scale(scheme="greys")),
    tooltip=["Country/Region", "Year", "Emissions"]
).interactive()

st.altair_chart(hm2, use_container_width = True)

st.subheader("Heatmap Comparisons")
st.markdown("The colorful heatmap is not as useful as the monochrome one.")
st.markdown("The colorful heatmap is just an array of hues, given some non-intuitive order.")
st.markdown("This makes it difficult for the viewer to discern the true differences between the different colors on the heatmap.")
st.markdown("Furthermore, there is no reason to have as many hues in this heatmap as is offered by the rainbow colormap.")
st.markdown("After all, there are very few structures in the data that need to be emphasized (emissions).")
st.markdown("In comparison, the monochrome is a changing of luminance.")
st.markdown("The changes in luminance are more intuitive to the viewer.")
st.markdown("Additionally, it is known that ordered colormaps, such as the one used in heatmaps, are more effective when they vary in saturation or luminance.")
st.markdown("Thus, the rainbow colormap is less effective than the monochrome one.")



st.header("Additional Visual")


#P1
with st.container():
    option = st.multiselect("Select the countries to view.", countries, ["United States"])

    st.subheader("Emissions Data by Country per Year")

    filter_data = source.loc[source["Country/Region"].isin(option)]
    #filter_data
    bar_chart = alt.Chart(filter_data).mark_bar().encode(
        column = "Year:O",
        x = alt.X("Country/Region:N", title = ""),
        y = "Emissions:Q",
        color = "Country/Region",
        tooltip = ["Country/Region", "Year", "Emissions", "Non-OECD Economies"]
    ).properties(
        width=(len(option)*10)
    ).interactive()

    st.altair_chart(bar_chart) #, use_container_width = True)


#P2
with st.container():
    filter_data2 = filter_data
    #filter_data2
    bar_chart2 = alt.Chart(filter_data2).mark_bar().encode(
        x = "Year:O",
        y = "Emissions:Q",
        color = "Country/Region",
        tooltip = ["Country/Region", "Year", "Emissions", "Non-OECD Economies"]
    ).interactive()

    st.altair_chart(bar_chart2) #, use_container_width = True)


st.markdown("The first visual shows grouped bar charts, where you can view each country's emissions per year.")
st.markdown("The second visual shows stacked bar charts, wehre you can see each country's emissions levels stacked atop one another based on year.")
st.markdown("The first visual is better than the second.")
st.markdown("The second visual's stacking makes it difficult to discern the true amount of emissions produced per country.")
st.markdown("Were a large-emitting country be shown alongside a low-emitting country, the low-emitting country would barely be seen on the plot, making it seem it produced no emissions that year.")
st.markdown("The first visual more accurately shows the magnitude of emissions each country contributed to each year.")
st.markdown("You can also easily compare how much each country's emissions have changed from year to year with both itself and to other nations.")
st.markdown("The second plot makes this comparison difficult, if not impossible to do due to the nature of the stacking.")'''
st.code(code, language='python')