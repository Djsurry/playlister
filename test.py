import youtube_dl

playlists = [
    "https://www.youtube.com/playlist?list=PLBRIO7dbinFq7Xf_O9rjjUA5HE8fxE6c4"
]

for playlist in playlists:

    with youtube_dl.YoutubeDL({"ignoreerrors": True, "quiet": True}) as ydl:
        playlist_dict = ydl.extract_info(playlist, download=False)

    print(playlist_dict)
