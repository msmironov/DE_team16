from kafka import KafkaProducer
import pandas as pd
import json

def kafka_python_producer_sync(producer, msg, topic):
    producer.send(topic, bytes(msg, encoding='utf-8'))
    print("Sending " + msg)
    producer.flush(timeout=60)

if __name__ == '__main__':
    producer = KafkaProducer(bootstrap_servers='34.135.27.110:9092')  # use your VM's external IP Here!
    with open("C:/Users/msmir/Desktop/Uni/Data Engineering/Assignment 2/data_ex.csv") as f:   # change this path to the path in your laptop
        lines = f.read().splitlines()

    for line in lines:

        arr = str.split(line, ',')

        arr = [s.replace('"', '') for s in arr]

        dic = {"id" : arr[0],
        "title" : arr[1],
        "type": arr[2],
        "genres": arr[3],
        "averageRating": arr[4],
        "numVotes": arr[5],
        "releaseYear": arr[6]}

        js = json.dumps(dic)

        kafka_python_producer_sync(producer, js, 'IMDB_6')

    f.close()
