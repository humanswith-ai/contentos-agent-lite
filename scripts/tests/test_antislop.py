from scripts import antislop


def test_clean_text():
    r = antislop.scan("Stripe processed $1.4T in 2024. Founders cut fees 12%.", "en")
    assert r["count"] == 0
    assert r["verdict"] == "clean"


def test_delve_is_hit():
    r = antislop.scan("Let's delve into the world of payments.", "en")
    assert any(h["rule"] == "delve" for h in r["hits"])
    assert r["count"] >= 1


def test_sycophantic_opening():
    r = antislop.scan("Great question! Payments matter.", "en")
    assert any(h["rule"] == "sycophantic_opening" for h in r["hits"])


def test_three_hits_blocks():
    txt = "In today's fast-paced world, let's delve into our robust seamless solution."
    r = antislop.scan(txt, "en")
    assert r["count"] >= 3
    assert r["verdict"] == "block"


def test_ru_calque_intensifier():
    r = antislop.scan("Наше мощное бесшовное революционное решение.", "ru")
    assert r["count"] >= 2
    assert any(h["lang"] == "ru" for h in r["hits"])
