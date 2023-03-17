"""Tests for functions"""

import yaml

import akshara.varnakaarya as vk


def test_get_vinyaasa():
    """Test get_vinyaasa() function"""

    fname = "tests/sample_texts.yml"

    with open(fname, "r", encoding="utf-8") as file:
        data_dict = yaml.safe_load(file)

    data_dict = data_dict["vinyaasa"]

    for key in data_dict.keys():
        assert ",".join(vk.get_vinyaasa(key)) == data_dict[key]
