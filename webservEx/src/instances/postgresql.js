const { Sequelize } = require(process.env.ORM)

const sequelizeConnect = new Sequelize(
    process.env.ENGINE_POSTGRESQL,
    {
        dialect: process.env.DIALECT,
        //port: parseInt(process.env.POSTGRES_PORT)
    }
)

module.exports = { Sequelize, sequelizeConnect }