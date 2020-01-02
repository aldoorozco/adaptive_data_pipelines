const fastify = require('fastify')({ logger: true })
const path = require('path')

const start = async () => {
  try {
    await fastify.listen(8080, '0.0.0.0')
    fastify.log.info(`server listening on ${fastify.server.address().port}`)
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
}
start()

fastify.register(require('fastify-static'), {
  root: path.join(__dirname, 'resources'),
  prefix: '/resources/',
})

fastify.get('/', function (req, reply) {
  reply.sendFile('index.html')
})
