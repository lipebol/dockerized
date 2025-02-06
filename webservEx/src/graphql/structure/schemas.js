const { buildSchema } = require(process.env.GRAPHQL_SCHEMA)

const schemas = buildSchema(`
    scalar Date

    type Query {
        genre(name: String, page: Int): [GENRE]
        artist(name: String, page: Int): [ARTIST]
        track(name: String, page: Int): [TRACK]
    }

    type GENRE {
        name: String
        url: String
    }

    type ARTIST {
        name: String
        profile: String
    }

    type TRACK {
        _id: ID
        trackid: String
        length: String
        artUrl: String
        album: String
        artist: ARTIST
        autoRating: String
        discNumber: String
        name: String
        trackNumber: String
        url: String
        genres: [GENRE]
    }
`)

module.exports = { schemas }