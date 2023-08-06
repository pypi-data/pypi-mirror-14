#!/bin/bash
pandarus ../pandarus/tests/data/test_provinces.gpkg --field1=adm1_code ../pandarus/tests/data/test_countries.gpkg --field2=name test-province-intersect --no-bz2
pandarus ../pandarus/tests/data/test_provinces.gpkg --field1=adm1_code ../pandarus/tests/data/test_countries.gpkg --field2=name test-province-intersect csv
pandarus ../pandarus/tests/data/test_provinces.gpkg --field1=adm1_code ../pandarus/tests/data/test_countries.gpkg --field2=name test-province-intersect pickle

pandarus areas ../pandarus/tests/data/test_provinces.gpkg --field=adm1_code test-province-areas --no-bz2
pandarus areas ../pandarus/tests/data/test_provinces.gpkg --field=adm1_code test-province-areas --no-bz2 csv
pandarus areas ../pandarus/tests/data/test_provinces.gpkg --field=adm1_code test-province-areas --no-bz2 pickle

pandarus -h
pandarus --help
pandarus --version
