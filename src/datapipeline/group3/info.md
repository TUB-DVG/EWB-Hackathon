## Report Group Three 

Group three worked on integration of Open Street Map (OSM) with CityGML data. For this, a virtual Jupyter Lab environment was used, hosted by TU Munich. The code in 'group3' is the code that was used to generate the final result and is downloaded from that virtual environment. Due to limited sizes of the files, the full data is not included in this repository, the file '696_5346.gml' is a sample file. The groupd discussed the use of [aria2](https://aria2.github.io/) to mass download the data. 



Code for the evaluation of the results can be found in the file 'buildings_lod2.ipynb'. To install the necessary packages, the file 'pip-install.ipynb' can be used, once you have set up a venv. The file of buildings_lod2 size is too large, to be uploaded to GitHub, so to get a good uderstanding, download the repo and run it yourself.

In the group, the influnence of data processing on the quality of the results was discussed. Depending on the type of the spatial or or attribute merge, different results were obtained. In the discussion, it was mentioned that maybe several steps for obtaining the final result are necessary. For example first merging with 'Flurgundstücke' and then with the GML buildings.


