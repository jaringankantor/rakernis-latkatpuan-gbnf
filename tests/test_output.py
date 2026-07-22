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


def test_log_analysis_shape() -> None:
    output = (
        '{"sumber_log":"core-switch-01","jenis_perangkat":"perangkat_jaringan",'
        '"waktu_kejadian":"23 Juli 2026 pukul 08.14 WIB",'
        '"tingkat_keparahan":"kritis","status":"insiden_aktif",'
        '"masalah_terdeteksi":"MAC flapping pada VLAN 120",'
        '"bukti_log":["MAC 00aa.11bb.22cc berpindah antara Gi1/0/23 dan Gi1/0/24"],'
        '"dampak":"Potensi gangguan konektivitas VLAN 120",'
        '"perlu_tindak_lanjut":true,"urgensi":"segera",'
        '"rekomendasi":["Periksa loop pada port Gi1/0/23 dan Gi1/0/24"],'
        '"informasi_tambahan_dibutuhkan":["Topologi dan status spanning-tree VLAN 120"]}'
    )
    analysis = json.loads(output)
    assert list(analysis) == [
        "sumber_log",
        "jenis_perangkat",
        "waktu_kejadian",
        "tingkat_keparahan",
        "status",
        "masalah_terdeteksi",
        "bukti_log",
        "dampak",
        "perlu_tindak_lanjut",
        "urgensi",
        "rekomendasi",
        "informasi_tambahan_dibutuhkan",
    ]
    assert analysis["jenis_perangkat"] in {
        "perangkat_jaringan",
        "server",
        "tidak_diketahui",
    }
    assert analysis["tingkat_keparahan"] in {"info", "peringatan", "kritis"}
    assert analysis["status"] in {
        "normal",
        "perlu_dipantau",
        "perlu_tindak_lanjut",
        "insiden_aktif",
    }
    assert isinstance(analysis["perlu_tindak_lanjut"], bool)
    assert analysis["urgensi"] in {"tidak_perlu", "terjadwal", "segera"}
    for field in ("bukti_log", "rekomendasi", "informasi_tambahan_dibutuhkan"):
        assert all(isinstance(item, str) for item in analysis[field])
