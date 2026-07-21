import json
import re

import pytest


YES_NO_PATTERN = re.compile(r"^(?:ya|tidak)\s*$")


@pytest.mark.parametrize("output", ["ya", "tidak", "ya\n"])
def test_yes_no_valid_output(output: str) -> None:
    assert YES_NO_PATTERN.fullmatch(output)


@pytest.mark.parametrize("output", ["Ya", "mungkin", "ya, benar"])
def test_yes_no_rejects_invalid_output(output: str) -> None:
    assert not YES_NO_PATTERN.fullmatch(output)


def test_json_example_is_valid() -> None:
    output = '{"nama":"Kopi Gayo","harga":75000}'
    assert json.loads(output) == {"nama": "Kopi Gayo", "harga": 75000}


def test_user_profile_shape() -> None:
    output = '{"nama":"Dinda","usia":27,"kota":"Bandung","minat":["membaca"]}'
    profile = json.loads(output)
    assert list(profile) == ["nama", "usia", "kota", "minat"]
    assert isinstance(profile["nama"], str)
    assert 0 <= profile["usia"] <= 150
    assert isinstance(profile["kota"], str)
    assert all(isinstance(item, str) for item in profile["minat"])


def test_police_report_shape() -> None:
    output = (
        '{"nama_pelapor":"Rina","kontak_pelapor":"081234567890",'
        '"jenis_laporan":"pencurian","waktu_kejadian":"20 Juli 2026 pukul 19.30",'
        '"lokasi_kejadian":"Area parkir Pasar Baru, Jakarta",'
        '"uraian":"Ponsel pelapor dicuri","terlapor":"",'
        '"saksi":["Pak Dedi"],"barang_bukti":["rekaman CCTV","nota pembelian"],'
        '"tindakan_segera":false}'
    )
    report = json.loads(output)
    assert list(report) == [
        "nama_pelapor",
        "kontak_pelapor",
        "jenis_laporan",
        "waktu_kejadian",
        "lokasi_kejadian",
        "uraian",
        "terlapor",
        "saksi",
        "barang_bukti",
        "tindakan_segera",
    ]
    assert report["jenis_laporan"] in {
        "kehilangan",
        "pencurian",
        "penipuan",
        "kekerasan",
        "gangguan_kamtibmas",
        "lainnya",
    }
    assert all(isinstance(item, str) for item in report["saksi"])
    assert all(isinstance(item, str) for item in report["barang_bukti"])
    assert isinstance(report["tindakan_segera"], bool)
