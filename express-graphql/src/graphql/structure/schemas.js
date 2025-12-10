import { buildSchema } from 'graphql'

export const schemas = buildSchema(`
    scalar Date

    interface Errors {
        error: String!
        message: String!
        status_code: Int!
    }

    type NotFound implements Errors {
        error: String!
        message: String!
        status_code: Int!
    }

    type BadRequest implements Errors {
        error: String!
        message: String!
        status_code: Int!
    }

    type InternalError implements Errors {
        error: String!
        message: String!
        status_code: Int!
    }

    type Unauthorized implements Errors {
        error: String!
        message: String!
        status_code: Int!
    }

    type Info {
        total: Int
        pages: Int
    }

    type _ImageField_ {
        url: String
        width: Int
        height: Int
    }

    type _CopyrightField_ {
        text: String
        type: String
    }

    type spotifExGenresFields {
        name: String
        about: String
    }

    type spotifExArtistsFields {
        id: String
        name: String
        profile: String
        followers: Int
        images: [_ImageField_] 
        genres: [spotifExGenresFields]
    }

    type spotifExArtists {
        data: [spotifExArtistsFields]
    }

    type spotifExAlbumsFields {
        id: String
        name: String
        album_type: String
        release_date: String
        available_markets: [String]
        external_url: String
        images: [_ImageField_]
        total_tracks: Int
        copyrights: [_CopyrightField_]
        external_ids: String
        label: String
    }

    type spotifExTracksFields {
        trackid: String
        name: String
        album: spotifExAlbumsFields
        artists: [spotifExArtistsFields]
        url: String
        duration_ms: String
        popularity: Int
        explicit: Boolean
        track_number: Int
        disc_number: Int
        external_ids: String
    }

    type spotifExTracks {
        data: [spotifExTracksFields]
    }
    
    type spotifExDaylistsFields {
        track: spotifExTracksFields
        date: String
        listen: Int
    }

    type spotifExDaylists {
        data: [spotifExDaylistsFields]
    }

    union spotifExArtistsResponse = spotifExArtists | Info | NotFound | BadRequest | InternalError | Unauthorized
    union spotifExTracksResponse = spotifExTracks | Info | NotFound | BadRequest | InternalError | Unauthorized
    union spotifExDaylistsResponse = spotifExDaylists | Info | NotFound | BadRequest | InternalError | Unauthorized

    type Query {
        spotifyAPI(id: String): spotifExTracksResponse!
        spotifExArtists(name: String, page: Int, info: Boolean, lookup: Boolean): spotifExArtistsResponse!
        spotifExTracks(title: String, page: Int, info: Boolean, lookup: Boolean): spotifExTracksResponse!
        spotifExDaylists(date: String, page: Int, info: Boolean, lookup: Boolean): spotifExDaylistsResponse!
    }
`)