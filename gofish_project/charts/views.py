from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test
import json
import time

from models import DataPoint, EndGame

#################################################################
# CHART ADMIN
#################################################################
@user_passes_test(lambda u: u.is_superuser)
def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    context_dict = {}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('charts/index.html', context_dict, context)

@user_passes_test(lambda u: u.is_superuser)
def parseLog(request):
    numEntries = 0
    logCopy = 'logs-perf/gofish-' + str(time.time()) + '.log'
    # parse the log file
    with open('gofish.log', 'r') as f:
        with open(logCopy, 'w') as fw:
            for line in f:
                if line != '\n':
                    DataPoint.insertFromLine(line)
                    numEntries += 1
                    fw.write(line)

    # flush the log file
    with open('gofish.log', 'w') as f:
        pass

    # report on the number of processed lines
    context = RequestContext(request)
    context_dict = {'numEntries': numEntries}
    return render_to_response('charts/log_parsed.html', context_dict, context)

@user_passes_test(lambda u: u.is_superuser)
def dataByUser(request):
    choices = DataPoint.describeData()
    context = RequestContext(request)
    context_dict = {'choices': choices}
    return render_to_response('charts/data_user.html', context_dict, context)

@user_passes_test(lambda u: u.is_superuser)
def dataAggregated(request):
    context = RequestContext(request)
    context_dict = {
        'choices': {
            'bar': {
                'optTime'      : 'Optimality of Time',
                'optMoney'     : 'Optimality of Money',
                'loptTime'     : 'Local Opt. of Time',
                'loptMoney'    : 'Local Opt. of Money',
                'optTimeAbs'   : 'Absolute Opt. of Time',
                'optMoneyAbs'  : 'Absolute Opt. of Money',
                'loptTimeAbs'  : 'Absolute Loc. Opt. of Time',
                'loptMoneyAbs' : 'Absolute Loc. Opt. of Money'
            },
            'boxX': {
                'cueDetail'    : 'Detail of Cues',
                'level'        : 'Level of Game',
                'gameNum'      : 'Game Number',
                'fishCost'     : 'Fishing Cost',
                'moveCost'     : 'Moving Cost',
                'endGame'      : 'End Game',
                'level'        : 'Level of Game',
            },
            'boxY': {
                'optTime'      : 'Optimality of Time',
                'optMoney'     : 'Optimality of Money',
                'loptTime'     : 'Local Opt. of Time',
                'loptMoney'    : 'Local Opt. of Money',
                'optTimeAbs'   : 'Absolute Opt. of Time',
                'optMoneyAbs'  : 'Absolute Opt. of Money',
                'loptTimeAbs'  : 'Absolute Loc. Opt. of Time',
                'loptMoneyAbs' : 'Absolute Loc. Opt. of Money'
            }
        }
    }
    return render_to_response('charts/data_aggregated.html', context_dict, context)

#################################################################
# Endgame analytics
#################################################################
@user_passes_test(lambda u: u.is_superuser)
def parseEndLog(request):
    numEntries = 0
    logCopy = 'logs-end/end-' + str(time.time()) + '.log'
    # parse the log file
    with open('end.log', 'r') as f:
        with open(logCopy, 'w') as fw:
            for line in f:
                if line != '\n':
                    EndGame.insertFromLine(line)
                    numEntries += 1
                    fw.write(line)

    # flush the log file
    with open('end.log', 'w') as f:
        pass

    # report on the number of processed lines
    context = RequestContext(request)
    context_dict = {'numEntries': numEntries}
    return render_to_response('charts/log_parsed.html', context_dict, context)

@user_passes_test(lambda u: u.is_superuser)
def dataEndgame(request):
    context = RequestContext(request)
    context_dict = {
        'choices': {
            'groups': {
                'level'     : 'Level of Game',
                'moveCost ' : 'Moving Cost',
                'cueDetail' : 'Detail of Cues',
                'line'      : 'Level of Lines',
            },
            'choices': {
                'earned'    : 'Money Earned',
                'diffMax'   : '% of Max Possible Earnings',
                'diffOpt'   : '% of Opt Strategy Earnings',
                'diffLOpt'  : '% Local Opt Strategy Earnings',
            }
        }
    }
    return render_to_response('charts/data_endgame.html', context_dict, context)

#################################################################
# Optimisation of the Game
#################################################################
@user_passes_test(lambda u: u.is_superuser)
def optimise(request):
    context = RequestContext(request)

    # 1. Monte Carlo simulation
    yc = YieldSimulation(100)
    # 2. Build a cp model from resulting yields
    yields = yc.getYields()
    model = YieldModel(yields)
    # 3. Solve the model
    context_dict = model.optimise()
    # 4. Get descriptives for our simulation, if successful
    if context_dict['solution']:
        context_dict['stats'] = \
                yc.describeYields(context_dict['solution'])
        # 5. plot the earnings
        yc.exportEarnings(context_dict['solution'])
        # 6. export fish value distributions
        YieldSimulation.exportDistributions(yields, context_dict['solution'])


    return render_to_response('charts/optimise.html', context_dict, context)

#################################################################
# Data API
#################################################################
# data for single user query
@user_passes_test(lambda u: u.is_superuser)
def getData(request):
    qs = DataPoint.query(
        username  = request.GET.get('username', None),
        gameNum   = request.GET.get('gameNum', None),
        cueDetail = request.GET.get('cueDetail', None),
        level     = request.GET.get('level', None),
        moveCost  = request.GET.get('moveCost', None),
        endGame   = request.GET.get('endGame', None))

    response = {'data': [el.toDict() for el in qs]}
    return HttpResponse(json.dumps(response), content_type="application/json")

# data for aggregated bar charts 
@user_passes_test(lambda u: u.is_superuser)
def getBarData(request):
    qs = DataPoint.queryBarData(request.GET.get('x', None))

    response = {'data': [el for el in qs]}
    return HttpResponse(json.dumps(response), content_type="application/json")

# data for aggregated box charts
@user_passes_test(lambda u: u.is_superuser)
def getBoxData(request):
    qs = DataPoint.queryBoxData(
        x = request.GET.get('x', None),
        y = request.GET.get('y', None))

    response = {'data': [el for el in qs]}
    return HttpResponse(json.dumps(response), content_type="application/json")

# data for aggregated endgame bar charts
@user_passes_test(lambda u: u.is_superuser)
def getEndData(request):
    qs, x = EndGame.queryBarData(
        x = request.GET.get('x', None),
        y = request.GET.get('y', None))

    # we need x to decypher response
    response = {'data': qs, 'x': x}
    return HttpResponse(json.dumps(response), content_type="application/json")

# data for aggregated endgame box charts
@user_passes_test(lambda u: u.is_superuser)
def getEndBoxData(request):
    qs, x = EndGame.queryBoxData(
        x = request.GET.get('x', None),
        y = request.GET.get('y', None))

    # we need x to decypher response
    response = {'data': qs, 'x': x}
    return HttpResponse(json.dumps(response), content_type="application/json")

