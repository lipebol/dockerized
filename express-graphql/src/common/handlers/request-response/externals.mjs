
export class Externals {

    static async initialize(handler) {
        if (handler.about.resolver in Externals) {
            return await Externals[handler.about.resolver](handler)
        }
    }

    static async spotifyAPI(handler) {
        let response = await Externals.get(
            `https://api.spotify.com/v1/tracks/${handler.params}`,
            handler.authExternal
        )

        handler[response.status_code ? 'error' : 'data'] = response.status_code ?
            response : {
                duration_ms: response.duration_ms, disc_number: response.disc_number,
                track_number: response.track_number, popularity: response.popularity,
                explicit: response.explicit, isrc: response.external_ids.isrc,
                url: response.external_urls.spotify, name: response.name
            }


        if (!handler.error && handler.fields.includes('album')) {
            response = await Externals.get(
                response.album.href, handler.authExternal
            )

            if (response.status_code) { handler.error = response }
            else {
                handler.data.album = {
                    id: response.id, name: response.name, album_type: response.album_type,
                    total_tracks: response.total_tracks, copyrights: response.copyrights,
                    external_url: response.external_urls.spotify, label: response.label,
                    release_date: response.release_date, images: response.images,
                    available_markets: response.available_markets
                }
            }
        }

        if (!handler.error && handler.fields.includes('artists')) {
            response = await Promise.all(
                response.artists.map(
                    async (artist) => {
                        const response = await Externals.get(
                            artist.href, handler.authExternal
                        )
                        return {
                            id: response.id, name: response.name,
                            profile: response.external_urls.spotify,
                            followers: response.followers.total,
                            images: response.images, genres: response.genres
                                .map((genre) => { return { name: genre, about: '' } })
                        }
                    }
                )
            )
            if (response.status_code) { handler.error = response }
            else { handler.data.artists = response }
        }
        return await handler
    }


    static async get(endpoint, token) {
        const response = await fetch(
            endpoint, { headers: { 'Authorization': `Bearer ${token}` } }
        ).then(response => response.json())
        return !response.error ? response :
            {
                ...{
                    400: { name: 'BadRequest' },
                    401: { name: 'Unauthorized' },
                    404: { name: 'NotFound' }
                }[response.error.status], status_code: response.error.status
            }
    }
}