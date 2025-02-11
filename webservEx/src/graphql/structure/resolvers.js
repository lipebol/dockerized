const { c_ } = require(process.env.CONTROLLER)

const resolvers = {
    async book(args, _, context) {
        args.about = { query: arguments.callee.name, context }
        return await c_.multi(args)
    },
    async nvi(args) {
        args.query = arguments.callee.name
        return await c_.multi(args)
    },
    async genre(args, _, context) {
        args.about = { query: arguments.callee.name, context }
        return await c_.multi(args)
    },
    async artist(args, _, context) {
        args.about = { query: arguments.callee.name, context }
        return await c_.multi(args)
    },
    async track(args) {
        args.query = arguments.callee.name
        return await c_.multi(args)
    }
}

module.exports = { resolvers }