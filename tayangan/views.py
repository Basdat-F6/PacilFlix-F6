from django.shortcuts import render, redirect

data = [
    {
        "judul": "Inception",
        "sinopsis": "Film yang mengisahkan tentang pencuri yang dapat mencuri informasi dari alam bawah sadar seseorang melalui mimpi.",
        "trailer": "https://www.youtube.com/watch?v=YoHD9XEInc0",
        "tanggal_rilis": "16 Juli 2010",
        "total_view": 1000000,
        "aksi": "https://example.com/tayangan/1"
    },
    {
        "judul": "Interstellar",
        "sinopsis": "Film yang mengisahkan tentang perjalanan ruang angkasa untuk menyelamatkan umat manusia dari kelaparan di Bumi.",
        "trailer": "https://www.youtube.com/watch?v=zSWdZVtXT7E",
        "tanggal_rilis": "7 November 2014",
        "total_view": 1500000,
        "aksi": "https://example.com/tayangan/2"
    },
    {
        "judul": "The Dark Knight",
        "sinopsis": "Film yang mengisahkan tentang petualangan Batman melawan Joker, musuh bebuyutannya.",
        "trailer": "https://www.youtube.com/watch?v=EXeTwQWrcwY",
        "tanggal_rilis": "18 Juli 2008",
        "total_view": 2000000,
        "aksi": "https://example.com/tayangan/3"
    }
]

top_indonesia = [
    {
        "judul": "Dilan 1990",
        "sinopsis": "Film yang mengisahkan tentang kisah cinta remaja antara Dilan dan Milea di tahun 1990-an.",
        "trailer": "https://www.youtube.com/watch?v=lI7H7w6kN2M",
        "tanggal_rilis": "25 Januari 2018",
        "total_view": 500000,
        "aksi": "https://example.com/tayangan/dilan"
    },
    {
        "judul": "Gundala",
        "sinopsis": "Film yang mengisahkan tentang superhero lokal, Gundala, yang berjuang melawan kejahatan di Indonesia.",
        "trailer": "https://www.youtube.com/watch?v=bfKhfDJbjR8",
        "tanggal_rilis": "29 Agustus 2019",
        "total_view": 300000,
        "aksi": "https://example.com/tayangan/gundala"
    },
    {
        "judul": "Si Doel The Movie",
        "sinopsis": "Film yang mengisahkan tentang kehidupan Doel, seorang lelaki Jakarta yang memiliki cerita cinta rumit.",
        "trailer": "https://www.youtube.com/watch?v=b_NcpcYD8d0",
        "tanggal_rilis": "2 Agustus 2018",
        "total_view": 400000,
        "aksi": "https://example.com/tayangan/si-doel"
    }
]


def watch(request):
    context = {
        "data": data,
    }
    return render(request, "tayangan.html", context)


def detail_film(request):
    context = {
        "data": data,
    }
    return render(request, "detail_film.html", context)

def detail_series(request):
    context = {
        "data": data,
    }
    return render(request, "detail_series.html", context)

def episode(request):
    context = {
        "data": data,
    }
    return render(request, "episode.html", context)

def search(request):
    context = {
        "data": data,
    }
    return render(request, "hasil.html", context)

def topindonesia(request):
    context = {
        "data": top_indonesia,
    }
    return render(request, "tayangan.html", context)