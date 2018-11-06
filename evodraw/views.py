from django.shortcuts import render
from evodraw.lib.evospace import Population
# Create your views here.
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from evodraw.models import Collection, Collection_Individual
from evodraw.lib.evospace import Individual
from evodraw.lib.colors import init_pop, evolve_Tournament, one_like, add_rating
from django.views.decorators.http import require_http_methods
import time
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

EVOLUTION_INTERVAL = 8
REINSERT_THRESHOLD = 20
popName = 'pop'


def welcome(request):
    if request.user.is_authenticated and request.user != 'AnonymousUser':
        return render(request,
                      'evoi/welcome.html',
                                   { 'user':  request.user                                  # , 'plus_scope':plus_scope,'plus_id':plus_id
                                   } )
    else:
        return render(request,'evoi/welcome.html',
                                  {'user_name': None

                          })

def album(request):
    if request.user.is_authenticated and request.user != 'AnonymousUser':
        return render(request,
                      'evoi/album.html',
                                   { 'user':  request.user                                  # , 'plus_scope':plus_scope,'plus_id':plus_id
                                   } )
    else:
        return render(request,'evoi/album.html',
                                  {'user_name': None })



@require_http_methods(["POST"])
def ilike(request):
    one_like(request.POST['individual'], request.user.username, time.time())
    return HttpResponse("ok", content_type='text')


@require_http_methods(["POST"])
def rating(request):
    json_data = json.loads(request.body)
    add_rating(individual_id = json_data['individual_id'],rating = json_data['rating'],user= request.user.username, timestamp = time.time(), )
    return HttpResponse("ok", content_type='text')



@require_http_methods(["POST"])
def user_collection(request, collection_id):
    if request.method == 'POST' and request.user.is_authenticated and request.user != 'AnonymousUser':
        collection = Collection.objects.get(pk=collection_id)
        ci = Collection_Individual(
            individual_id = request.POST['individual'],
            collection = collection,
            added_from = None,
            from_user = None,
            date_added = now())
        ci.save()

        return HttpResponse(request.POST['individual'], content_type='application/json')


def user_collections(request):
    if request.user.is_authenticated and request.user != 'AnonymousUser':
        uc= Collection.objects.all().filter(owner=request.user)
        jd = { 'collections': [{'id': col.id, 'name':col.name} for col in uc]}
        j= json.dumps(jd)
        return HttpResponse(j, content_type='application/json')

    if request.method == 'POST' and request.user.is_authenticated and request.user != 'AnonymousUser':

            # Check if they exists

            c = Collection(name=request.POST['name'],
                          # description=request.POST['description'],
                           visibility='Public',
                           owner=request.user,
                           )
            c.save()
            return HttpResponse(c.id, content_type='application/json')




@require_http_methods(["GET"])
def get_my_album(request):
    if request.user.is_authenticated and request.user != 'AnonymousUser':
        c = None
        try:
            c = Collection_Individual.objects.filter(collection__owner=request.user)

        except ObjectDoesNotExist:
            print('ObjectDoesNotExist')


        individuals = [Individual(id=i.individual_id,visibility=i.visibility ).get(as_dict=True) for i in c]
        result = json.dumps({'data':individuals})


        return HttpResponse(result, content_type='application/json')
    else:
        return HttpResponse({}, content_type='application/json')




@require_http_methods(["POST"])
def add_to_collection(request):
    json_data = json.loads(request.body)
    if request.user.is_authenticated and request.user != 'AnonymousUser':
        c = None
        try:
            c = Collection.objects.filter(name="MyAlbum",visibility='Public',
                           owner=request.user).get()

        except ObjectDoesNotExist:
            print('ObjectDoesNotExist')
            c =  Collection.objects.create(name="MyAlbum",visibility='Public',
                                           owner=request.user,
                                           )
            c.save()

        Collection_Individual.objects.update_or_create( collection=c , individual_id=json_data['individual_id'],
           defaults={ 'collection':c , 'individual_id':json_data['individual_id'],'visibility':json_data['visibility']})
        data = json.dumps({"result": "Inserted", "error": None})
        return HttpResponse(data, content_type='application/json')
    else:
        data = json.dumps({"result": "Not Inserted", "error": "You need to Authenticate"})
        return HttpResponse(data, content_type='application/json')


