# Scraping Chronicling America newspaper articles via API

This repository contains the complete code and usage examples for retrieving full-text newspaper articles from the [Chronicling America](https://www.loc.gov/collections/chronicling-america/about-this-collection/) database using its API. Further information on the [API services](https://www.loc.gov/apis/micro-services/text-services/) can be found on the Library of Congress website.

The scripts allow users to retrieve the full text of articles, text snippets centered on a specified keyword (highlighted), and related metadata, including a unique ID, newspaper title, location (state and city), and date of publication. The output is provided in JSON and CSV formats.

The code integrates multiple options for advanced queries. The present use case focuses on Chinese students in the United States, but the scripts can support any other topic by simply modifying the search terms in the API request URL.

In addition, supplementary scripts generate summary statistics and visualizations based on the query results, including statistics by newspaper title, geographic location (state and city), and temporal distribution. 

A guide detailing the applied data-processing pipeline is also provided in both Markdown (.md) and PDF formats. 
