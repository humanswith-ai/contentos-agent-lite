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


def test_ar_cliche_detected():
    r = antislop.scan("نقدم حلول مبتكرة وجودة عالية لتحقيق أفضل النتائج.", "ar")
    assert r["count"] >= 2
    assert any(h["lang"] == "ar" for h in r["hits"])


def test_ar_clean_text():
    r = antislop.scan("تعالج المنصة 100 ألف طلب في الثانية.", "ar")
    assert r["count"] == 0
    assert r["verdict"] == "clean"


def test_ar_dialect_flagged():
    r = antislop.scan("احنا عايزين نعمل ده دلوقتي.", "ar")
    assert any(h["rule"] == "ar_dialect" for h in r["hits"])


def test_ru_rules_not_applied_to_arabic():
    r = antislop.scan("حلول مبتكرة", "ar")
    assert all(h["lang"] != "ru" for h in r["hits"])
