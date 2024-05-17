from django.shortcuts import render, redirect

data = [
    {
      "judul": "The Great Adventure",
      "sinopsis": "An epic journey through uncharted lands.",
      "trailer_url": "https://youtu.be/ft70sAYrFyY",
      "tanggal_rilis": "2024-01-01",
      "total_view": 12000
    },
    {
      "judul": "Mystery of the Depths",
      "sinopsis": "Exploring the secrets beneath the ocean.",
      "trailer_url": "https://youtu.be/ft70sAYrFyY",
      "tanggal_rilis": "2024-02-15",
      "total_view": 9500
    },
    {
      "judul": "Lost in Time",
      "sinopsis": "A journey back to the age of dinosaurs.",
      "trailer_url": "https://youtu.be/ft70sAYrFyY",
      "tanggal_rilis": "2024-03-22",
      "total_view": 11000
    },
    {
      "judul": "Sky High",
      "sinopsis": "The thrill of flight and the beauty of the sky.",
      "trailer_url": "https://youtu.be/ft70sAYrFyY",
      "tanggal_rilis": "2024-04-18",
      "total_view": 10500
    },
    {
      "judul": "Desert Mirage",
      "sinopsis": "Survival and mirages in the vast desert.",
      "trailer_url": "https://youtu.be/ft70sAYrFyY",
      "tanggal_rilis": "2024-05-05",
      "total_view": 9000
    }
  ]
film = [
    {
      "judul": "The Great Adventure",
      "sinopsis": "An epic journey through uncharted lands.",
      "trailer_url": "https://youtu.be/ft70sAYrFyY",
      "tanggal_rilis": "2024-01-01",
      "total_view": 12000
    },
    {
      "judul": "Mystery of the Depths",
      "sinopsis": "Exploring the secrets beneath the ocean.",
      "trailer_url": "https://youtu.be/ft70sAYrFyY",
      "tanggal_rilis": "2024-02-15",
      "total_view": 9500
    },
    {
      "judul": "Lost in Time",
      "sinopsis": "A journey back to the age of dinosaurs.",
      "trailer_url": "https://youtu.be/ft70sAYrFyY",
      "tanggal_rilis": "2024-03-22",
      "total_view": 11000
    }
  ]

series = [
    {
      "judul": "Sky High",
      "sinopsis": "The thrill of flight and the beauty of the sky.",
      "trailer_url": "https://youtu.be/ft70sAYrFyY",
      "tanggal_rilis": "2024-04-18",
      "total_view": 10500
    },
    {
      "judul": "Desert Mirage",
      "sinopsis": "Survival and mirages in the vast desert.",
      "trailer_url": "https://youtu.be/ft70sAYrFyY",
      "tanggal_rilis": "2024-05-05",
      "total_view": 9000
    }
  ]

top_indonesia = [
    {
      "judul": "Dilan 1990",
      "sinopsis": "Film yang mengisahkan tentang kisah cinta remaja antara Dilan dan Milea di tahun 1990-an.",
      "trailer_url": "https://www.youtube.com/watch?v=lI7H7w6kN2M",
      "tanggal_rilis": "25 Januari 2018",
      "total_view": 500000
    },
    {
      "judul": "Gundala",
      "sinopsis": "Film yang mengisahkan tentang superhero lokal, Gundala, yang berjuang melawan kejahatan di Indonesia.",
      "trailer_url": "https://www.youtube.com/watch?v=bfKhfDJbjR8",
      "tanggal_rilis": "29 Agustus 2019",
      "total_view": 300000
    },
    {
      "judul": "Si Doel The Movie",
      "sinopsis": "Film yang mengisahkan tentang kehidupan Doel, seorang lelaki Jakarta yang memiliki cerita cinta rumit.",
      "trailer_url": "https://www.youtube.com/watch?v=b_NcpcYD8d0",
      "tanggal_rilis": "2 Agustus 2018",
      "total_view": 400000
    }
  ]

def show_trailers(request):
    context = {
        "trailers": data,
        "film": film,
        "series": series,
    }
    return render(request, "trailer_list.html", context)

def show_top_indo(request):
    context = {
        "trailers": top_indonesia,
        "film": film,
        "series": series,
    }
    return render(request, "trailer_list.html", context)