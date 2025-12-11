import { Controllers } from '../../controllers.mjs'

class Resolvers {

    static create() {
        return {
            async spotifyAPI(args, context, info) {
                return await Controllers.multi(
                    Resolvers.handler(args, context, info)
                )
            },
            async spotifExArtists(args, context, info) {
                return await Controllers.multi(
                    Resolvers.handler(args, context, info)
                )
            },
            async spotifExTracks(args, context, info) {
                console.log(Resolvers.handler(args, context, info))
                return await Controllers.multi(
                    Resolvers.handler(args, context, info)
                )
            },
            async spotifExDaylists(args, context, info) {
                return await Controllers.multi(
                    Resolvers.handler(args, context, info)
                )
            }
        }
    }

    static handler(args, context, info) {
        return {
            headers: context.headers,
            filter: Object.keys(args)[0].toString(),
            params: Object.values(args)[0],
            about: {
                resolver: info.fieldName,
                type: info.returnType.ofType.name
                    .replace('Response', ''),
                fields: info.fieldNodes,
            }
        }
    }
}

export const resolvers = Resolvers.create()