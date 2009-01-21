def runga(context):
    
    from iga.gacommon import gaParams

    filename = context.get('app_name', 'funcopt.yml')
    gaParams.fileArgs('config/' + filename)
    pop = gaParams.consoleGA()

    return pop

def init_iga(context):
    
    from iga.gacommon import gaParams

    filename = context.get('app_name', 'funcopt.yml')
    gaParams.fileArgs('config/%s' % (filename))
    gaParams.onInit(context)

    return gaParams
