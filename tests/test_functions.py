"""Tests for functions"""

import akshara.varnakaarya as vk


def test_get_vinyaasa():
    """Test get_vinyaasa() function"""

    assert vk.get_vinyaasa("अरिन्दमः") == [
        "अ",
        "र्",
        "इ",
        "न्",
        "द्",
        "अ",
        "म्",
        "अ",
        "ः",
    ]
    assert vk.get_vinyaasa("संस्कृतम्") == [
        "स्",
        "अ",
        "ं",
        "स्",
        "क्",
        "ऋ",
        "त्",
        "अ",
        "म्",
    ]
