from dataclasses import dataclass
from encodings import utf_8
from flask import Flask, jsonify, request
import pika

app = Flask(__name__)
if "__main__" == __name__:
    app.run(host="0.0.0.0", port=80)

@app.route('/listen', methods=['POST'])
def listen():
    def callback(ch, method, properties, body):
        print(" [x] %r" % body)
        global data
        data = body
        ch.basic_ack(delivery_tag= method.delivery_tag)
        connection.close()

    request_data = request.get_json()
    keys = request_data['keys'][0:]
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.exchange_declare(exchange='hw3', exchange_type='direct')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    for key in keys:
        channel.queue_bind( exchange='hw3', queue=queue_name, routing_key=key)
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming()
    return jsonify(msg=data.decode('utf_8'))

    
@app.route('/speak', methods=['POST'])
def speak():
    request_data = request.get_json()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='hw3', exchange_type='direct')
    channel.basic_publish(exchange='hw3', routing_key=request_data['key'], body=request_data['msg'])
    print(" [x] Sent %r under %r key" % (request_data['msg'], request_data['key']))
    connection.close()
    return jsonify(request_data),200

