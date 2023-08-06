confluo
=======

    From **con-** ‎(“with; together”) + **fluō** ‎(“flow”). **cōnfluō**
    ‎(present infinitive cōnfluere, perfect active cōnfluxī); third
    conjugation, no passive     1. (intransitive) I flow or run
    together, meet.     2. (intransitive, figuratively) I flock or crowd
    together, throng, assemble.

⇢ **confluo** is a scalable distributed microservice framework using
AMQP/RabbitMQ as a broker.

.. code:: python

    import asyncio
    from confluo.core import Service

    a = Service("Service-A")
    b = Service("Service-B")

    @b.subscribe("/foo/bar")
    async def foo_bar_event(path, headers, body):
        print("Got /foo/bar event with body: '{0}'".format(body))
        response = await b.call("Service-A", "/bar", {"data": "Some body data"})
        print("Got response: '{0}'".format(response))
            
    @a.route("/bar")
    async def bar_command(path, headers, body):
        print("Got /bar command with body: '{0}'".format(body))
        return {"value": 1}

    if __name__ == "__main__":
        # connect services
        loop.run_until_complete(asyncio.wait([a.connect(), b.connect()]))
        
        # Publish event
        loop.run_until_complete(a.publish("/foo/bar", "wtf"))

        loop = asyncio.get_event_loop()
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            loop.run_until_complete(asyncio.wait([a.shutdown(), b.shutdown()]))
            loop.stop()
            loop.close()

Usage
-----

Make sure rabbitmq is installed and running. e.g:

::

    sudo docker run -d --hostname my-rabbit --name some-rabbit rabbitmq:3-management
