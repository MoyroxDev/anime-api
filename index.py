from flask import Flask, request, jsonify
from animeflv import AnimeFLV

app = Flask(__name__)

@app.route('/latest', methods=['GET'])
def get_latest_episodes():
    """Obtener los últimos episodios estrenados."""
    with AnimeFLV() as api:
        latest_episodes = api.get_latest_episodes()
        response = [
            {
                'anime_title': episode.anime,
                'episode_id': episode.id,  # ID del episodio
                'image_url': episode.image_preview # Imagen del anime
            }
            for episode in latest_episodes
        ]
        return jsonify(response)

@app.route('/latest-animes', methods=['GET'])
def get_latest_animes():
    """Obtener los últimos animes agregados."""
    with AnimeFLV() as api:
        latest_animes = api.get_latest_animes()
        response = [
            {
                'anime_id': anime.id,
                'title': anime.title,
                'type': anime.type,
                'image_url': anime.poster,  # URL de la imagen del anime
            }
            for anime in latest_animes
        ]
        return jsonify(response)

@app.route('/search', methods=['GET'])
def search_anime():
    """Buscar animes por nombre."""
    # http://127.0.0.1:5000/search?query=naruto example
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Se requiere un parámetro "query".'}), 400
    
    with AnimeFLV() as api:
        resultados = api.search(query)
        return jsonify([{'id': anime.id, 'title': anime.title} for anime in resultados])

@app.route('/anime/<string:anime_id>', methods=['GET'])
def get_anime_info(anime_id):
    """Obtener información detallada de un anime específico por ID."""
    with AnimeFLV() as api:
        info_anime = api.get_anime_info(anime_id)

        # Preparar datos detallados del anime
        anime_data = {
            'title': info_anime.title,
            'description': info_anime.synopsis,
            'rating': info_anime.rating,
            'status': info_anime.debut,
            'poster_url': info_anime.poster,
            'banner': info_anime.banner,
            'episodes': info_anime.episodes,
            'type': info_anime.type
        }
        return jsonify(anime_data)

@app.route('/episode/<string:anime_id>/<int:episode_id>/streaming', methods=['GET'])
def get_video_servers(anime_id, episode_id):
    """Obtener enlaces de streaming para un episodio específico."""
    with AnimeFLV() as api:
        servidores = api.get_video_servers(anime_id, episode_id)
        return jsonify(servidores)

@app.route('/episode/<string:anime_id>/<int:episode_id>/download', methods=['GET'])
def get_download_links(anime_id, episode_id):
    """Obtener enlaces de descarga para un episodio específico."""
    with AnimeFLV() as api:
        servidores = api.get_links(anime_id, episode_id)
        return jsonify([{'server': servidor.server, 'url': servidor.url} for servidor in servidores])

if __name__ == '__main__':
    app.run(debug=True)
