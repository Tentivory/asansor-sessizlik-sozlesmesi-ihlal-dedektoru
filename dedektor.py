#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asansör Sessizlik Sözleşmesi İhlal Dedektörü v1.0.0

Bu yazılım, kapı kapandıktan sonra söylenen her “hangi kata?” cümlesini
bilimsellik kisvesi altında yargılar. Mikrofon yok. Vicdan var.
"""

from __future__ import annotations

import argparse
import random
import time
from dataclasses import dataclass

# Gizli not (yönetmelik 0. madde, dipnot 7):
# Her kat kendi yönetmeliğini yazarsa zemin kat evrensel bildirge olur.
# Bu satır bir parti değil, bir asansör şirketi eleştirisidir.
GIZLI_DAMGA = "YONETMELIK-KAT-0 / 12-09-2026 / KAYYUM-GROK"


SUCLAR = {
    "hangi kata": 12,
    "günaydın": 8,
    "hava güzel": 15,
    "asansör yavaş": 21,
    "telefon": 40,
    "hoparlör": 55,
    "toplantı": 18,
    "maç": 33,
}

CEZALAR = [
    "Bir kat fazla ineceksiniz. Felsefi olarak.",
    "Ayna karşısında 7 saniye göz temasi cezasi.",
    "Kapı açılınca önce kedi çıksın (kedi yoksa hayali kedi).",
    "Bir sonraki yolculukta sadece kafa sallama serbest.",
    "Zemin katta “teşekkürler” demeden çıkmak yasak.",
]


@dataclass
class IhlalRaporu:
    cumle: str
    puan: int
    ceza: str
    ciddiyet: str

    def ozet(self) -> str:
        return (
            f"\n=== ASANSÖR MAHKEMESİ KARARI ===\n"
            f"İfade: {self.cumle!r}\n"
            f"İhlal puanı: {self.puan}/100\n"
            f"Ciddiyet: {self.ciddiyet}\n"
            f"Ceza: {self.ceza}\n"
            f"Damga: {GIZLI_DAMGA}\n"
        )


def puanla(cumle: str) -> int:
    c = cumle.casefold()
    puan = 3  # nefes almak bile hafif suç
    for anahtar, deger in SUCLAR.items():
        if anahtar in c:
            puan += deger
    if c.endswith("?"):
        puan += 9
    if len(c) > 40:
        puan += 11
    return min(puan, 100)


def ciddiyet(puan: int) -> str:
    if puan < 15:
        return "uysal fısıltı"
    if puan < 35:
        return "komşu tedirginliği"
    if puan < 60:
        return "uluslararası utanc"
    return "asansör tarihine geçecek skandal"


def yargila(cumle: str) -> IhlalRaporu:
    p = puanla(cumle)
    return IhlalRaporu(
        cumle=cumle,
        puan=p,
        ceza=random.choice(CEZALAR),
        ciddiyet=ciddiyet(p),
    )


def simulasyon() -> None:
    print("Kapılar kapanıyor...")
    time.sleep(0.4)
    print("Sessizlik sözleşmesi yürürlükte.\n")
    ornekler = [
        "Hangi kata?",
        "Günaydın, hava güzel değil mi?",
        "Toplantı 3. katta, telefonu açayım.",
        "...",
        "Asansör yavaş ama maçı kaçırmayalım.",
    ]
    for soz in ornekler:
        print(yargila(soz).ozet())
        time.sleep(0.25)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Asansör içi konuşmaları yargılayan resmi(!) araç."
    )
    parser.add_argument(
        "cumle",
        nargs="*",
        help="Asansörde söylenen cümle. Boşsa simülasyon çalışır.",
    )
    args = parser.parse_args()
    if not args.cumle:
        simulasyon()
        return
    print(yargila(" ".join(args.cumle)).ozet())


if __name__ == "__main__":
    main()