@require_http_methods(["POST"])
def remove_from_my_album(request):
    json_data = json.loads(request.body)
    if request.user.is_authenticated and request.user != 'AnonymousUser':
        try:
            Collection_Individual.objects.filter(collection__name='MyAlbum',
                                                 collection__owner=request.user,
                                                 individual_id=json_data['individual_id']).delete()

        except ObjectDoesNotExist:
            print('Can not Delete')


        data = json.dumps({"result": "Deleted", "error": None})
        return HttpResponse(data, content_type='application/json')
    else:
        data = json.dumps({"result": "Not Deleted", "error": "You need to Authenticate"})
        return HttpResponse(data, content_type='application/json')


def evospace(request):
    if request.method == 'POST':
        population = Population(popName)
        json_data = json.loads(request.body)
        method = json_data["method"]
        params = json_data["params"]
        id = json_data["id"]


        print(method, params)
        if method == "initialize":
            result = population.initialize()
            data = json.dumps({"result": result, "error": None, "id": id})
            print (data)
            return HttpResponse(data, content_type='application/javascript')
        elif method == "get_sample":
            #Auto ReInsert
            if population.read_sample_queue_len() >= REINSERT_THRESHOLD:
                population.respawn(5)
            result = population.get_sample(params[0])
            if result:
                data = json.dumps({"result": result, "error": None, "id": id})
            else:
                data = json.dumps({"result": None, "error":
                    {"code": -32601, "message": "EvoSpace empty"}, "id": id})
            return HttpResponse(data, content_type='application/json')
        elif method == "read_pop_keys":
            result = population.read_pop_keys()
            if result:
                data = json.dumps({"result": result, "error": None, "id": id})
            else:
                data = json.dumps({"result": None, "error":
                    {"code": -32601, "message": "EvoSpace empty"}, "id": id})
            return HttpResponse(data, content_type='application/json')
        elif method == "read_sample_queue":
            result = population.read_sample_queue()
            if result:
                data = json.dumps({"result": result, "error": None, "id": id})
            else:
                data = json.dumps({"result": None, "error":
                    {"code": -32601, "message": "EvoSpace empty"}, "id": id})
            return HttpResponse(data, content_type='application/json')

        elif method == "put_sample":
            #Cada EVOLUTION_INTERVAL evoluciona
            print ("##################")
            if not population.get_returned_counter() % EVOLUTION_INTERVAL:
                try:
                    print ("Evolucionando")
                    evolve_Tournament()
                except Exception as e:
                    print (e.message)
                pass
            population.put_sample(params[0])

            # #Aqui se va armar la machaca del individuo
            # if request.user.is_authenticated():
            #     usr = request.user.username
            #     first_name = request.user.first_name
            #     last_name = request.user.last_name
            #     name = first_name + " " + last_name
            #     nodo = Nodo()
            #     person = Person()
            #     person_result = person.get_person(name)
            #     activity_stream = Activity_stream()
            #
            #     #print u
            #     print "=========Parametros==========="
            #     print params[0]
            #
            #     if params[0]["individuals_with_like"]:
            #         for item in params[0]["individuals_with_like"]:
            #             id = item
            #             print id
            #             individual_node = Graph_Individual()
            #
            #             print "prueba ", params[0]["individuals_with_like"]
            #
            #             # Verificar si el nodo individual existe con status last
            #             individual_node_exist = individual_node.get_node(id)
            #
            #             if person_result:
            #                 nodo1 = node(person_result[0][0])
            #
            #             if individual_node_exist: # si la lista esta vacia quiere decir que no existe
            #                 nodo2 = node(individual_node_exist[0][0])
            #
            #             relation = Relations()
            #             relation.likes(nodo1,nodo2)
            #
            #             #request.user.username in k
            #
            #             #Agreagando Activity stream para el verbo like
            #             activity_stream.activity("person", "like", "evaluate", usr)
            #
            #             #Curret experience calculation
            #             current_experience(request)
            #
            #     print "=========Parametros==========="
            # else:
            #     print ("Usuario anonimo")

            return HttpResponse(json.dumps("Success"), content_type='application/json')
        elif method == "init_pop":
            data = init_pop(populationSize=params[0])
            return HttpResponse(json.dumps("Success"), content_type='application/javascript')
        elif method == "respawn":
            data = population.respawn(n=params[0])
            return HttpResponse(json.dumps("Success"), content_type='application/javascript')
        elif method == "put_individual":
            print ( "params", params[0])
            population.put_individual(**params[0])
            data = json.dumps({"result": None, "error": None, "id": id})
            return HttpResponse(data, content_type='application/json')

    else:
        return HttpResponse("ajax & post please", content_type='text')
