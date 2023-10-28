from django.shortcuts import render
import datetime
import hashlib
import json
from uuid import uuid4
import socket
from urllib.parse import urlparse
from django.http import JsonResponse, HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt #New




#Armar el blockchain
class Blockchain:

    def __init__(self):
        """ Constructor de la clase Blockchain. """

        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = []
        
    def add_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.append(parsed_url.netloc)
        
    def replace_chain(self):
        network = self.nodes
        print(network)
        longest_chain = None
        max_length = len(self.chain)
        
        for node in network:
            print(node)
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                data = response.json()
                length= data['length']
                print(length)
                chain = data['chain']
                
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
            
            if longest_chain:
                self.chain = longest_chain
                return True
        return False
         
    def create_block(self, proof, previous_hash):
  
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions':self.transactions}
        
        self.transactions = []
        self.chain.append(block)
        return block
    
    
    def add_transaction(self,sender,receiver,amount,time):
        self.transactions.append({
            'sender':sender,
            'receiver':receiver,
            'amount':amount})
        previous_block = self.get_previous_block()
        return previous_block['index']+1
    
        
    def get_previous_block(self):
        return self.chain[-1]
    

    def proof_of_work(self, previous_proof):
       

        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof*2 - previous_proof*2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        hash_block = hashlib.sha256(encoded_block).hexdigest()
        return hash_block
    

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]

            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof*2 - previous_proof*2).encode()).hexdigest()
            
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index += 1

        return True
    
    


# Creating our Blockchain
blockchain = Blockchain()
# Creating an address for the node running our server
node_address = str(uuid4()).replace('-', '') #New
root_node = 'e36f0158f0aed45b3bc755dc52ed4560d' #New
listNodes = list(blockchain.nodes)
# Mining a new block
def mine_block(request):
    if request.method == 'GET':
        previous_block = blockchain.get_previous_block()
        previous_nonce = previous_block['proof']
        nonce = blockchain.proof_of_work(previous_nonce)
        previous_hash = blockchain.hash(previous_block)
        blockchain.add_transaction(sender = root_node, receiver = node_address, amount = 1.15, time=str(datetime.datetime.now()))
        block = blockchain.create_block(nonce, previous_hash)
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'nonce': block['proof'],
                    'previous_hash': block['previous_hash'],
                    'transactions': block['transactions']}
        
    return JsonResponse(response)

# Getting the full Blockchain
def get_chain(request):

    if request.method == 'GET':
        response = {'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
        
    return JsonResponse(response)



def is_valid(request):

    if request.method == 'GET':
        is_valid = blockchain.is_chain_valid(blockchain.chain) 

        if is_valid:
            response = {'message': 'All good. The Blockchain is valid.'}

        else:
            response = {'message': 'We have a problem. The Blockchain is not valid.'}

    return JsonResponse(response)

# Adding a new transaction to the Blockchain
@csrf_exempt
def add_transaction(request): #New
    if request.method == 'POST':
        received_json = json.loads(request.body)
        print(received_json)
        transaction_keys = ['sender', 'receiver', 'amount','time']
        if not all(key in received_json for key in transaction_keys):
            return 'Some elements of the transaction are missing', HttpResponse(status=400)
        index = blockchain.add_transaction(received_json['sender'], received_json['receiver'], received_json['amount'],received_json['time'])
        response = {'message': f'This transaction will be added to Block {index}'}
    return JsonResponse(response)

# Connecting new nodes
@csrf_exempt
def connect_nodes(request): #New
    if request.method == 'POST':
        received_json = json.loads(request.body)
        print(str(received_json))
        nodes = received_json.get('nodes')
        print(nodes)
        if nodes is None:
            return "No node", HttpResponse(status=400)
        for node in nodes:
            blockchain.add_node(node)
        response = {'message': 'All the nodes are now connected. The Blockchain now contains the following nodes:',
                    'total_nodes': list(blockchain.nodes)}
    return JsonResponse(response)

# Replacing the chain by the longest chain if needed
def replace_chain(request): #New
    if request.method == 'GET':
        is_chain_replaced = blockchain.replace_chain()
        if is_chain_replaced:
            response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                        'new_chain': blockchain.chain}
        else:
            response = {'message': 'All good. The chain is the largest one.',
                        'actual_chain': blockchain.chain}
    return JsonResponse(response)
